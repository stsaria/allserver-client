import threading, traceback, client, etc, os
import PySimpleGUI as sg

lang = etc.load_lang()

main_layout = [
    [sg.Text("AllServer GUI Client", font=("", 20))],
    [sg.Text(lang["Text"][2], font=("", 12))],
    [sg.Multiline(key="serverlist", size=(90, 15), disabled=True)],
    [sg.Text(lang["Text"][3], font=("", 12))],
    [sg.Multiline(key="log", size=(90, 5), disabled=True)],
    [sg.Text(lang["Text"][0]), sg.Input(key="listserverip"), sg.Button(lang["Button"][0],key="searchserver")],
    [sg.Text(lang["Text"][4]), sg.Input(key="mcid")],
    [sg.Text(lang["Text"][5]), sg.Input(key="motd")],
    [sg.Text(lang["Text"][1]), sg.Input(key="minecraftserverip"), sg.Button(lang["Button"][1],key="makeserver")],
    [sg.Button(lang["Button"][2], key="Quit")]
]

def gui_start():
    is_readonly = True
    is_minecraft_run = False
    if os.path.isfile("run"): os.remove("run")
    try:
        window = sg.Window("AllServer -Client-", main_layout, disable_close=True)
        while True:
            event, values = window.read(timeout=50)
            # ウィンドウの×ボタンクリックで終了
            if os.path.isfile("3141592653589793238") and is_readonly:
                window["serverlist"].update(disabled=False)
                window["log"].update(disabled=False)
                is_readonly = False
            if not os.path.isfile("run"):
                is_minecraft_run = False
            if event == "Quit" and not is_minecraft_run:
                break
            elif event == "Quit" and is_minecraft_run:
                sg.Popup(lang["ErrorMessage"][3], "Cant Quit")
            elif event == "searchserver":
                servers_str = ""
                result, servers = client.search_servers(values["listserverip"])
                if result == 0:
                    window["log"].print(lang["Message"][0])
                else:
                    window["log"].print(lang["Word"][7]+" : "+lang["ErrorMessage"][0])
                    continue
                servers_str = servers_str + lang["Word"][0] + ":" + str(len(servers)) + "\n"
                for i in servers:
                    servers_str = servers_str + lang["Word"][1] + ":" + i[0] + " IP:" + i[1] + " " + lang["Word"][2] + ":" + i[2] + " " + lang["Word"][3] + ":" + i[3] + " " + lang["Word"][4] + ":" + i[4] + "\n"
                window["serverlist"].update(servers_str)
            elif event == "makeserver" and not is_minecraft_run:
                if values["mcid"] == "":
                    continue
                thread = threading.Thread(target=client.start_server, args=(values["minecraftserverip"], values["motd"], values["mcid"], window))
                thread.start()
                is_minecraft_run = True
    except KeyboardInterrupt:
        return
    except:
        sg.PopupError(lang["Word"][7]+" : \n"+traceback.format_exc())

if __name__ == "__main__":
    gui_start()