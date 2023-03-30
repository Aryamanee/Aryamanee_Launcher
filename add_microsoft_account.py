import PySimpleGUI as sg
import msmcauth
import json
from pathlib import Path

def main(pos = (323, 144)):
    langfile = open(Path("lang/en_us.json"), "r")
    lang = json.loads(langfile.read())
    langfile.close()


    try:
        accountsfile = open(Path("accounts/accounts.json"), "r")
    except FileNotFoundError:
        accountsfile = open(Path("accounts/accounts.json"), "w+")
        accountsfile.write("{}")
        accountsfile.close()
        accountsfile = open(Path("accounts/accounts.json"), "r")
    accounts = json.loads(accountsfile.read())
    accountsfile.close()

    sg.theme("DarkAmber")

    layout = [
        [sg.Text(lang["email"], size=(20,1)), sg.InputText(size=(50,1))],
        [sg.Text(lang["password"], size=(20,1)), sg.InputText(password_char='*', size=(50,1))],
        [sg.Button(button_text=lang["add_account"]), sg.Button(button_text="Close")]
    ]

    window = sg.Window('Aryamanee Launcher - Microsoft Login', layout, size=(720,480), relative_location=(0,0), finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
            pos=window.current_location()
            window.close()
            import main
            main.main(pos)
            break
        if event == lang["add_account"]:
            try:
                login = msmcauth.login(values[0], values[1])
            except msmcauth.InvalidCredentials:
                sg.popup(lang["incorrect_login"], title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break
            except msmcauth.ChildAccount:
                sg.popup_error(title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break
            except msmcauth.LoginWithXboxFailed:
                sg.popup_error(title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break
            except msmcauth.NotPremium:
                sg.popup_error(title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break
            except msmcauth.NoXboxAccount:
                sg.popup_error(title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break
            except msmcauth.TwoFactorAccount:
                sg.popup_error(title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break
            except msmcauth.XstsAuthenticationFailed:
                sg.popup_error(title=lang["login_error"])
                pos=window.current_location()
                window.close()
                import main
                main.main(pos)
                break

            accounts[login.uuid] = {"username": login.username, "email": values[0], "password": values[1], "cracked": "no"}

            accountsfile = open(Path("accounts/accounts.json"), "w+")
            accountsfile.write(json.dumps(accounts))
            accountsfile.close()

if __name__ == "__main__":
    main()