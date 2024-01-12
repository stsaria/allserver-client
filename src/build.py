import subprocess, platform, shutil, os

user_use_platform = platform.system()
os_name = ""

if user_use_platform == "Windows":
    os_name = "win"
else:
    os_name = "unix"

make_list = ["lang?dir", "config?dir", "README.md?file", "detailed-manual"]

def copy_need_file():
    for i in make_list: 
        if "?dir" in i:
            shutil.copytree(i.split("?")[0], f"bin/{os_name}/"+i.split("?")[0])
        elif "?file" in i:
            shutil.copy(i.split("?")[0], f"bin/{os_name}/"+i.split("?")[0])

def pyinstall():
    user_use_platform = platform.system()
    os.makedirs("bin", exist_ok=True)
    subprocess.run(f"pyinstaller src/allserver.py --onefile --distpath=bin/{os_name} --uac-admin", shell=True)
def install():
    user_use_platform = platform.system()
    architecture_name = ""
    if os.path.isdir("bin"): shutil.rmtree("bin")
    pyinstall()
    copy_need_file()
    if user_use_platform == "Windows":
        architecture_name = platform.machine().lower()
        shutil.make_archive(f"allserver-win-{architecture_name}-bin", 'zip', root_dir='./bin/win')
    else:
        architecture_name = os.uname().machine
        shutil.make_archive(f"allserver-unix-{architecture_name}-bin", 'gztar', root_dir='./bin/unix')
