class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        print("Called")
        self.username = username
        self.message = f"User '{username}' already exists."
        super().__init__(self.message)
        
class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Invalid username or password"
        super().__init__(self.message)
        
class TokenCredentialsException(Exception):
    def __init__(self):
        self.message = "Could not validate credentials"
        super().__init__(self.message)