import uuid

import uvicorn
from fastapi import FastAPI, status, HTTPException

from app.database.database import engine, Base, async_session
from app.database.user_dal import UserDAL
from app.models.user import User

app = FastAPI()

EXCEPTION_USER_NOT_FOUND = HTTPException(status_code=404, detail="User not found")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def health_check():
    return {"message": "Health check"}


@app.get("/users/", status_code=status.HTTP_200_OK)
async def get_users():
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_all()


@app.get(
    "/user/{user_id}",
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: str):
    try:
        uuid.UUID(user_id)
    except ValueError:
        raise EXCEPTION_USER_NOT_FOUND

    async with async_session() as session:
        async with session.begin():

            user_dal = UserDAL(session)
            user = await user_dal.get(user_id)
            if user is None:
                raise EXCEPTION_USER_NOT_FOUND

            user.password = '******'

            return user


@app.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(
    name: str,
    username: str,
    email: str,
    password: str
):
    user = User(
        name=name,
        username=username,
        email=email,
        password=password
    )

    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            exists_email = await user_dal.get_by_email(email)
            if exists_email is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

            await user_dal.create(user)
            return {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "email": user.email
            }


@app.patch(
    "/user/{user_id}",
    status_code=status.HTTP_202_ACCEPTED
)
async def update_user(
        user_id: str,
        name: str,
        username: str,
        email: str
):
    try:
        uuid.UUID(user_id)
    except ValueError:
        raise EXCEPTION_USER_NOT_FOUND

    user_update = User(
        id=user_id,
        name=name,
        username=username,
        email=email
    )

    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)

            if await user_dal.get(user_update.id) is None:
                raise EXCEPTION_USER_NOT_FOUND
            await user_dal.update(user_update)
            return {
                "id": user_id,
                "name": name,
                "username": username,
                "email": email
            }


@app.delete(
    "/user/{user_id}",
    status_code=status.HTTP_200_OK
)
async def delete_user(user_id: str):
    try:
        uuid.UUID(user_id)
    except ValueError:
        raise EXCEPTION_USER_NOT_FOUND

    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            await user_dal.delete(user_id)
            return {"message": "User deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
