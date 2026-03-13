import shlex
import inspect
from writer import write_message
from colorama import Fore, Style


class Interface:
    def __init__(self, commands: dict[str, callable]):
        self.__commands = commands

    def command_loop(self):
        while True:
            user_input = input("Enter command: ")
            if user_input.lower() in ["exit", "quit"]:
                write_message("Exiting...", "info")
                break

            try:
                command_parts = shlex.split(user_input)
            except ValueError as e:
                write_message(f"Invalid input: {e}", "error")
                continue

            if not command_parts:
                continue

            command_name = command_parts[0]
            args = command_parts[1:]

            if command_name == "help":
                self.__print_help()
            elif command_name in self.__commands:
                try:
                    self.__commands[command_name](*args)
                except Exception as e:
                    write_message(e, "error")
            else:
                write_message(f"Unknown command: {command_name}", "error")

    def __print_help(self):
        lines = [f"{Fore.CYAN}{Style.BRIGHT}Available Commands:{Style.RESET_ALL}\n"]
        for name, func in self.__commands.items():
            sig = inspect.signature(func)
            params = [
                str(p) for p in sig.parameters.values()
                if p.name != "self"
            ]
            command_line = f"{Fore.YELLOW}{name}{Fore.RESET}"
            if params:
                command_line += f" {Fore.MAGENTA}{' '.join(params)}{Fore.RESET}"
            lines.append(command_line)
        lines.append(f"{Fore.YELLOW}help{Fore.RESET}")
        lines.append(f"{Fore.YELLOW}exit{Fore.RESET} | {Fore.YELLOW}quit{Fore.RESET}")
        print("\n".join(lines) + "\n")
