from writer import write_message


class Interface:
    def __init__(self, commands: dict[str, callable]):
        self.__commands = commands

    def command_loop(self):
        while True:
            user_input = input("Enter command: ")
            if user_input.lower() in ["exit", "quit"]:
                write_message("Exiting...", "info")
                break

            command_parts = user_input.split()
            if not command_parts:
                continue

            command_name = command_parts[0]
            args = command_parts[1:]

            if command_name in self.__commands:
                try:
                    self.__commands[command_name](*args)
                except Exception as e:
                    write_message(e, "error")
            else:
                write_message(f"Unknown command: {command_name}", "error")
