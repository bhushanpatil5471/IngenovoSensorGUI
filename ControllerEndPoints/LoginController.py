from typing import Optional
from Entity import SensorDataObject
from Utils import NewAccessToken as accessTkn
from Constants import Constants as consts
import requests
from fastapi import APIRouter
from Utils import NewAccessToken
from Utils import extract
import threading as th
import json
from Service import loginService

login = APIRouter()
origins = ["*"]


@login.post('/login')
def accessProjectsFunc(userName: str, password: str):
    return loginService.loginAuth(userName, password)
