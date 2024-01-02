import sys, os

if "src" in os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0]))).replace("\\", "/").split("/") and os.getcwd().replace("\\", "/").split("/")[-1] == "src":
    os.chdir('../')
elif not "src" in os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0]))):
    os.chdir(os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0]))))
else:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '..')))

import check, gui

def main():
    result = check.check()
    if result != 0:
        return 1
    
    gui.gui_start()

if __name__ == "__main__":
    main()