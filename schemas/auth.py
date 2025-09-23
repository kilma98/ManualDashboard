from pydantic import BaseModel, constr


class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=100)
    password: constr(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: constr(min_length=3, max_length=100)
    password: constr(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



