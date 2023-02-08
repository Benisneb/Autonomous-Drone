#!/usr/bin/env python3
import asyncio  
from mavsdk import System
    # Asyncio allows for near concurrent processing 
    # Mavsdk interacts with the drone through serial port (USB0)
    
# Connect to the drone by serial / tcp / udp 
# Check the status of the drone is connected 
async def start_connection():
    # await drone.connect(system_address="serial:///dev/ttyUSB0:921600")
    await drone.connect(system_address="udp://:14540")
    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break


# Called when the drone needs to check connection / telemetry / health           
async def check_status():
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break


# Print the values of the telemetry status and throw exception for errors
async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return

    
# Arm the drone if status check passed, generate path
# Lift up and verify surroundings clear
async def takeoff():
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)

    print("-- Landing")
    await drone.action.land()

    status_text_task.cancel()

# Call dron functions
async def main():
    await start_connection()
    await check_status()
    await takeoff()

if __name__=="__main__":
    drone = System()
    status_text_task = ""
    # Run the asyncio loop
    asyncio.run(main())