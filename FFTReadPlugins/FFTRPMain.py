import importlib
from tkinter import filedialog
file_type = [("All Files", "*.*")]
read_plugin = None

def readFile(self, settings):
    global read_plugin
    if read_plugin != "":
        file = filedialog.askopenfilename(filetypes=file_type)
        imports = read_plugin.import_file(file, settings)
        return self.import_grid(imports)
    print("You must set your read mode first")
    return None



def set_import(module):
    global file_type, read_plugin
    file_type = module.set_import()
    read_plugin = module
