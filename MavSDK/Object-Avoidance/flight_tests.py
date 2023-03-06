#!/usr/bin/env python3

import asyncio

import drone_util

from mavsdk.mission import (MissionItem, MissionPlan) # Mission planning for control
from mavsdk.offboard import (Attitude, OffboardError) # Altitude Control
from mavsdk.offboard import (OffboardError, PositionNedYaw) # GPS Control
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed) # Velocity Control
from mavsdk.offboard import (OffboardError, VelocityNedYaw) # GPS & Velocity Control
    # Asyncio allows for near concurrent processing 
    # Mavsdk interacts with the drone through serial port USB0/1 or ACM0/1 
    # Mavsdk.offboard allows manual altitude/thrust/tilt/GPS

class flights():
    def __init__(self):
        pass

    # Arm the drone if status check passed, generate path
    # Lift up and verify surroundings clear
    async def takeoff(self, drone, util):

        print("-- Taking off")
        # await drone.action.set_takeoff_altitude(6)
        # await drone.action.takeoff()

        await asyncio.sleep(10)
        await util.arm_drone(drone)

        print("-- Setting initial setpoint")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, util.heading))

        await util.start_offboard(drone)  

        print("-- Go 0m North, 0m East, -5m Down within local coordinate system")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, util.heading))
        await asyncio.sleep(10)

        print("-- Go 0m North, 0m East, -5m Down within local coordinate system, turn to face East")
        await drone.offboard.set_position_ned(PositionNedYaw(0, 0.0, -5.0, 180.0))
        await asyncio.sleep(10)

        await util.stop_offboard(drone)
        await util.land_drone(drone, util)

        await asyncio.sleep(10)


    async def altitude_control(self, drone, util):

        print("-- Setting initial setpoint")
        await drone.action.set_takeoff_altitude(4)
        await drone.action.takeoff()
        await asyncio.sleep(8)

        await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))
        await util.start_offboard(drone)

        # await drone.offboard.PositionGlobalYaw(lat_deg, lon_deg, alt_m, yaw_deg, altitude_type)

        # print("-- Go up at 70% thrust")
        await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.7))
        await asyncio.sleep(4)

        print("-- Roll 30 at 60% thrust")
        await drone.offboard.set_attitude(Attitude(30.0, 0.0, 0.0, 0.6))
        await asyncio.sleep(2)

        print("-- Roll -30 at 60% thrust")
        await drone.offboard.set_attitude(Attitude(-30.0, 0.0, 0.0, 0.6))
        await asyncio.sleep(2)

        print("-- Hover at 60% thrust")
        await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.6))
        await asyncio.sleep(2)

        await util.stop_offboard(drone)
        await util.land_drone(drone, util)
        
        await asyncio.sleep(10)


    async def GPS_control(self, drone, util):

        print("-- Setting initial setpoint")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

        await util.start_offboard(drone)

        print("-- Go 0m North, 0m East, -5m Down within local coordinate system")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
        await asyncio.sleep(10)

        print("-- Go 5m North, 0m East, -5m Down within local coordinate system, turn to face East")
        await drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, -5.0, 90.0))
        await asyncio.sleep(10)

        print("-- Go 5m North, 10m East, -5m Down within local coordinate system")
        await drone.offboard.set_position_ned(PositionNedYaw(5.0, 10.0, -5.0, 90.0))
        await asyncio.sleep(15)

        print("-- Go 0m North, 10m East, 0m Down within local coordinate system, turn to face South")
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 10.0, 0.0, 180.0))
        await asyncio.sleep(10)

        await util.stop_offboard(drone)
        await util.land_drone(drone, util)

        await asyncio.sleep(10)


    # Moves the drone in a circle -> then circle sideways
    # Can move the drone at different speeds
    async def velocity_control(self, drone, util):

        print("-- Setting initial setpoint")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

        await util.start_offboard(drone)

        print("-- Turn clock-wise and climb")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, -1.0, 60.0))
        await asyncio.sleep(5)

        print("-- Turn back anti-clockwise")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, -60.0))
        await asyncio.sleep(5)

        print("-- Wait for a bit")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(2)

        print("-- Fly a circle")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(5.0, 0.0, 0.0, 30.0))
        await asyncio.sleep(15)

        print("-- Wait for a bit")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(5)

        print("-- Fly a circle sideways")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, -5.0, 0.0, 30.0))
        await asyncio.sleep(15)

        print("-- Wait for a bit")
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(8)

        await util.stop_offboard(drone)
        await util.land_drone(drone, util)

        await asyncio.sleep(10)


    async def GPS_velocity_control(self, drone, util):

        await util.start_offboard(drone)

        print("-- Setting initial setpoint")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))

        print("-- Go up 2 m/s")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, -2.0, 0.0))
        await asyncio.sleep(4)

        print("-- Go North 2 m/s, turn to face East")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(2.0, 0.0, 0.0, 90.0))
        await asyncio.sleep(4)

        print("-- Go South 2 m/s, turn to face West")
        await drone.offboard.set_velocity_ned(
            VelocityNedYaw(-2.0, 0.0, 0.0, 270.0))
        await asyncio.sleep(4)

        print("-- Go West 2 m/s, turn to face East")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, -2.0, 0.0, 90.0))
        await asyncio.sleep(4)

        print("-- Go East 2 m/s")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 2.0, 0.0, 90.0))
        await asyncio.sleep(4)

        print("-- Turn to face South")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 180.0))
        await asyncio.sleep(2)

        print("-- Go down 1 m/s, turn to face North")
        await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 1.0, 0.0))
        await asyncio.sleep(4)

        await util.stop_offboard(drone)
        await util.land_drone(drone, util)

        await asyncio.sleep(10)


    async def schedule_mission(self, drone):
        mission_items = []

        # Need to give proper information to mission coordinates (47,8)

        # mission_items.append(MissionItem(47.398039859999997,
        #                                 8.5455725400000002,
        #                                 25,
        #                                 10,
        #                                 True,
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 MissionItem.CameraAction.NONE,
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan')))
        # mission_items.append(MissionItem(47.398036222362471,
        #                                 8.5450146439425509,
        #                                 25,
        #                                 10,
        #                                 True,
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 MissionItem.CameraAction.NONE,
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan')))
        # mission_items.append(MissionItem(47.397825620791885,
        #                                 8.5450092830163271,
        #                                 25,
        #                                 10,
        #                                 True,
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 MissionItem.CameraAction.NONE,
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan'),
        #                                 float('nan')))

        # mission_plan = MissionPlan(mission_items)

        # await drone.mission.set_return_to_launch_after_mission(True)

        # print("-- Uploading mission")
        # await drone.mission.upload_mission(mission_plan)

        # print("-- Starting mission")
        # await drone.mission.start_mission()

        # await util.land_drone(drone, di.termination_task, util)

        # await asyncio.sleep(10)


    async def qgroundcontrol_mission(self, drone, util):
        mission_import_data = await drone.mission_raw.import_qgroundcontrol_mission("example-mission.plan")
        print(f"{len(mission_import_data.mission_items)} mission items imported")
        await drone.mission_raw.upload_mission(mission_import_data.mission_items)
        print("Mission uploaded")