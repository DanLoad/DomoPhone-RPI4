from modules.RFID.RFID import *
from modules.RF.RF import *
from modules.Finger.Search import *
#from users.templates.users.run_db import *
from serial import Serial


logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )



def Finger_loop():
    uart = ""
    try:
        uart = PyFingerprint('/dev/uart2', 115200, 0xFFFFFFFF, 0x00000000)

        if ( uart.verifyPassword() == False ):
            raise ValueError('Указан неверный пароль датчика отпечатка пальца!')

    except Exception as e:
        print('Датчик отпечатка пальца не может быть инициализирован!')
        print('Сообщение об исключении: ' + str(e))
        exit(1)

    while True:
        Read_finger(uart)




def Rfid_loop():

    ser = Serial()
    try:
        ser = Serial("/dev/serial1", baudrate=115200, timeout=3.0)
        ser.open()
    except Exception as e:
        print('RFID считыватель не может инициализироваться!')

    print("loop")
    while True:
        #Read_uid(ser)

        logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )
        logging.info(ser.is_open)
        logging.info(ser.in_waiting)
        if ser.is_open:
            logging.info("222222 >>>>>>>>>>")
            eeee = ser.in_waiting
            logging.info(eeee)
            if ser.in_waiting > 0:
                value = ""
                try:
                    read_byte = uart.read()
                except:
                    read_byte = "?"
                logging.info("redb >>>>>>>>>>")
                logging.info(read_byte)
                logging.info("redb >>>>>>>>>>")
                if read_byte == b'\x02':
                    for Counter in range(12):
                        try:
                            read_add = uart.read()
                        except:
                            read_add = "?"
                            break
                        value = value + read_add.decode('utf8')
                    logging.info(value)
                    if re.match("^[A-Za-z0-9]*$", value):
                        # logging.info(RunCheckStatus("rfid", "rec", "no"))
                        global timePause
                        if RunCheckStatus("rfid", "rec", "no"):
                            # logging.info(RunCheckValue("rfid", value))
                            if RunCheckValue("rfid", value):
                                RunSave("rfid", value)
                        elif time.time() > timePause:
                            if RunAccess("rfid", value):
                                logging.info("Open door >>>>>>>>>>")
                                timePause = time.time() + 1
                            else:
                                logging.info("no open door >>>>>>>>>>>")
                        else:
                            uart.flushInput()
                    else:
                        uart.flushInput()


def RF_loop():
    while True:
        RF_run()



def Init_loop():
    RunReset()
    logging.info("Рестарт")
    delayTime = 0
    while True:
        if time.time() > delayTime:
            RunTime()
            delayTime = time.time() + 3
