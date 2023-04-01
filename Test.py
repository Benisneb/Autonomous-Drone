#!/usr/bin/env python3

import time
import serial
import sys
import select

if __name__=="__main__":
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, parity=serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
    
    pico_data =  None
    print("sh>> ")

    try:
        while True:
            i, o , e = select.select([sys.stdin], [], [], 10)
            if (i):
                command = str(sys.stdin.readline().strip()) + "\n"
            ser.writelines(bytes(command.encode('ascii')))
            print('here')
            pico_data_input=ser.readline().decode("utf-8", "ignore")
            if not(pico_data_input == pico_data):
                print("sh>> " + str(pico_data_input))
                pico_data = pico_data_input
            time.sleep(0.000001)
    except KeyboardInterrupt:
        ser.close()
        print('\n\tClosed Port\n')
        exit(1)