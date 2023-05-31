import importlib
import platform
import subprocess

def check_and_install(module):
    try:
        importlib.import_module(module)
        #print(f"Modulul '{module}' este deja instalat.")
    except ImportError:
        #print(f"Modulul '{module}' nu este instalat. Se instalează...")
        subprocess.check_call(["pip", "install", module])
        #print(f"Modulul '{module}' a fost instalat.")
    finally:
        globals()[module] = importlib.import_module(module)
        #importlib.import_module(module)
        #print(f"Modulul '{module}' este importat.")

def check_win_install(module, as_name):
    if platform.system() == "Windows":
        try:
            globals()[as_name] = importlib.import_module(module)
            #print(f"Modulul '{module}' este deja instalat.")
        except ImportError:
            #print(f"Modulul '{module}' nu este instalat. Se instalează...")
            subprocess.check_call(["pip", "install", module])
            globals()[as_name] = importlib.import_module(module)
            #print(f"Modulul '{module}' a fost instalat.")
        finally:
            pass
            #print(f"Modulul '{module}' este importat ca '{as_name}'.")
    else:
        check_and_install(as_name)
