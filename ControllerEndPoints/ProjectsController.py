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
from Service import DeviceDataService


router = APIRouter()
origins = ["*"]


def getFreshAccessToken():
    access_token = accessTkn.get_access_token()

    return access_token


def startRepeat():
    th.Timer(3600, startRepeat()).start()
    print("hello")


@router.get("/getAccessToken")
def accessTokenFunc():
    return NewAccessToken.get_access_token()


@router.get('/getProjects')
def accessProjectsFunc():
    access_token = getFreshAccessToken()
    obj = requests.get(
        url=consts.projects_url,
        headers={'Authorization': 'Bearer ' + access_token},
    ).json()
    return obj


@router.get('/getProjectDevices')
def accessProjectsDevicesFun():
    access_token = getFreshAccessToken()
    try:
        obj = requests.get(
            url=consts.projects_devices_url,
            headers={'Authorization': 'Bearer ' + access_token},
        )

    except IOError as e:
        return "error in getting data"

    return DeviceDataService.sensorDataSegrigation(obj.text)


@router.get('/getProjectDeviceData/{deviceName}')
def accessProjectsDevicesFun(deviceName: str):
    access_token = getFreshAccessToken()
    try:
        obj = requests.get(
            url=consts.device_data_url + deviceName,
            headers={'Authorization': 'Bearer ' + access_token},
        ).json()

    except IOError as e:
        return "error in getting data"

    return obj


@router.get('/getDevicesDataWithData')
def accessProjectsDevicesFun():
    access_token = getFreshAccessToken()
    try:
        obj = requests.get(
            url=consts.projects_devices_url,
            headers={'Authorization': 'Bearer ' + access_token},
        ).json()
    except IOError as e:
        return "error in getting data" + e

    # allDeviceData = json.loads(obj)

    device_names = extract.json_extract(obj, 'name')[1::2]
    device_identifiers = extract.json_extract(obj, 'name')[::2]

    sensorList = []

    for idD in device_identifiers:
        device_identifier = idD.split("/")[-1]
        # print(device_identifier)
        device_data = requests.get(
            url=consts.device_data_url + device_identifier,
            headers={'Authorization': 'Bearer ' + access_token}
        )

        # Data scraping starts here --------------------------------------
        mainData = json.loads(device_data.text)
        # general Data
        MD_name = mainData['name']
        MD_sensortype = mainData['type']

        # lable Data
        MD_labels = mainData['labels']
        MD_L_lableName = MD_labels['name']
        MD_L_lablevirtualSensor = MD_labels['virtual-sensor']

        # reported obj starts-here ------
        reportedData = mainData['reported']

        # networkStatus nested in reported starts here------
        reportedNetworkStatus = reportedData['networkStatus']
        RNS_SignalStrength = reportedNetworkStatus['signalStrength']
        RNS_rssi = reportedNetworkStatus['rssi']
        RNS_updateTime = reportedNetworkStatus['updateTime']
        RNS_transmissionMode = reportedNetworkStatus['transmissionMode']

        # cloudConnectors nested in networkStatus nested in reported starts here------
        cloudConnectorsArray = reportedNetworkStatus['cloudConnectors']
        cloudConnectors = cloudConnectorsArray[0]
        RNS_CC_id = cloudConnectors['id']
        RNS_CC_signalStrength = cloudConnectors['signalStrength']
        RNS_CC_rssi = cloudConnectors['rssi']

        # batteryStatus nested in reported starts here------
        batteryStatus = reportedData['batteryStatus']

        # temperature nested in reported starts here------
        reportedTemperature = reportedData['temperature']

        # data under temperature nested in reported starts here------
        RT_value = reportedTemperature['value']
        RT_updateTime = reportedTemperature['updateTime']
        RT_samplesArray = reportedTemperature['samples']
        RT_samples = RT_samplesArray[0]

        # data under samples in temperature nested in reported starts here------
        RT_S_value = RT_samples['value']
        RT_S_sampleTime = RT_samples['sampleTime']

        # touch nested in reported starts here------
        touch = reportedData['touch']
        # Data scraping ends here--------------------------------------

        # sensorObj = SensorDataObject.SensorDataObject()
        # sensorObj(sensorId, 'sensorType', 'labelsName', 'sensorStatus', 'signalStrength','temperatureValue', 'batteryStatus')
        # sensorList.append(sensorObj)
        thisDict = {
            "MD_name": MD_name,
            "MD_SensonId": device_identifier,
            "MD_sensortype": MD_sensortype,
            "MD_L_lableName": MD_L_lableName,
            "MD_L_lablevirtualSensor": MD_L_lablevirtualSensor,
            "RNS_SignalStrength": RNS_SignalStrength,
            "RNS_rssi": RNS_rssi,
            "RNS_updateTime": RNS_updateTime,
            "RNS_transmissionMode": RNS_transmissionMode,
            "RNS_CC_id": RNS_CC_id,
            "RNS_CC_signalStrength": RNS_CC_signalStrength,
            "RNS_CC_rssi": RNS_CC_rssi,
            "RT_value": RT_value,
            "RT_updateTime": RT_updateTime,
            "RT_S_value": RT_S_value,
            "RT_S_sampleTime": RT_S_sampleTime,
            "touch": touch,
        }

        sensorList.append(thisDict)
    return sensorList
