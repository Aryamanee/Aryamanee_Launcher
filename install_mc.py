import os

import PySimpleGUI as sg
import json
import minecraft_launcher_lib as mcll
import subprocess

def main(pos = (323, 144)):
    langfile = open("lang\\en_us.json", "r")
    lang = json.loads(langfile.read())
    langfile.close()
    sg.theme("DarkAmber")

    layout = [
        [sg.Text(lang["type"], size=(20,1)), sg.Combo(values=[lang["vanilla"], lang["fabric"], lang["forge"]], readonly=True, enable_events=True)],
        [sg.Text(lang["version"], size=(20,1)), sg.Combo(values=[], key="-versions-", readonly=True, size=(100,1), enable_events=True)],
        [sg.Checkbox(lang["release"], enable_events=True, default=True)],
        [sg.Button(lang["install"], disabled=True)],
        [sg.Button(button_text="Close"), sg.ProgressBar(max_value=100, key="progressbar")]
    ]

    window = sg.Window('Aryamanee Launcher - Add Version', layout, size=(720,480), relative_location=(0,0), location=pos)
    while True:
        event, values = window.read()
        print(values)
        print(event)
        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            pos = window.current_location()
            print(mcll.utils.get_version_list())
            window.close()
            import main
            main.main(pos)
            break

        if event == 0 or event == 1:
            stableversions = []
            versionsdisplay = []
            stableversionsdisplay = []
            if values[0] == lang["vanilla"]:
                versions = mcll.utils.get_version_list()
                for ver in versions:
                    versionsdisplay.append(ver["id"])
                    if ver["type"] == "release":
                        stableversions.append(ver)
                        stableversionsdisplay.append(ver["id"])
            elif values[0] == lang["fabric"]:
                versions = mcll.fabric.get_all_minecraft_versions()
                for ver in versions:
                    versionsdisplay.append(ver["version"])
                    if ver["stable"] == True:
                        stableversions.append(ver)
                        stableversionsdisplay.append(ver["version"])
            elif values[0] == lang["forge"]:
                version = mcll.utils.get_version_list()
                versions = []
                for ver in version:
                    fv = mcll.forge.find_forge_version(ver["id"])
                    if fv != None:# and mcll.forge.supports_automatic_install(fv):
                        versions.append(ver)
                        versionsdisplay.append(ver["id"])
                for ver in versions:
                    if ver["type"] == "release":
                        stableversions.append(ver)
                        stableversionsdisplay.append(ver["id"])
            if values[1]:
                window["-versions-"].Update(values=stableversionsdisplay)
                window[lang["install"]].Update(disabled=True)
            else:
                window["-versions-"].Update(values=versionsdisplay)
                window[lang["install"]].Update(disabled=True)
        if event == lang["install"]:
            subprocess.Popen("py mc_installer.py " + values[0] + " " + values["-versions-"])
            if values[0] == lang["vanilla"]:
                print(values["-versions-"])
            elif values[0] == lang["fabric"]:
                print(values["-versions-"])
            elif values[0] == lang["forge"]:
                print(mcll.forge.find_forge_version(values["-versions-"]))
                #print(mcll.forge.is_forge_version_valid(mcll.forge.find_forge_version(values["-versions-"])))
                



        if event == "-versions-":
            if values[0] != "" and values["-versions-"] != "":
                window[lang["install"]].Update(disabled=False)
            else:
                window[lang["install"]].Update(disabled=True)

if __name__ == "__main__":
    main()