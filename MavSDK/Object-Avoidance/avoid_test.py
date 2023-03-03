#!/usr/bin/env python3

import os
import argparse
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
async def init_drone(sim):
    await util.start_connection(drone, sim)
    await util.check_status(drone)
    await util.setup_info(drone)

    # await util.define_geofence()
    # await util.calibrate_drone()
    # await tune_example.run()

# Initialize the drone and start a flight path 
async def main(sim):
    await init_drone(sim)
    f = await util.abs_altitude(drone)
    print("GPS Coordinates \n\tAltitude: "+str(util.absolute_altitude)+"\n\tLatitude: "+str(util.latitude)+"\n\tLongitude: "+str(util.longitude))

    #   Move drone using mavsdk commands   #
    await util.arm_drone(drone)
    # await util.print_all_params(drone)
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

# Launches ./mavsdk_server on port 50051 across the serial port, typically ttyACM0 on ubuntu
def launch_mavsdk():
    try:
        os.system("gnome-terminal -e 'bash -c \"./mavsdk_server -p 50051 serial:///dev/ttyACM0:921600; bash\" '")
    except:
        print("Server can't launch, check /dev/tty___ port used")


if __name__=="__main__":
    # Take arguments passed to program to see if simulation is run ('-s 1' runs sim)
    parser = argparse.ArgumentParser(description='Drone object avoidance in simulation or over pixhawk4.')
    parser.add_argument('-s', choices=['1','0'], help='Set flag as 1 or 0 to run simulation, default is 0.')
    args = parser.parse_args()
    sim = (args.s)
    print(sim)

    # Initilize the drone to look for the mav_sdk server on 'localhost':port 50051 
    #   If "--sim" is added when running program initiates simulator 
    if ( (sim == None) or (sim == '0') ):
        drone = System(mavsdk_server_address='localhost', port=50051)
        launch_mavsdk()
    else:
        drone = System()

    # Create Objects for use in scripts
    util = drone_util.util()
    flights = flight_tests.flights()

    # Run the asyncio loop
    asyncio.run(main(sim))