class Interface:
    # commands is a dictionary where the key is the command string
    # and the value is a callable (function) that executes the command
    def __init__(self, commands: dict[str, callable]):
        self.commands = commands

    # This method will continuously read user input and execute 
    # the corresponding command
    def command_loop(self):
        while True:
            user_input = input("Enter a command: ")
            if user_input in self.commands:
                self.commands[user_input]()
            else:
                print("Unknown command")
