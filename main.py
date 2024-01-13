from fastapi import FastAPI, HTTPException

from model.user import User

app = FastAPI()

mock_users: list[User] = []


@app.get("/health-check")
async def health_check():
    return {"message": "Health check"}


@app.get("/user/{user_id}")
async def get_user(user_id: int) -> User:
    # Procurando user pelo id fornecido
    user = [user for user in mock_users if user.id == user_id]
    if user:
        return user[0]

    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/")
async def create_user(user: User) -> User:
    user_id = user.id
    user_ids = [u.id for u in mock_users]
    if user_id not in user_ids:
        mock_users.append(user)
        return user
    raise HTTPException(status_code=409, detail="User id already exist.")
