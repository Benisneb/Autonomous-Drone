#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.tune import (SongElement, TuneDescription, TuneError)

    # How to use the tune for custom songs
    # https://github.com/mavlink/MAVSDK-Python/blob/main/examples/tune.py

async def run():

    song_elements = []
    song_elements.append(SongElement.DURATION_4);
    song_elements.append(SongElement.NOTE_G);
    song_elements.append(SongElement.NOTE_A);
    song_elements.append(SongElement.NOTE_B);
    song_elements.append(SongElement.FLAT);
    song_elements.append(SongElement.OCTAVE_UP);
    song_elements.append(SongElement.DURATION_1);
    song_elements.append(SongElement.NOTE_E);
    song_elements.append(SongElement.FLAT);
    song_elements.append(SongElement.OCTAVE_DOWN);
    song_elements.append(SongElement.DURATION_4);
    song_elements.append(SongElement.NOTE_PAUSE);
    song_elements.append(SongElement.NOTE_F);
    song_elements.append(SongElement.NOTE_G);
    song_elements.append(SongElement.NOTE_A);
    song_elements.append(SongElement.OCTAVE_UP);
    song_elements.append(SongElement.DURATION_2);
    song_elements.append(SongElement.NOTE_D);
    song_elements.append(SongElement.NOTE_D);
    song_elements.append(SongElement.OCTAVE_DOWN);
    song_elements.append(SongElement.DURATION_4);
    song_elements.append(SongElement.NOTE_PAUSE);
    song_elements.append(SongElement.NOTE_E);
    song_elements.append(SongElement.FLAT);
    song_elements.append(SongElement.NOTE_F);
    song_elements.append(SongElement.NOTE_G);
    song_elements.append(SongElement.OCTAVE_UP);
    song_elements.append(SongElement.DURATION_1);
    song_elements.append(SongElement.NOTE_C);
    song_elements.append(SongElement.OCTAVE_DOWN);
    song_elements.append(SongElement.DURATION_4);
    song_elements.append(SongElement.NOTE_PAUSE);
    song_elements.append(SongElement.NOTE_A);
    song_elements.append(SongElement.OCTAVE_UP);
    song_elements.append(SongElement.NOTE_C);
    song_elements.append(SongElement.OCTAVE_DOWN);
    song_elements.append(SongElement.NOTE_B);
    song_elements.append(SongElement.FLAT);
    song_elements.append(SongElement.DURATION_2);
    song_elements.append(SongElement.NOTE_G);

    tune_description = TuneDescription(song_elements, 200)
    await drone.tune.play_tune(tune_description)

    print("Tune played")

async def connect_drone():
    print(drone)
    await drone.connect(system_address="serial:///dev/ttyACM0:921600")
    #await drone.connect(system_address="udp://localhost:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

async def main():
    connect_drone()
    run()

if __name__ == "__main__":
    # Run the asyncio loop
    drone = System() 
    asyncio.run(main())
