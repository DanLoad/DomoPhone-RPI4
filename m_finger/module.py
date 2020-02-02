from pyfingerprint.pyfingerprint import PyFingerprint
from serial import Serial
from m_rfid.db import *
import logging
import time
import re
import hashlib

timePause = 0;

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

def Finger_loop():
    ser = Serial()
    try:
        ser = PyFingerprint('/dev/ttyAMA1', 115200, 0xFFFFFFFF, 0x00000000)
        if ( ser.verifyPassword() == False ):
            raise ValueError('Указан неверный пароль датчика отпечатка пальца!')
    except Exception as e:
        print('Датчик отпечатка пальца не может быть инициализирован!')
        print('Сообщение об исключении: ' + str(e))
        exit(1)
    while True:
        if RunCheckVar("STATUS", "REC"):
            Add_finger(ser)
        elif RunCheckVar("STATUS", "DELETE"):
            Delete_finger(ser)
        else:
            Check_finger(ser)




def Add_finger(ser):
    logging.info('Currently used templates: ' + str(ser.getTemplateCount()) +'/'+ str(ser.getStorageCapacity()))
    try:
        place = FingerFree()
        if not place == "FULL":
            FingerChangeVar("STEP", "ONE")
            while FingerCheckVar("STATUS", "REC") & FingerCheckVar("STEP", "ONE"):
                if ser.readImage():
                    ser.convertImage(0x01)
                    result = ser.searchTemplate()
                    positionNumber = result[0]
                    logging.info("Позиция ..." + str(positionNumber))
                    if positionNumber >= 0:
                        if FingerCheckValue("finger", positionNumber):
                            print('Template already exists at position #' + str(positionNumber))
                            logging.info("Такой существует")
                            continue
                        else:
                            if ser.deleteTemplate(positionNumber):
                                FingerChangeVar("STATUS", "REC")
                                FingerChangeVar("STEP", "ONE")
                                logging.info("Сначало удалил и...")
                                continue
                            else:
                                FingerChangeVar("STATUS", "ERROR")
                                FingerChangeVar("STEP", "NO")
                                continue
                    FingerChangeVar("STEP", "REMOWE")
                    time.sleep(2)
                    logging.info('Waiting for same finger again...')
                    FingerChangeVar("STEP", "TWO")
            while FingerCheckVar("STATUS", "REC") & FingerCheckVar("STEP", "TWO"):
                if ser.readImage():
                    ser.convertImage(0x02)
                    if ( ser.compareCharacteristics() == 0 ):
                        FingerChangeVar("STATUS", "NOT_MATCH")
                        FingerChangeVar("STEP", "NO")
                        continue
                    else:
                        ser.createTemplate()
                        positionNumber = ser.storeTemplate(place)
                        if positionNumber == place:
                            FingerSave(place)
                            logging.info("Палец сохранен в " + str(place))
                        else:
                            FingerChangeVar("STATUS", "NO")
                            FingerChangeVar("STEP", "ERROR")
        else:
            FingerChangeVar("STATUS", "NO")
            FingerChangeVar("STEP", "FULL")
    except Exception as e:
        FingerChangeVar("STATUS", "NO")
        FingerChangeVar("STEP", "ERROR")
        logging.info('Operation failed!')
        logging.info('Exception message: ' + str(e))




def Check_finger(ser):
    try:
        ## Ждет пока не прочитает палец
        if ser.readImage() == True:
            ## Преобразует изображение и сохраняет в буфер №1
            ser.convertImage(0x01)
            ## Ищет шаблон
            result = ser.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]
            if not positionNumber == -1:
                logging.info('Найден шаблон в позиции #' + str(positionNumber))
                logging.info('Оценка точности: ' + str(accuracyScore))
                ## Загружает найденый шаблон в буфер №1
                uart.loadTemplate(positionNumber, 0x01)
                ## Скачивает характеристики шаблона, загруженного в charbuffer 1
                characterics = str(uart.downloadCharacteristics(0x01)).encode('utf-8')
                ## Хеширует характеристики шаблона
                logging.info('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
                logging.info("open door>>>>>>>>>>>>>")
            else:
                logging.info('Совпадение не найдено!')
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))



def Delete_finger(ser):
    run = Status.objects.get(comand = "run")
    number = int(run.number)
    if number >= 0:
        if ( uart.deleteTemplate(number) == True ):
            FingerDelete("finger", number)
            RunChangeStatus("delete", "ok")
