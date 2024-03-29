import configparser, webbrowser, threading, traceback, client, etc, os
import PySimpleGUI as sg

lang = etc.load_lang()
word = lang["Word"]
servers = []

main_layout = [
    [sg.Text("AllServer GUI Client", font=("", 20))],
    [sg.Text(lang["Text"][7], font=("", 14))],
    [sg.Text(lang["Text"][0]), sg.Input(key="listserverip"), sg.Button(lang["Button"][0],key="searchserver")],
    [sg.Text(lang["Text"][6], font=("", 14))],
    [sg.Text(lang["Text"][4]), sg.Input(key="mcid")],
    [sg.Text(lang["Text"][5]), sg.Input(key="motd")],
    [sg.Text(lang["Text"][1]), sg.Input(key="minecraftserverip"), sg.Button(lang["Button"][1],key="makeserver")],
    [sg.Text(lang["Text"][2], font=("", 14))],
    [sg.Table(servers, headings=[word[1],"IP",word[2],word[3],word[4]], key="serverlist",
        col_widths=lang["SgTableRatio"], auto_size_columns=False, display_row_numbers=True, bind_return_key=True, expand_y=True)],
    [sg.Text(lang["Text"][3], font=("", 14))],
    [sg.Multiline(key="log", size=(83, 5), disabled=True)],
    [sg.Button(lang["Button"][3], key="Help"), sg.Button(lang["Button"][2], key="Quit")]
]

def gui_start():
    global word
    is_readonly = True
    is_minecraft_run = False
    if os.path.isfile("nostop"): os.remove("nostop")
    try:
        window = sg.Window("AllServer -Client-", main_layout, disable_close=True)
        while True:
            event, values = window.read(timeout=50)
            if os.path.isfile("3141592653589793238") and is_readonly:
                window["log"].update(disabled=False)
                is_readonly = False
            if not os.path.isfile("nostop"):
                is_minecraft_run = False
            if event == "Quit" and not is_minecraft_run:
                break
            elif event == "Quit" and is_minecraft_run:
                sg.Popup(lang["ErrorMessage"][3], title="Cant Quit")
            elif event == "searchserver":
                result, servers = client.search_servers(values["listserverip"])
                if result == 0:
                    window["log"].print(lang["Message"][0])
                else:
                    window["log"].print(word[7]+" : "+lang["ErrorMessage"][0])
                    continue
                window["serverlist"].update(servers)
            elif event == "makeserver" and not is_minecraft_run:
                if values["mcid"] == "":
                    continue
                thread = threading.Thread(target=client.start_server, args=(values["minecraftserverip"], values["motd"], values["mcid"], window))
                thread.start()
                is_minecraft_run = True
            elif event == "Help":
                ini = configparser.ConfigParser()
                ini.read('config/basic.ini', 'UTF-8')
                lang_name = ini["lang"]["lang"]
                webbrowser.open(os.path.abspath(f"./detailed-manual/manual-{lang_name}.html"))
    except KeyboardInterrupt:
        return
    except:
        sg.PopupError(lang["Word"][7]+" : \n"+traceback.format_exc())