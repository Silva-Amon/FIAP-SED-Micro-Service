from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
