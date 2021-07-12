from typing import Optional
from fastapi import FastAPI
import uvicorn

from ControllerEndPoints.ProjectsController import origins
from Utils import NewAccessToken
from ControllerEndPoints import ProjectsController, LoginController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(ProjectsController.router)
app.include_router(LoginController.login)

origins = [
    "http://localhost:4200",
    "http://localhost:8080",
    "*"
]

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
