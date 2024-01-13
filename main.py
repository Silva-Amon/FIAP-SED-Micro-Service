from typing import List

from fastapi import FastAPI, HTTPException

from model.user import User
from config.mysql_config import database, users

app = FastAPI()


@app.get("/health-check")
async def health_check():
    return {"message": "Health check"}


@app.get("/users/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/user/", response_model=User)
async def create_user(user: User):
    query = users.insert().values(username=user.username, email=user.email,
                                  password=user.password, full_name=user.full_name)
    user_id = await database.execute(query)
    return {"id": user_id, **user.dict()}


@app.put("/user/{user_id}", response_model=User)
async def update_item(user_id: int, updated_user: User):
    query = users.update().where(users.c.id == user_id).values(
        username=updated_user.username, email=updated_user.email,
        password=updated_user.password, full_name=updated_user.full_name
    )
    await database.execute(query)
    return {"id": user_id, **updated_user.dict()}


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
