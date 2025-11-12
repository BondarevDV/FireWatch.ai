class InvalidFileTypeError(Exception):
    """Кастомное исключение для неверного типа файла."""
    def __init__(self, message: str = "CUSTOM Invalid file type. Please upload an image."):
        self.message = message
        super().__init__(self.message)