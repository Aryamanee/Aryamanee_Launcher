import PySimpleGUI as sg
import msmcauth
import json
from subprocess import call
from os import startfile
from uuid import uuid4

def main(pos = (323, 144)):
    langfile = open("lang\\en_us.json", "r")
    lang = json.loads(langfile.read())
    langfile.close()


    try:
        accountsfile = open("accounts\\accounts.json", "r")
    except FileNotFoundError:
        accountsfile = open("accounts\\accounts.json", "w+")
        accountsfile.write("{}")
        accountsfile.close()
        accountsfile = open("accounts\\accounts.json", "r")
    accounts = json.loads(accountsfile.read())
    accountsfile.close()

    sg.theme("DarkAmber")

    layout = [
        [sg.Text(lang["username"], size=(20,1)), sg.InputText(size=(50,1))],
        [sg.Button(button_text=lang["add_account"]), sg.Button(button_text="Close")]
    ]

    window = sg.Window('Cracked Login', layout, size=(720,480), relative_location=(0,0), finalize=True)

    while True:
        event, values = window.read()
        print(values)
        print(event)

        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            pos=window.current_location()
            window.close()
            import main
            main.main(pos)
            break
        if event == lang["add_account"]:
            uuid = str(uuid4()).replace("-", "")
            accounts[uuid] = {"username": values[0], "email": "", "password": "", "cracked": "yes"}

            accountsfile = open("accounts\\accounts.json", "w+")
            accountsfile.write(json.dumps(accounts))
            accountsfile.close()

if __name__ == "__main__":
    main()