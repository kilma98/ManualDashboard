from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


