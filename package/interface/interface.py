import shlex
import inspect
from writer import write_message
from colorama import Fore, Style
from .constants import (
    AVAILABLE_COMMANDS,
    ERROR,
    EXITING_MESSAGE,
    INFO,
    INPUT_PROMPT,
    INVALID_INPUT,
    SELF_PARAM,
    UNKNOWN_COMMAND,
    InterfaceCommands,
)

class Interface:
    def __init__(self, commands: dict[str, callable]):
        self.__commands = commands

    def command_loop(self):
        while True:
            user_input = input(INPUT_PROMPT)
            normalized_input = user_input.strip().lower()
            
            if normalized_input in [InterfaceCommands.EXIT.value, InterfaceCommands.QUIT.value]:
                write_message(EXITING_MESSAGE, INFO)
                break
            if normalized_input == InterfaceCommands.HELP.value:
                self.__print_help()
                continue

            try:
                command_parts = shlex.split(user_input.strip())
            except ValueError as e:
                write_message(
                    INVALID_INPUT.format(error=e),
                    ERROR,
                )
                continue

            if not command_parts:
                continue

            command_name = command_parts[0]
            args = command_parts[1:]

            if command_name in self.__commands:
                try:
                    self.__commands[command_name](*args)
                except Exception as e:
                    write_message(e, ERROR)
            else:
                write_message(
                    UNKNOWN_COMMAND.format(command=command_name),
                    ERROR,
                )

    def __print_help(self):
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}"
            f"{AVAILABLE_COMMANDS}"
            f"{Style.RESET_ALL}\n"
        ]
        for name, func in self.__commands.items():
            sig = inspect.signature(func)
            params = [
                str(p) for p in sig.parameters.values()
                if p.name != SELF_PARAM
            ]
            command_line = f"{Fore.YELLOW}{name}{Fore.RESET}"
            if params:
                command_line += f" {Fore.MAGENTA}{' '.join(params)}{Fore.RESET}"
            lines.append(command_line)
        lines.append(f"{Fore.YELLOW}{InterfaceCommands.HELP.value}{Fore.RESET}")
        lines.append(
            f"{Fore.YELLOW}{InterfaceCommands.EXIT.value}{Fore.RESET}"
            f" | {Fore.YELLOW}{InterfaceCommands.QUIT.value}{Fore.RESET}"
        )
        print("\n".join(lines) + "\n")
