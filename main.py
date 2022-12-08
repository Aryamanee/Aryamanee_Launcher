import PySimpleGUI as sg
import msmcauth
import minecraft_launcher_lib as mcll
import json
from accounts.account import account_class
import subprocess
from uuid import uuid4
def main(pos=(0,0)):
    langfile = open("lang\\en_us.json", "r")
    lang = json.loads(langfile.read())
    langfile.close()

    sg.theme('DarkAmber')

    try:
        accountsfile = open("accounts\\accounts.json", "r")
    except FileNotFoundError:
        accountsfile = open("accounts\\accounts.json", "w+")
        accountsfile.write("{}")
        accountsfile.close()
        accountsfile = open("accounts\\accounts.json", "r")
    accounts = json.loads(accountsfile.read())
    accountsfile.close()
    accountnames=[]
    for acc in accounts:
        print(accounts[acc]["username"])
        if accounts[acc]["cracked"] == "no":
            cracked = False
        else:
            cracked = True
        accountnames.append(account_class(acc, accounts[acc]["username"], cracked, accounts[acc]["email"], accounts[acc]["password"]))

    versionnames = []
    for version in mcll.utils.get_installed_versions(".minecraft"):
        versionnames.append(version["id"])

    layout = [[sg.Text(lang["account"], size=(7, 1)), sg.Combo(values=accountnames, readonly=True), sg.Button(lang["add_microsoft_account"]), sg.Button(lang["add_cracked_account"])],
              [sg.Text(lang["version"], size=(7, 1)), sg.Combo(size=(70,1), values=versionnames, readonly=True), sg.Button(lang["add_version"])],
              [sg.Button(lang["launch_minecraft"])]]

    window = sg.Window('Aryamanee Launcher', layout, size=(720, 480), relative_location=(0, 0), location=pos)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print(values)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        if event == lang["add_microsoft_account"]:
            pos = window.current_location()
            window.close()
            import add_microsoft_account
            add_microsoft_account.main(pos)
            break
        if event == lang["add_cracked_account"]:
            pos = window.current_location()
            window.close()
            import add_cracked_account
            add_cracked_account.main(pos)
            break
        if event == lang["add_version"]:
            pos = window.current_location()
            window.close()
            import install_mc
            install_mc.main(pos)
            break
        if event == lang["launch_minecraft"]:
            if values[0].cracked:
                options = {
                    "username": values[0].username,
                    "uuid": values[0].uuid,
                    "token": ""
                }
                cmd = mcll.command.get_minecraft_command(values[1]["id"], ".minecraft", options)
                subprocess.Popen(cmd)
            else:
                try:
                    login = msmcauth.login(values[0].email, values[0].password)
                    print(login)
                    options = {
                        "username": login.username,
                        "uuid": login.uuid,
                        "token": login.access_token
                    }
                    cmd = mcll.command.get_minecraft_command(values[1], ".minecraft", options)
                    subprocess.Popen(cmd)
                except msmcauth.InvalidCredentials:
                    sg.popup(lang["incorrect_login"], title=lang["login_error"])
                except msmcauth.ChildAccount:
                    sg.popup_error(title=lang["login_error"])
                except msmcauth.LoginWithXboxFailed:
                    sg.popup_error(title=lang["login_error"])
                except msmcauth.NotPremium:
                    sg.popup_error(title=lang["login_error"])
                except msmcauth.NoXboxAccount:
                    sg.popup_error(title=lang["login_error"])
                except msmcauth.TwoFactorAccount:
                    sg.popup_error(title=lang["login_error"])
                except msmcauth.XstsAuthenticationFailed:
                    sg.popup_error(title=lang["login_error"])


if __name__=="__main__":
    main((323, 144))