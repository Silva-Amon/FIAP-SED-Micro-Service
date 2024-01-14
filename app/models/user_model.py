from pydantic import BaseModel

from app.database.user import User


class CreateUserModel(BaseModel):
    name: str
    username: str
    email: str
    password: str

    def to_user(self):
        return User(
            name=self.name,
            username=self.username,
            email=self.email,
            password=self.password
        )
