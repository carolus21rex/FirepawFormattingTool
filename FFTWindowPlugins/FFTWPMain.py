import os
import json
folderPath = os.path.abspath(os.path.dirname(__file__))

def getTabsToString():
    file_path = folderPath+'\\tabs.txt'
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            content_with_commas = content.replace('\n', ',')
            return content_with_commas
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None


def getExportModesToString():
    file_path = folderPath+'\exports.txt'
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            content_with_commas = content.replace('\n', ',')
            return content_with_commas
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None


def getReadModesToString():
    file_path = folderPath+'\\reads.txt'
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            content_with_commas = content.replace('\n', ',')
            return content_with_commas
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None

def doNothing(self):
    self.add_row()
    return
def readPluginSettings():
    file_path = folderPath+'\\pluginSettings.json'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error while decoding JSON data in the file: {e}")
        return None
    except Exception as e:
        print(f"Error while reading the file: {e}")
        return None


def savePluginSettings():
    return None


def saveFile(self):
    print(1)
    return None


def changeSettings(self):
    print(2)
    return None