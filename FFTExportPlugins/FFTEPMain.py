from tkinter import filedialog

file_type = [("All Files", "*.*")]
export_plugin = None


def exportFile(self, settings):
    global export_plugin
    print(export_plugin)
    if export_plugin:
        file = filedialog.asksaveasfilename(filetypes=file_type, defaultextension=".txt")
        if file:
            export_plugin.export_file(file, settings, self)
    else:
        print("You must set your export mode first")
    return None


def set_export(module):
    global file_type, export_plugin
    file_type = module.set_export()
    export_plugin = module
    print(file_type)
