supply_air_temperature = 100
setpoint = 14
outdoor_air_temperature = 20
cooling_command = 100


def validate_supply_air_temperature(supply_air_temperature):
    if supply_air_temperature < -20 or supply_air_temperature > 60:
        return "SENSOR FAULT: Invalid Supply Air Temperature"

    return "SENSOR STATUS: Valid"


def detect_cooling_fault(supply_air_temperature, setpoint, cooling_command):

    sensor_status = validate_supply_air_temperature(
        supply_air_temperature
    )

    if sensor_status != "SENSOR STATUS: Valid":
        return sensor_status

    difference = supply_air_temperature - setpoint

    if cooling_command >= 80 and difference > 8:
        return "SEVERE FAULT: Major Cooling Performance Failure"

    elif cooling_command >= 80 and difference > 5:
        return "MODERATE FAULT: Cooling Performance Issue"

    elif difference <= 3:
        return "NORMAL: System Operating Normally"

    elif difference <= 5:
        return "WARNING: Temperature Deviation"

    else:
        return "WARNING: Temperature Deviation"


result = detect_cooling_fault(
    supply_air_temperature,
    setpoint,
    cooling_command
)


print("HVAC Fault Detection")
print("--------------------")
print(f"Supply Air Temperature: {supply_air_temperature}°C")
print(f"Setpoint: {setpoint}°C")
print(f"Outdoor Air Temperature: {outdoor_air_temperature}°C")

difference = supply_air_temperature - setpoint
print(f"Temperature Difference: {difference}°C")

print(result)