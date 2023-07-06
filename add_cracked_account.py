import PySimpleGUI as sg
import json
from uuid import uuid4
from pathlib import Path
from os import getenv, path, mkdir

def main(pos = (323, 144)):
    appdata = Path.joinpath(Path(getenv('LOCALAPPDATA')), Path("Aryamanee_Launcher"))
    if not path.exists(appdata):
        mkdir(appdata)

    langfile = open(Path("lang/en_us.json"), "r")
    lang = json.loads(langfile.read())
    langfile.close()

    try:
        accountsfile = open(Path.joinpath(appdata, Path("accounts.json")), "r")
    except FileNotFoundError:
        accountsfile = open(Path.joinpath(appdata, Path("accounts.json")), "w+")
        accountsfile.write("{}")
        accountsfile.close()
        accountsfile = open(Path.joinpath(appdata, Path("accounts.json")), "r")
    accounts = json.loads(accountsfile.read())
    accountsfile.close()

    sg.theme("DarkAmber")

    layout = [
        [sg.Text(lang["username"], size=(20,1)), sg.InputText(size=(50,1))],
        [sg.Button(button_text=lang["add_account"]), sg.Button(button_text="Close")]
    ]

    window = sg.Window('Aryamanee Launcher - Cracked Login', layout, size=(720,480), relative_location=(0,0), finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            pos=window.current_location()
            window.close()
            import main
            main.main(pos)
            break
        if event == lang["add_account"]:
            uuid = str(uuid4()).replace("-", "")
            accounts[uuid] = {"username": values[0], "email": "", "password": "", "cracked": "yes"}

            accountsfile = open(Path("accounts/accounts.json"), "w+")
            accountsfile.write(json.dumps(accounts))
            accountsfile.close()

if __name__ == "__main__":
    main()