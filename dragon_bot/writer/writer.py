from colorama import Fore


# This function is used to write messages to the console
# with different colors based on the type of message
# (info, warning, error).
def write_message(message: str, msg_type: str = "info"):
    if msg_type == "info":
        print(Fore.GREEN + str(message) + Fore.RESET)
    elif msg_type == "warning":
        print(Fore.YELLOW + str(message) + Fore.RESET)
    elif msg_type == "error":
        print(Fore.RED + str(message) + Fore.RESET)
    else:
        print(str(message))
