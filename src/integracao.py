from serial import Serial
from threading import Thread, Timer
from time import sleep
from cv2 import *
from traceback import format_exc

    
def serial():
  while True:
    if meu_serial != None:
      texto_recebido = meu_serial.readline().decode().strip()
      if texto_recebido != "":
        print(texto_recebido)

        # ESCREVA AQUI O SEU CÓDIGO DA SERIAL!



            
    sleep(0.1)
    

# CASO A SERIAL NÃO FUNCIONE, COMENTE A LINHA ABAIXO E DESCOMENTE A SEGUINTE

meu_serial = Serial("ttyACM0", baudrate=9600, timeout=0.1)
#meu_serial = None

print("[INFO] Serial: ok")

thread = Thread(target=serial)
thread.daemon = True
thread.start()  

#drone = Tello("TELLO-C7AC08", test_mode=True)
drone = Tello("TELLO-D023AE", test_mode=True)
drone.inicia_cmds()
print("[INFO] Drone pronto")



def imprime_e_envia_coordenadas():

  # ESCREVA AQUI O CÓDIGO DO TIMER RECORRENTE
  
  
  
  timer = Timer(2, imprime_e_envia_coordenadas)
  timer.start() 
   
   
imprime_e_envia_coordenadas()



while True:

  # COLOQUE AQUI O CÓDIGO DO WHILE DA IMPLEMENTACAO
    

  if waitKey(1) & 0xFF == ord("q"):
    break
    
   