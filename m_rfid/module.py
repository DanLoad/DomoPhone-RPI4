from serial import Serial
from m_rfid.db import *
import logging
import time
import re


timePause = 0;

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

def Rfid_loop():

    ser = Serial()
    try:
        ser = Serial("/dev/ttyS0", 9600, timeout=3.0)
        ser.open()
    except Exception as e:
        print('RFID считыватель не может инициализироваться!')

    print("loop")
    while True:
        #Read_uid(ser)

        if ser.is_open:
            if ser.in_waiting > 0:
                value = ""
                try:
                    read_byte = ser.read()
                except:
                    read_byte = "?"
                logging.info("redb >>>>>>>>>>")
                logging.info(read_byte)
                logging.info("redb >>>>>>>>>>")
                if read_byte == b'\x02':
                    for Counter in range(12):
                        try:
                            read_add = ser.read()
                        except:
                            read_add = "?"
                            break
                        value = value + read_add.decode('utf8')
                    logging.info(value)
                    if re.match("^[A-Za-z0-9]*$", value):
                        global timePause

                        if RunCheckVar("STATUS", "REC"):
                            if RunCheckRfid(value):
                                RunSaveRfid(value)
                                RunChangeVar("STATUS", "SAVE")
                                logging.info("save >>>>>>>>>>")

                                aa
                            else:
                                RunChangeVar("STATUS", "NO")
                                logging.info("NOOOOO save >>>>>>>>>>")
                                ser.flushInput()
                                ss

                        elif time.time() > timePause:
                            if RunAccess(value):
                                logging.info("Open door >>>>>>>>>>")
                                timePause = time.time() + 1
                                dd
                            else:
                                logging.info("no open door >>>>>>>>>>>")
                                ff
                        else:
                            ser.flushInput()
                    else:
                        ser.flushInput()
