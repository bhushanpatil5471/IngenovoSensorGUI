from typing import Optional
from fastapi import FastAPI

from ControllerEndPoints.ProjectsController import origins
from Utils import NewAccessToken
from ControllerEndPoints import ProjectsController, LoginController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(ProjectsController.router)
app.include_router(LoginController.login)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
