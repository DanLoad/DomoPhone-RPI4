from serial import Serial
from m_rfid.db import *
#from m_rfid import settings
#from m_rfid.module import *
import logging
import time
import re

from django.conf import settings
from m_rfid import my_settings

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
                settings.configure(my_settings, RFID_STATUS="DDE")
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
                        logging.info(settings.RFID_STATUS)
                        global timePause

                        if settings.RFID_STATUS == "REC":
                            dd
                            # logging.info(RunCheckValue("rfid", value))

                            if RunCheckValue(value):
                                if RunSave(value):
                                    settings.configure(my_settings, RFID_STATUS="SAVE")
                                else:
                                    ser.flushInput()

                        elif time.time() > timePause:
                            if RunAccess(value):
                                logging.info("Open door >>>>>>>>>>")
                                rt
                                timePause = time.time() + 1
                            else:
                                logging.info("no open door >>>>>>>>>>>")
                                gt
                        else:
                            ser.flushInput()
                    else:
                        ser.flushInput()
























                        """
                        if RunAccess("rfid", value):
                            logging.info("Open door >>>>>>>>>>")
                            rt
                            timePause = time.time() + 1
                        else:
                            logging.info("no open door >>>>>>>>>>>")
                            gt





                        if settings.RFID_STATUS == REC:
                            # logging.info(RunCheckValue("rfid", value))

                            if RunCheckValue("rfid", value):
                                RunSave("rfid", value)
                        elif time.time() > timePause:
                            if RunAccess("rfid", value):
                                logging.info("Open door >>>>>>>>>>")
                                rt
                                timePause = time.time() + 1
                            else:
                                logging.info("no open door >>>>>>>>>>>")
                                gt
                        else:
                            ser.flushInput()
                    else:
                        ser.flushInput()


                        """
