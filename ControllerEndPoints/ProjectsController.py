from typing import Optional

import main
from Entity import SensorDataObject
from Utils import NewAccessToken as accessTkn
from Constants import Constants as consts
import requests
from fastapi import APIRouter, Depends
from Utils import NewAccessToken
from Utils import extract
import threading as th
import json
from Service import DeviceDataService
import main

router = APIRouter()
origins = ["*"]


# def getFreshAccessToken():
#     access_token = accessTkn.get_access_token()
#
#     return access_token
#
#
# def startRepeat():
#     th.Timer(3600, startRepeat()).start()
#     print("hello")
#
#
# @router.get("/getAccessToken")
# def accessTokenFunc():
#     return NewAccessToken.get_access_token()
#
#
# @router.get('/getProjects')
# def accessProjectsFunc():
#     access_token = getFreshAccessToken()
#     obj = requests.get(
#         url=consts.projects_url,
#         headers={'Authorization': 'Bearer ' + access_token},
#     ).json()
#     return obj
#
#
# @router.get('/getProjectDevices')
# def accessProjectsDevicesFun():
#     access_token = getFreshAccessToken()
#     try:
#         obj = requests.get(
#             url=consts.projects_devices_url,
#             headers={'Authorization': 'Bearer ' + access_token},
#         )
#
#     except IOError as e:
#         return "error in getting data"
#
#     return DeviceDataService.sensorDataSegrigation(obj.text)
#
#
# @router.get('/getProjectDeviceData/{deviceName}')
# def accessProjectsDevicesFun(deviceName: str):
#     access_token = getFreshAccessToken()
#     try:
#         obj = requests.get(
#             url=consts.device_data_url + deviceName,
#             headers={'Authorization': 'Bearer ' + access_token},
#         ).json()
#
#     except IOError as e:
#         return "error in getting data"
#
#     return obj

