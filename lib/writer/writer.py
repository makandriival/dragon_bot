from colorama import Fore


# This function is used to write messages to the console 
# with different colors based on the type of message 
# (info, warning, error).
def write_message(message: str, type: str = "info"):
    if type == "info":
        print(Fore.GREEN + message + Fore.RESET)
    elif type == "warning":
        print(Fore.YELLOW + message + Fore.RESET)
    elif type == "error":
        print(Fore.RED + message + Fore.RESET)
    else:
        print(message)