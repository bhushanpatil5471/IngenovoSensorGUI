class SensorData:
    def __init__(self, sensorId, sensorType, labelsName, sensorStatus, signalStrength, temperatureValue, batteryStatus):
        self.sensorId = sensorId
        self.sensorType = sensorType
        self.labelsName = labelsName
        self.sensorStatus = sensorStatus
        self.signalStrength = signalStrength
        self.temperatureValue = temperatureValue
        self.batteryStatus = batteryStatus
