from enum import Enum


class InterfaceCommands(Enum):
    EXIT = "exit"
    QUIT = "quit"
    HELP = "help"


INPUT_PROMPT = "Enter command: "
INFO = "info"
ERROR = "error"
EXITING_MESSAGE = "Exiting..."
INVALID_INPUT = "Invalid input: {error}"
UNKNOWN_COMMAND = "Unknown command: {command}"
AVAILABLE_COMMANDS = "Available Commands:"
SELF_PARAM = "self"
