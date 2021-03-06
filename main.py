import uvicorn
from ControllerEndPoints import ProjectsController, LoginController
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from Constants import users
from Constants import Constants as consts
import requests
import json
from Service import DeviceDataService
from Utils import NewAccessToken as accessTkn

app = FastAPI()

app.include_router(ProjectsController.router)
# app.include_router(LoginController.login)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }
fake_users_db = users.users_db


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    # print('hashed password')
    # print(pwd_context.encrypt(plain_password))
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class Response(BaseModel):
    access_token: str
    token_type: Optional[str] = None
    status: Optional[str] = None


@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "status_code": status.HTTP_200_OK}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


def getFreshAccessToken():
    access_token = accessTkn.get_access_token()
    # f = open("cToken", "r")
    # existingToken = f.read()

    return access_token


@app.get("/Token/getAccessToken")
def accessTokenFunc(current_user: User = Depends(get_current_active_user)):
    return accessTkn.get_access_token()


@app.get('/Projects/getProjects')
def accessProjectsFunc(current_user: User = Depends(get_current_active_user)):
    access_token = getFreshAccessToken()
    obj = requests.get(
        url=consts.projects_url,
        headers={'Authorization': 'Bearer ' + access_token},
    ).json()
    return obj


@app.get('/Projects/getProjectDevices')
def accessProjectsDevicesFun(current_user: User = Depends(get_current_active_user)):
    access_token = getFreshAccessToken()
    try:
        obj = requests.get(
            url=consts.projects_devices_url,
            headers={'Authorization': 'Bearer ' + access_token},
        )

    except IOError as e:
        return "error in getting data"

    return DeviceDataService.sensorDataSegrigation(obj.text)


@app.get('/Projects/getProjectDeviceData/{deviceName}')
def accessProjectsDevicesFun(deviceName: str, current_user: User = Depends(get_current_active_user)):
    access_token = getFreshAccessToken()
    try:
        obj = requests.get(
            url=consts.device_data_url + deviceName,
            headers={'Authorization': 'Bearer ' + access_token},
        ).json()

    except IOError as e:
        return "error in getting data"

    return obj
