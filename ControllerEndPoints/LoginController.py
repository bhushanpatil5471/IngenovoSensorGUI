from fastapi import APIRouter
from Service import loginService

login = APIRouter()
origins = ["*"]


@login.post('/login')
def accessProjectsFunc(userName: str, password: str):

    return loginService.loginAuth(userName, password)

