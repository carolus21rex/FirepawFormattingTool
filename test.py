import tkinter as tk
import FFTExportPlugins as FFTEP
import FFTReadPlugins as FFTRP
import FFTWindowPlugins as FFTWP

from tkinter import Menu, Scrollbar

class DraggableBox(tk.Label):
    def __init__(self, master, grid_app, text=""):
        super().__init__(master, text=text, bg='lightblue', relief='raised', padx=10, pady=5)
        self.grid_app = grid_app

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_drag)

        self.start_col = None
        self.start_row = None
        self.box_positions = []

    def on_press(self, event):
        self._drag_data = {'x': event.x, 'y': event.y}
        self.start_col = self.grid_info()["column"]
        self.start_row = self.grid_info()["row"]

    def on_release(self, event):
        x = self.winfo_x()
        y = self.winfo_y()

        # Find the nearest row and column for the released box
        nearest_row, nearest_col = self.find_nearest_row_and_col(x, y)

        # Move all boxes in the same column down one row
        for box in self.grid_app.widgets:
            box_row = box.grid_info().get('row')
            box_col = box.grid_info().get('column')
            if "row" in box.grid_info() and box_col == nearest_col and box_row >= nearest_row:
                box.grid(row=box.grid_info().get('row') + 1, column=nearest_col)

        # Snap the released box to its new position
        self.grid(row=nearest_row, column=nearest_col)
        self.pack_boxes()

    def find_nearest_row_and_col(self, x, y):
        nearest_row = int(y / self.winfo_height())
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

    def pack_boxes(self):
        x_dimension = 2
        y_dimension = len(self.grid_app.widgets)
        loc = [[-1] * x_dimension for _ in range(y_dimension)]
        # loc[box] [0 = col, 1 = row]
        changed = 1

        for box in self.grid_app.widgets:
            newLine = [box.grid_info().get('column'), box.grid_info().get('row')]
            loc.append(newLine)
        while changed == 1:
            xii = 0
            for box in self.grid_app.widgets:
                box_row = box.grid_info().get('row')
                box_col = box.grid_info().get('column')
                if "row" in box.grid_info() and [box_col, box_row - 1] not in loc and box_row > 0:
                    xii = 1
                    box.grid(row=box.grid_info().get('row') - 1, column=box_col)
            if xii == 0:
                changed = 0


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid App")
        self.root.geometry("400x400")
        self.widgets = []

        # Add a menu bar at the top
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Row", command=self.add_row)

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
        self.create_grid()

        # Add tabs to the menu
        tabs = "settings, export modes, import modes"
        self.add_tabs_to_menu(tabs)

    def create_grid(self):
        for row in range(16):
            for col in range(2):
                box = DraggableBox(self.grid_frame, self, f"Box {row}-{col}")
                box.grid(row=row, column=col, padx=1, pady=1)
                self.widgets.append(box)

    def add_row(self):
        new_box = DraggableBox(self.grid_frame, self, f"New Box")
        new_box.grid(row=len(self.widgets) // 2, column=len(self.widgets) % 2, padx=1, pady=1)
        self.widgets.append(new_box)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_tabs_to_menu(self, tabs):
        tab_list = tabs.split(', ')
        for tab in tab_list:
            self.add_tab_to_menu(tab)

    def add_tab_to_menu(self, tab):
        file_menu = self.root.nametowidget(".!menu.!file")
        tab_menu = tk.Menu(file_menu)
        tab_menu.add_command(label="Default", command=FFTWP.FFTWPMain.doNothing)  # Calls the method from another folder
        file_menu.add_cascade(label=tab, menu=tab_menu)





def createWindow(settings):

    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
