#!/usr/bin/env python3

import asyncio
import drone_util
import flight_tests
import tune_example

from mavsdk import System
    # Asyncio allows for near concurrent processing 
    # Mavsdk interacts with the drone through serial port USB0/1 or ACM0/1 
    # Mavsdk.offboard allows manual altitude/thrust/tilt/GPS
    

# Basic setup before flight can happen 
# Connect to drone
async def init_drone():
    await util.start_connection(drone)
    await util.check_status(drone)
    await util.setup_info(drone)

    # await util.define_geofence()
    # await util.calibrate_drone()
    # await tune_example.run()

# Initialize the drone and start a flight path 
async def main():
    await init_drone()
    await util.arm_drone(drone)

    #   Move drone using mavsdk commands   #
    await flights.takeoff(drone, util)
    await asyncio.sleep(10)
    # await flights.altitude_control(drone, util)
    # await asyncio.sleep(10)
    # await flights.GPS_control(drone, util)
    # await asyncio.sleep(10)
    # await flights.velocity_control(drone, util)
    # await asyncio.sleep(10)
    # await flights.schedule_mission(drone, util)
    # await flights.qgroundcontrol_mission(drone, util)


if __name__=="__main__":
    # Create Objects for use in scripts
    drone = System()
    util = drone_util.util()
    flights = flight_tests.flights()

    # Run the asyncio loop
    asyncio.run(main())