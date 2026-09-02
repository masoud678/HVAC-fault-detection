supply_air_temperature = 25
setpoint = 14
outdoor_air_temperature = 20

difference = supply_air_temperature - setpoint

print("HVAC Fault Detection")
print("--------------------")
print(f"Supply Air Temperature: {supply_air_temperature}°C")
print(f"Setpoint: {setpoint}°C")
print(f"Outdoor Air Temperature: {outdoor_air_temperature}°C")
print(f"Temperature Difference: {difference}°C")

if outdoor_air_temperature > 25 and difference > 5:
    print("FAULT: Possible Cooling Failure")

elif difference <= 3:
    print("System Status: Normal")

elif difference <= 5:
    print("WARNING: Temperature Deviation")

else:
    print("WARNING: Temperature Deviation")