class PortAlreadyInUseException(Exception):
    def __init__(self, port: int):
        self.port = port
        self.message = f"Port {self.port} already in use"
        super().__init__(self.message)