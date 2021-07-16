import json
from Entity import SensorDataObject
from datetime import datetime as dt
import dateutil.parser


def sensorDataSegrigation(rawdata):
    allMainData = json.loads(rawdata)
    AMD_devices = allMainData['devices']
    sensorList = []
    for mainData in AMD_devices:
        # print(mainData)
        # Data scraping starts here --------------------------------------
        # mainData = json.loads(device_data.text)
        # general Data
        MD_name = mainData['name']
        device_identifier = MD_name.split("/")[-1]
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
        RT_updateTimeDefault = reportedTemperature['updateTime']
        yourdate = dateutil.parser.parse(RT_updateTimeDefault)
        RT_updateTime = dt.strftime(yourdate, '%d/%m/%Y %H:%M:%S')

        RT_samplesArray = reportedTemperature['samples']
        RT_samples = RT_samplesArray[0]

        # data under samples in temperature nested in reported starts here------
        RT_S_value = RT_samples['value']
        RT_S_sampleTime = RT_samples['sampleTime']

        # touch nested in reported starts here------
        touch = reportedData['touch']
        # Data scraping ends here--------------------------------------

        # # sensorObj = SensorDataObject.SensorData()
        # sensorObj=SensorDataObject.SensorData(device_identifier, 'sensorType', 'labelsName', 'sensorStatus', 'signalStrength','temperatureValue', 'batteryStatus')
        # sensorList.append(sensorObj)

        thisDict = {
            "MD_name": MD_name,
            "MD_SensorId": device_identifier,
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
            "touch": touch
        }

        sensorList.append(thisDict)

    return sensorList
