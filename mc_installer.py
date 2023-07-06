import os
import subprocess
import PySimpleGUI as sg
import json
import minecraft_launcher_lib as mcll
from sys import argv
import urllib.request
from pathlib import Path
from os import getenv, path, mkdir

def main(type: str, ver: str):
    appdata = Path.joinpath(Path(getenv('LOCALAPPDATA')), Path("Aryamanee_Launcher"))
    if not path.exists(appdata):
        mkdir(appdata)
    minecraft_folder = Path.joinpath(appdata, Path(".minecraft"))
    if not path.exists(minecraft_folder):
        mkdir(minecraft_folder)

    current_max = 0
    current_progress = 0
    current_status = ""



    langfile = open(Path("lang/en_us.json"), "r")
    lang = json.loads(langfile.read())
    langfile.close()

    sg.theme("DarkAmber")

    layout = [[sg.Text(lang["installing"] + " " + type + " " + ver)],
              [sg.ProgressBar(max_value=0, key="progressbar")],
              [sg.Text("", key="statusbox"),]
              ]
    window = sg.Window(title = "Aryamanee Launcher - " + lang["installing"] + " " + type + " " + ver, layout = layout, size = (300, 100), enable_close_attempted_event=True, finalize=True)

    def set_status(status: str):
        nonlocal current_status
        current_status=status
        window["statusbox"].Update(current_status)
        if status == "Installation complete":
            window.close()

    def set_progress(progress: int):
        nonlocal current_progress
        current_progress = progress
        if current_max!=0:
            window["progressbar"].UpdateBar(current_count=current_progress, max=current_max)

    def set_max(new_max: int):
        nonlocal current_max
        current_max = new_max
        window["progressbar"].UpdateBar(current_count=current_progress, max=current_max)

    callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}


    mcdir = minecraft_folder
    if type == lang["vanilla"]:
        mcll.install.install_minecraft_version(ver, mcdir, callback)
    elif type == lang["fabric"]:
        mcll.fabric.install_minecraft_version(ver, mcdir, callback)
        mcll.fabric.install_fabric(ver, mcdir, callback)
    elif type == lang["forge"]:
        mcll.forge.install_minecraft_version(ver, mcdir, callback)
        if mcll.forge.supports_automatic_install(mcll.forge.find_forge_version(ver)):
            mcll.forge.install_forge_version(mcll.forge.find_forge_version(ver), mcdir, callback)
        else:
            print(mcll.utils.get_java_executable())
            fv = mcll.forge.find_forge_version(ver)
            urllib.request.urlretrieve("https://files.minecraftforge.net/maven/net/minecraftforge/forge/"+fv+"/forge-"+fv+"-installer.jar", "forge-"+fv+"-installer.jar")
            subprocess.run(mcll.utils.get_java_executable()+" -jar "+f"forge-{fv}-installer.jar")
            os.remove(f"forge-{fv}-installer.jar")
    else:
        window.close()
    if current_status == "Installation complete":
        window.close()

if __name__ == "__main__":
    main(argv[1], argv[2])