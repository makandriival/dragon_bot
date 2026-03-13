import shlex
import inspect
import difflib
from typing import Callable
try:
    import gnureadline as readline
except ImportError:
    try:
        import readline
    except ImportError:
        readline = None
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion
except ImportError:
    PromptSession = None
    Completer = object
    Completion = None
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
from contacts.contacts import contacts


class _CommandCompleter(Completer):
    def __init__(self, commands_getter, usage_getter):
        self._commands_getter = commands_getter
        self._usage_getter = usage_getter

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        current_word = document.get_word_before_cursor(WORD=True)
        parts = text_before_cursor.split()

        if len(parts) <= 1 and not text_before_cursor.endswith(" "):
            options = self._commands_getter(current_word)
        else:
            options = self._commands_getter(current_word, contacts_only=True)

        if Completion is None:
            return

        for option in options:
            yield Completion(
                option,
                start_position=-len(current_word),
                display_meta=self._usage_getter(option),
            )

class Interface:
    def __init__(self, commands: dict[str, Callable]):
        self.__commands = commands
        self.__command_usages = self.__build_command_usages()
        self.__setup_readline()
        self.__prompt_session = self.__setup_prompt_session()

    def __build_usage_from_signature(self, command_name: str, func: Callable):
        sig = inspect.signature(func)
        params = [p for p in sig.parameters.values() if p.name != SELF_PARAM]
        if not params:
            return command_name

        parts = []
        for param in params:
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                parts.append(f"<{param.name}...>")
            elif param.default is inspect.Parameter.empty:
                parts.append(f"<{param.name}>")
            else:
                parts.append(f"[{param.name}]")
        return f"{command_name} {' '.join(parts)}"

    def __build_command_usages(self):
        usages = {
            InterfaceCommands.HELP.value: InterfaceCommands.HELP.value,
            InterfaceCommands.EXIT.value: InterfaceCommands.EXIT.value,
            InterfaceCommands.QUIT.value: InterfaceCommands.QUIT.value,
        }
        for name, func in self.__commands.items():
            usages[name] = self.__build_usage_from_signature(name, func)
        return usages

    def __get_command_usage(self, command_name: str):
        return self.__command_usages.get(command_name, command_name)

    def __setup_prompt_session(self):
        if PromptSession is None:
            return None
        return PromptSession(
            completer=_CommandCompleter(
                self.__get_completion_options,
                self.__get_command_usage,
            ),
            complete_while_typing=True,
        )

    def __get_completion_options(self, text: str, contacts_only: bool = False):
        if contacts_only:
            options = [name for name in contacts.data if name.startswith(text)]
            if not options and text:
                options = difflib.get_close_matches(text, list(contacts.data.keys()), n=3, cutoff=0.4)
            return options

        all_commands = list(self.__commands.keys()) + [c.value for c in InterfaceCommands]
        options = [cmd for cmd in all_commands if cmd.startswith(text)]
        if not options and text:
            options = difflib.get_close_matches(text, all_commands, n=3, cutoff=0.4)
        return options

    def __setup_readline(self):
        if readline is None:
            return
        if "libedit" in (readline.__doc__ or ""):
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.set_completer(self.__completer)
        readline.set_completer_delims(" \t\n")

    def __completer(self, text, state):
        if readline is None:
            return None
        buffer = readline.get_line_buffer()
        parts = buffer.split()

        if len(parts) <= 1:
            options = self.__get_completion_options(text)
        else:
            options = self.__get_completion_options(text, contacts_only=True)
        try:
            return options[state]
        except IndexError:
            return None

    def command_loop(self):
        while True:
            try:
                if self.__prompt_session is not None:
                    user_input = self.__prompt_session.prompt(INPUT_PROMPT)
                else:
                    user_input = input(INPUT_PROMPT)
            except KeyboardInterrupt:
                write_message("Exiting by user...", INFO)
                break

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
                write_message(INVALID_INPUT.format(error=e), ERROR)
                continue

            if not command_parts:
                continue

            command_name = command_parts[0]
            args = command_parts[1:]

            if command_name in self.__commands:
                command_func = self.__commands[command_name]
                try:
                    inspect.signature(command_func).bind(*args)
                except TypeError:
                    write_message(
                        f"Expected format: {self.__get_command_usage(command_name)}",
                        ERROR,
                    )
                    continue
                try:
                    command_func(*args)
                except Exception as e:
                    write_message(str(e), ERROR)
            else:
                write_message(UNKNOWN_COMMAND.format(command=command_name), ERROR)

    def __print_help(self):
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}"
            f"{AVAILABLE_COMMANDS}"
            f"{Style.RESET_ALL}\n"
        ]
        for name, func in self.__commands.items():
            usage = self.__build_usage_from_signature(name, func)
            command_line = f"{Fore.YELLOW}{name}{Fore.RESET}"
            if usage != name:
                command_line += f" {Fore.MAGENTA}{usage[len(name) + 1:]}{Fore.RESET}"
            lines.append(command_line)
        lines.append(f"{Fore.YELLOW}{InterfaceCommands.HELP.value}{Fore.RESET}")
        lines.append(
            f"{Fore.YELLOW}{InterfaceCommands.EXIT.value}{Fore.RESET} | "
            f"{Fore.YELLOW}{InterfaceCommands.QUIT.value}{Fore.RESET}"
        )
        print("\n".join(lines) + "\n")
