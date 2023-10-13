# This is Firepaw's file formatting tool.
# Feel free to develop plugins and use this for your own benefit.
# There is no warranty for ANYTHING made using this program.
#
#
# Handles window building. Takes parameters from settings.json.
# Reads code from folders found in FFTWindowPlugins.
import importlib
import sys

import os
import json
import FFTWindowPlugins.FFTWPMain as FFTWPMain
import FFTExportPlugins.FFTEPMain as FFTEPMain
import FFTReadPlugins.FFTRPMain as FFTRPMain
import FFTInstallPlugin as FFTIP
import tkinter as tk

from tkinter import Menu, Scrollbar

folderPath = os.path.abspath(os.path.dirname(__file__))

settings = {}
pluginSettings = {}


class DraggableBox(tk.Label):
    def __init__(self, master, grid_app, text=""):
        super().__init__(master, text=text, bg='lightblue', relief='raised', padx=10, pady=5)
        self.grid_app = grid_app

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_drag)
        # Bind the Delete key event to the delete_box method
        self.bind("<ButtonPress-3>", self.delete_box)

        self.start_col = None
        self.start_row = None
        self.box_positions = []

    def delete_box(self, event):
        # Delete the last clicked box
        self.destroy()

    def on_press(self, event):
        self.master.last_clicked_box = self
        self._drag_data = {'x': event.x, 'y': event.y}
        self.start_col = self.grid_info()["column"]
        self.start_row = self.grid_info()["row"]

    def on_release(self, event):
        x = self.winfo_x()
        y = self.winfo_y()

        # Find the nearest row and column for the released box
        nearest_row, nearest_col = self.find_nearest_row_and_col(x, y)

        x_dimension = 2
        y_dimension = len(self.grid_app.widgets)
        loc = [[-1] * x_dimension for _ in range(y_dimension)]
        # loc[box] [0 = col, 1 = row]
        for box in self.grid_app.widgets:
            newLine = [box.grid_info().get('column'), box.grid_info().get('row')]
            loc.append(newLine)
        y = 0
        if [nearest_col, nearest_row] in loc:
            y = nearest_row
            while [nearest_col, y] in loc:
                y += 1

        # Move all boxes in the same column down one row
        for box in self.grid_app.widgets:
            box_row = box.grid_info().get('row')
            box_col = box.grid_info().get('column')
            if "row" in box.grid_info() and box_col == nearest_col and y >= box_row >= nearest_row:
                box.grid(row=box.grid_info().get('row') + 1, column=nearest_col)

        # Snap the released box to its new position
        self.grid(row=nearest_row, column=nearest_col)

    def find_nearest_row_and_col(self, x, y):
        nearest_row = int(y / self.winfo_height()) - 1
        nearest_col = int(x / self.winfo_width())
        if nearest_col < 0:
            nearest_col = 0
        if nearest_row < 0:
            nearest_row = 0
        if nearest_col > 1:
            nearest_col = 1

        return nearest_row, nearest_col

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_data['x'] + event.x
        y = self.winfo_y() - self._drag_data['y'] + event.y
        self.place(x=x, y=y)


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firepaw's Formatting Tool")
        self.root.geometry(f"{settings['sizeX']}x{settings['sizeY']}+{settings['locX']}+{settings['locY']}")
        self.widgets = []

        # Add a menu bar at the top
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create a canvas for the scrollable frame
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar on the right side
        scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the draggable boxes
        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor=tk.NW)

        self.grid_frame.bind("<Configure>", self.on_frame_configure)
        # use this to test grid behaviors
        # self.create_grid()

        # Add tabs to the menu
        tabs = str(pluginSettings["tabs"])
        self.add_tabs_to_menu(tabs)

        # Bind the window close event to on_close()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def parse_geometry(self, geometry):
        # Parse the geometry string (e.g., "400x400+100+100") into sizeX, sizeY, locX, and locY
        size, locX, locY = geometry.split("+")
        sizeX, sizeY = map(int, size.split("x"))
        return sizeX, sizeY, locX, locY

    def save_settings(self):
        geo = self.root.geometry()
        sizeX, sizeY, locX, locY = self.parse_geometry(geo)
        settings["sizeX"] = sizeX
        settings["sizeY"] = sizeY
        settings["locX"] = locX
        settings["locY"] = locY

    # closing procedure
    def on_close(self):
        self.save_settings()
        FFTClose()
        self.root.destroy()

    # populates boxes
    # test
    def create_grid(self):
        for row in range(16):
            for col in range(2):
                box = DraggableBox(self.grid_frame, self, f"Box {row}-{col}")
                box.grid(row=row, column=col, padx=1, pady=1)
                self.widgets.append(box)

    # import
    def import_grid(self, data):
        for row, row_data in enumerate(data):
            for col, box_label in enumerate(row_data):
                box = DraggableBox(self.grid_frame, self, box_label)
                box.grid(row=row, column=col, padx=1, pady=1)
                self.widgets.append(box)

    # exports boxes

    def add_row(self):
        new_box = DraggableBox(self.grid_frame, self, f"New Box")
        new_box.grid(row=len(self.widgets) // 2, column=len(self.widgets) % 2, padx=1, pady=1)
        self.widgets.append(new_box)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_tabs_to_menu(self, tabs):
        tab_list = tabs.split(',')
        print(tab_list)
        for tab in tab_list:
            self.add_tab_to_menu(tab)

    def add_tab_to_menu(self, tab):
        file_menu = self.root.nametowidget(".!menu")
        tab_menu = tk.Menu(file_menu)
        if tab == 'File':
            self.file_tab(tab_menu)
        if tab == 'Exports':
            self.exports_tab(tab_menu)
        if tab == 'Read Modes':
            self.read_tabs(tab_menu)
        if tab == 'Plugins':
            self.plugin_tabs(tab_menu)
        file_menu.add_cascade(label=tab, menu=tab_menu)

    def file_tab(self, tab_menu):
        tab_menu.add_command(label="Save", command=lambda: FFTWPMain.saveFile(self))
        tab_menu.add_command(label="Settings", command=lambda: FFTWPMain.changeSettings(self))
        tab_menu.add_command(label="Import", command=lambda: FFTRPMain.readFile(self, pluginSettings))
        tab_menu.add_command(label="Export", command=lambda: FFTEPMain.exportFile(self, pluginSettings))

    def exports_tab(self, tab_menu):
        export_plugins_dir = os.path.join(folderPath, "FFTExportPlugins")
        if export_plugins_dir not in sys.path:
            sys.path.append(export_plugins_dir)
        tab_list = pluginSettings['Exports'].split(',')
        for name in tab_list:
            try:
                module = importlib.import_module(name)
                tab_menu.add_command(label=name, command=lambda mod=module: self.export_combined_function(mod))
            except ImportError:
                print(f"{name}.py was not found. Please ensure your entry in FFTWindowPlugins\\exports.txt\n"
                      f"matches the name of your plugin's script, your function has an entry point called main(),"
                      f" and does not contain any spaces.")

    def export_combined_function(self, module):
        module.main(self)
        FFTEPMain.set_export(module)

    def read_tabs(self, tab_menu):
        read_plugins_dir = os.path.join(folderPath, "FFTReadPlugins")
        if read_plugins_dir not in sys.path:
            sys.path.append(read_plugins_dir)
        tab_list = pluginSettings['Reads'].split(',')
        for name in tab_list:
            try:
                module = importlib.import_module(name)
                tab_menu.add_command(label=name, command=lambda mod=module: mod.main(self))
                FFTRPMain.set_import(module)
            except ImportError:
                print(f"{name}.py was not found. Please ensure your entry in FFTWindowPlugins\\exports.txt\n"
                      f"matches the name of your plugin's script, your function has an entry point called main(),"
                      f" and does not contain any spaces.")

    def plugin_tabs(self, tab_menu):

        tab_menu.add_command(label="Install Plugins", command=lambda: FFTIP.install(self))
        tab_menu.add_command(label="Uninstall Plugins", command=lambda: FFTIP.uninstall(self))
        tab_menu.add_command(label="Veiw Plugins", command=lambda: FFTIP.veiw(self))

    def getBoxes(self):
        box_contents = [['' for _ in range(2)] for _ in range(len(self.widgets))]  # Initialize a 2D array

        for box in self.widgets:
            row = box.grid_info()["row"]
            col = box.grid_info()["column"]
            text = box.cget("text")
            box_contents[row][col] = text

        return box_contents


def readSettings():
    global settings
    file_path = folderPath + '\\settings.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                settings[key] = value
            return 1
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error while decoding JSON data in the file: {e}")
        return None
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None


def saveSettings():
    with open(folderPath + '\\settings.json', 'w') as json_file:
        json.dump(settings, json_file)


def FFTClose():
    saveSettings()
    FFTWPMain.savePluginSettings()


def createWindow(in_settings):
    global pluginSettings
    readSettings()
    pluginSettings = in_settings
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
