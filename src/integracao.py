from serial import Serial
from threading import Thread, Timer
from time import sleep
from traceback import format_exc
from unidecode import unidecode


def serial():
    while True:
        if meu_serial != None:
            texto_recebido = meu_serial.readline().decode().strip()
            if texto_recebido != "":
                print(f"RECEBIDO DO ARDUINO: {texto_recebido}")

                # ESCREVA AQUI O SEU CÓDIGO DA SERIAL!

        sleep(0.1)


# CASO A SERIAL NÃO FUNCIONE, COMENTE A LINHA ABAIXO E DESCOMENTE A SEGUINTE

#meu_serial = Serial("/dev/ttyACM0", baudrate=115200, timeout=0.1)
meu_serial = None

texto = "ENVIADO DO PYTHON: OLÁ THERE\n"

print("[INFO] Serial: ok")

thread = Thread(target=serial)
thread.daemon = True
thread.start()

while True:

    # COLOQUE AQUI O CÓDIGO DO WHILE DA IMPLEMENTACAO
    #print("ESCRITO DO PYTHON: TESTE")
    meu_serial.write(texto.encode("UTF-8"))
    sleep(1)
