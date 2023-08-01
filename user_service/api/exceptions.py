from fastapi import HTTPException
from starlette import status


class UserAlreadyExistsException(HTTPException):
    def __init__(self, email):
        detail = f"Пользователь с email '{email}' уже зарегистрирован."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        detail = "Неверные учетные данные"
        headers = {"WWW-Authenticate": "Basic"}
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)
