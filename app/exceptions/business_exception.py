class BusinessException(Exception):
    def __init__(self, field: str, message: str, row: int | None = None):
        self.field = field
        self.message = message
        self.row = row
        super().__init__(message)
