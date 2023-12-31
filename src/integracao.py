from serial import Serial
from threading import Thread, Timer
from time import sleep
# from traceback import format_exc
from unidecode import unidecode

PORTA = "/dev/ttyUSB0"        # alterar dependendo de onde vai rodar
# sudo chmod a+rw /dev/ttyACM0 ou # sudo chmod a+rw /dev/ttyACM1 sudo chmod a+rw /dev/ttyUSB0

# CASO A SERIAL NÃO FUNCIONE, COMENTE A LINHA ABAIXO E DESCOMENTE A SEGUINTE
meu_serial = Serial(PORTA, baudrate=115200, timeout=0.1)
# meu_serial = None

#iniciou = False


def serial():
    while True:
        if meu_serial != None:
            texto_recebido = meu_serial.readline().decode().strip()
            if texto_recebido != "":
                print(f"RECEBIDO DO ARDUINO: {texto_recebido}")

                # ESCREVA AQUI O SEU CÓDIGO DA SERIAL!

        sleep(0.1)


def serial_load():
    thread = Thread(target=serial)
    thread.daemon = True
    thread.start()
    print("[INFO] Serial: ok")


def serial_send(texto):
    # if iniciou == False:
    meu_serial.write("INICIOU\n".encode("UTF-8"))
    # iniciou == True
    # else:
    # COLOQUE AQUI O CÓDIGO DO WHILE DA IMPLEMENTACAO
    # print("ESCRITO DO PYTHON: TESTE")
    meu_serial.write(texto.encode("UTF-8"))
    # sleep(1)

    meu_serial.write("\nFINALIZOU".encode("UTF-8"))


# serial_load()
# serial_send()
