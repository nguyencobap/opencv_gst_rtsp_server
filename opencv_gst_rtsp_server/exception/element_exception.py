class ElementNotFoundException(Exception):
    def __init__(self, element_name: str):
        self.element_name = element_name
        self.message = f"Element {self.element_name} not found"
        super().__init__(self.message)