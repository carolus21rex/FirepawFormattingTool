# This is Firepaw's file formatting tool.
# Feel free to develop plugins and use this for your own benefit.
# There is no warranty for ANYTHING made using this program.
#
#


import os
import json
import FFTWindow
import FFTWindowPlugins.FFTWPMain as FFTWPMain

folderPath = os.path.abspath(os.path.dirname(__file__))
pluginSettings = {}


def pluginSettings():
    global pluginSettings
    # plugin settings
    pluginSettings = FFTWPMain.readPluginSettings()

    pluginSettings['tabs'] = FFTWPMain.getTabsToString()
    pluginSettings['Exports'] = FFTWPMain.getExportModesToString()
    pluginSettings['Reads'] = FFTWPMain.getReadModesToString()
    print(pluginSettings)


def FFTMainInit():
    pluginSettings()


# Entry Point

FFTMainInit()

FFTWindow.createWindow(pluginSettings)
