import configparser, traceback, pickle, socket, check, time, etc, os

def is_socket_closed(sock):
    try:
        sock.fileno()
        return False
    except socket.error:
        return True

def search_servers(host : str, port = 50384, mode = "0", select_lang = ""):
    ini = configparser.ConfigParser()
    ini.read('config/basic.ini', 'UTF-8')
    servers = []
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        servers = pickle.loads(data)
    except:
        return 1, servers
    finally:
        client_socket.close()
    return 0, servers

def start_server(ip : str, motd : str, mcid : str, window, port = 50385):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lang = etc.load_lang()
    result = 0
    try:
        open("run", mode="w")
        client_socket.connect((ip, port))
        client_socket.sendall(f"{motd},{mcid}".encode('utf-8'))
        data = client_socket.recv(1024)
        if not data:
            window["log"].print(window["log"].print(lang["Word"][7]+" : "+lang["ErrorMessage"][1]))
            return 1
        server_version, server_port = data.decode("utf-8").split(",")
        window["log"].print("Wait",end="")
        while True:
            window["log"].print(".",end="")
            if check.network(ip, server_port):
                window["log"].print("OK")
                break
            time.sleep(2)
        if not server_port == "25565":
            window["log"].print(f"ServerIP : {ip}:{server_port}")
        else:
            window["log"].print(f"ServerIP : {ip}")
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
        if os.path.isfile("run"):
            os.remove("run")
    return result