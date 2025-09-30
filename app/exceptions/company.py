class CompanyNotFoundException(Exception):
    def __init__(self) -> None:
        self.message = "Company not found"
        super().__init__(self.message)
        
class CompanyAlreadyExistsException(Exception):
    def __init__(self) -> None:
        self.message = "This company already exists"
        super().__init__(self.message)