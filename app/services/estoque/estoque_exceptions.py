from app.common.exceptions import ConflictException

class EstoqueAlreadyExistsException(ConflictException):
    def __init__(self):
        details = [
            {
                "message": "Estoque já existe",
                "slug": "codigo-xxx-yyy",
            }
        ]
        super().__init__(details)

class EstoqueNotFoundException(ConflictException):
    def __init__(self):
        details = [
            {
                "message": "Estoque não encontrado",
                "slug": "codigo-xxx-yyy",
            }
        ]
        super().__init__(details)