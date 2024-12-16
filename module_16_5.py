from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
app = FastAPI()
users = []

valid_username = Annotated[str, Path(min_length=3, max_length=20, description="Enter a name", example="Max")]
valid_age = Annotated[int, Path(ge=18, le=123, description="Enter age", example=19)]
valid_id = Annotated[int, Path(ge=0, le=1000, description="Enter id", example=2)]


class User(BaseModel):
    id: valid_id
    username: valid_username
    age: valid_id

@app.get("/")
async def get_message(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users", response_model=List[User])
async def get_user():
    return users

@app.get('/user/{user_id}', response_model=User)
async def create_message (request: Request, user_id: valid_id) -> HTMLResponse:

    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})

    raise HTTPException(status_code=404, detail="Message not found")




@app.post('/user/{username}/{age}', response_model=User)
async def create_user(username: valid_username, age: valid_age):
    try:
        id = users[-1].id + 1
    except:
        id = 1

    user = User(id=id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: valid_id, username: valid_username, age: valid_age):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail="User was not found" )

@app.delete('/user/{user_id}', response_model=User)
async def del_user(user_id: valid_id):
    for __id, user in enumerate(users):
        if user.id == user_id:
            users.pop(__id)
            return user
    raise HTTPException(status_code=404, detail="User was not found")