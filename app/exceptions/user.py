class UserNotFoundException(Exception):
    def __init__(self) -> None:
        self.message = "User not found!"
        super().__init__(self.message)
        
class UserInvalidBirthdayException(Exception):
    def __init__(self) -> None:
        self.message = "Birthday cannot be in the future."
        super().__init__(self.message)