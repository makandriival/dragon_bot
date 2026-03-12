class NotEnoughArgumentsError(Exception):
    def __init__(
            self,
            message="Not enough arguments provided for the command."):
        self.message = message
        super().__init__(self.message)


class InvalidCommandError(Exception):
    def __init__(
            self,
            message="Invalid command. Please check the command and try"
            " again."):
        self.message = message
        super().__init__(self.message)


class NoteNotFoundError(Exception):
    def __init__(
            self,
            message="Note not found. Please check the index and try again."):
        self.message = message
        super().__init__(self.message)


class ContactNotFoundError(Exception):
    def __init__(
            self,
            message="Contact not found. Please check the name and try again."):
        self.message = message
        super().__init__(self.message)


class InvalidEmailError(Exception):
    def __init__(
            self,
            message="Invalid email format. Please provide a valid email"
            " address."):
        self.message = message
        super().__init__(self.message)


class DuplicateContactError(Exception):
    def __init__(
            self,
            message="Contact already exists. Please check the name and try"
            " again."):
        self.message = message
        super().__init__(self.message)


class InvalidPhoneNumberError(Exception):
    def __init__(
            self,
            message="Invalid phone number format. Please provide a"
            " valid phone number."):
        self.message = message
        super().__init__(self.message)


class InvalidDateError(Exception):
    def __init__(
            self,
            message="Invalid date format. Please provide a valid date"
            " (DD.MM.YYYY)."):
        self.message = message
        super().__init__(self.message)
