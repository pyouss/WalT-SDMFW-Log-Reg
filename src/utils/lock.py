import os
from utils.routes import ROOT_DIR 

def is_locked():
    return os.path.exists("{ROOT_DIR}/.lock")

def lock_modifications():
    if not os.path.exists("{ROOT_DIR}/.lock"):
        with open(".lock", 'w') as f:
            pass
    print(f"The config files are currently locked and cannot be modified until ./experiment is executed.")
    print(f"Alternatively, you can unlock the files by running ./configure unlock.")

def unlock_modifications():
    if os.path.exists(".lock"):
        os.remove('.lock')
    print(f"The config files are now unlocked.")
    print("./experiment command can not be executed until config files are locked.")
    print("The modifications get locked when you send the configurations with :")
    print("\tUse `./configure send` to send the configurations to nodes.")
    print("\tThis will lock the modifications")

