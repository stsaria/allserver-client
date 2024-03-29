import configparser, traceback, pickle, socket, check, time, etc, os

# ose -> [--\~]

def is_socket_closed(sock):
    try:
        sock.fileno()
        return False
    except socket.error:
        return True

def search_servers(host : str, port = 50384, mode = "0", select_lang = ""):
    if len(host.split(":")) > 1:
        if host.split(":")[1].isdigit():
            port = int(host.split(":")[1])
            host = host.split(":")[0]
    ini = configparser.ConfigParser()
    ini.read('config/basic.ini', 'UTF-8')
    servers = []
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    try:      
        client_socket.connect((host, port))
        send_data = ","
        if mode[0] == "0":
            if select_lang == "":
                send_data = ini['lang']['lang']+"/"+ini['lang']['spare_lang']+send_data
            else:
                send_data = select_lang+"/"+select_lang+send_data
        send_data = "0,"+send_data
        client_socket.sendall(send_data.encode('utf-8'))
        data = client_socket.recv(1024)
        if int(data.decode('utf-8')) != 0:
            return 1, servers
        client_socket.sendall("next".encode())
        data = client_socket.recv(1024)
        # I used to use PICKLE a long time ago when sending server lists.
        # I'm sending it as a string right now (I really doubt that's a good idea).
        try:
            # New Protcol
            for server in data.decode("utf-8").split("\\"):
                servers.append(server.split(","))
            if len(servers) >= 1: servers.pop(-1)
        except:
            # Old Protcol
            servers = pickle.loads(data)
    except:
        return 1, servers
    finally:
        client_socket.close()
    return 0, servers

def start_server(host : str, motd : str, mcid : str, window, port = 50385):
    if len(host.split(":")) > 1:
        if host.split(":")[1].isdigit():
            port = int(host.split(":")[1])
            host = host.split(":")[0]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lang = etc.load_lang()
    result = 0
    try:
        open("nostop", mode="w")
        window["log"].print(lang["Message"][4])
        client_socket.connect((host, port))
        client_socket.sendall(f"{motd},{mcid}".encode('utf-8'))
        data = client_socket.recv(1024)
        if not data:
            window["log"].print(window["log"].print(lang["Word"][7]+" : "+lang["ErrorMessage"][1]))
            return 1
        server_version, server_port = data.decode("utf-8").split(",")
        window["log"].print("Wait",end="")
        while True:
            window["log"].print(".",end="")
            if check.network(host, server_port):
                window["log"].print("OK")
                break
            time.sleep(2)
        if server_port == "25565":
            window["log"].print(f"Serverhost : {host}")
        else:
            window["log"].print(f"Serverhost : {host}:{server_port}")
        window["log"].print(f"ServerVersion : {server_version}\n"+lang["Message"][3])
        data = client_socket.recv(1024)
        if int(data) == 0:
            window["log"].print(lang["Message"][1])
            result = 0
        else:
            window["log"].print(lang["Message"][2])
            result = 1
    except ConnectionRefusedError:
        window["log"].print(lang["Word"][7]+" : "+lang["ErrorMessage"][2])
        return 2
    except:
        window["log"].print(lang["Word"][7]+" : \n"+traceback.format_exc())
        return -1
    finally:
        if not is_socket_closed(client_socket):
            client_socket.close()
        if os.path.isfile("nostop"):
            os.remove("nostop")
    return result