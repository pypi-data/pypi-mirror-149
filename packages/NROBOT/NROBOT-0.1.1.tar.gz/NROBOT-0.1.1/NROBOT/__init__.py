import os
import time
import math
try:
  import websocket
except:
  os.system('pip3 install websocket-client')
  import websocket



class NROBOT:
   def __init__(self,S_ADRESS):
      self.ws = websocket.WebSocket()
      self.ws.connect(S_ADRESS)
      self.cmd_mode = False
      self.oa_mode = 0
      self.R1 = 10000.0 #Resistor 1 of Voltage Divider
      self.R2 = 1000.0  #Resistor 2 of Voltage Divider
      
   def connect(self,S_ADDR=None):
      if S_ADDR != None:
         self.ws.connect(S_ADDR)

   def send(self,INPUT):
      self.ws.send(INPUT)

   def recieve(self):
      return self.ws.recv()
      
   def mode(self,N):
     if str(N) in ['0','1','2']:
       M_STATES = {
        '0':'STEP_MODE',
        '1':'SMOOTH_MODE',
        '2':'CONTINOUS_MODE'
       }
       if str(N) == '0': self.ws.send("Z")
       elif str(N) == '1': self.ws.send("Q")
       elif str(N) == '2': self.ws.send("X")
       return {
        'STATUS':f'Mode Set to {M_STATES[str(N)]}'
       }

   def move(self,DIRECTION):
      MOVE_STATES = {
        'L':'LEFT',
        'R':'RIGHT',
        'F':'FORWARD',
        'B':'BACKWARD',
        'S':'STOP'
      }
      if str(DIRECTION).upper() in ['L','R','F','B','S']:
        self.ws.send(str(DIRECTION.upper()))
        return {
          'STATUS':f'Direction Set to {MOVE_STATES[DIRECTION]}'
        }


   def stop(self): self.ws.send('S')

   def led(self,STATE):
      LED_STATES = {
        '0':'OFF',
        '1':'ON'
      }
      if str(STATE) in ['0','1']:
        if str(STATE) == '1': self.ws.send('o')
        else: self.ws.send('f')
      return {
        'STATUS':f'Led Set to {LED_STATES[str(STATE)]}'
      }

   def speed(self,N):
    if int(N) > 0 and int(N) <= 255:
      self.ws.send(f'p{N}')
      return {
        'STATUS':f'Speed Set to {int(N)}'
      }

   def m1_speed(self,N):
    if int(N) > 0 and int(N) <= 255:
      self.ws.send(f'e{N}')
      return {
        'STATUS':f'Moter 1 Speed Set to {int(N)}'
      }

   def m2_speed(self,N):
       if int(N) > 0 and int(N) <= 255:
         self.ws.send(f'w{N}')
         return {
           'STATUS':f'Moter 2 Speed Set to {int(N)}'
         }

   def step_delay(self,MS):
     self.ws.send(f'd{int(MS)}')
     return {
       'STATUS':f'Step Delay Set to {int(MS)}' 
     }

   def go(self,TRACK,delay=0.5):
     self.mode(0)
     for D in list(TRACK.upper()):
       if D in ['L','R','F','B','S']:
          self.move(D)
          time.sleep(delay)
     return {
        'STATUS':'Track Completed !'
     }

   def left(self,ms=None):
     if ms != None:
       self.ws.send('L')
       time.sleep(ms/1000.0)
       self.ws.send('S')
     else:
       self.ws.send('L')
       time.sleep(0.2)
       self.ws.send('S')

   def right(self,ms=None):
     if ms != None:
       self.ws.send('R')
       time.sleep(ms/1000.0)
       self.ws.send('S')
     else:
       self.ws.send('R')
       time.sleep(0.2)
       self.ws.send('S')

   def forward(self,ms=None):
     if ms != None:
       self.ws.send('F')
       time.sleep(ms/1000.0)
       self.ws.send('S')
     else:
       self.ws.send('F')
       time.sleep(0.2)
       self.ws.send('S')  

   def backward(self,ms=None):
     if ms != None:
       self.ws.send('B')
       time.sleep(ms/1000.0)
       self.ws.send('S')
     else:
       self.ws.send('B')
       time.sleep(0.2)
       self.ws.send('S')

   def get_battery(self):
      self.ws.send('k')
      time.sleep(0.1)
      r = self.ws.recv().replace('C','')
      adc = int(r)
      RFRAC = self.R2 / (self.R1 + self.R2)
      batV = adc*((3.3 / 1024.0) / RFRAC)
      BPER = math.floor((batV / 12.6) * 100.0)
      return {
        'STATUS':f'Voltage : {batV} , Percentage : {BPER}%',
        'VOLTAGE':batV,
        'LEVEL':BPER
      }

   def get_adc(self):
      self.ws.send('k')
      time.sleep(0.1)
      r = self.ws.recv().replace('C','')
      adc = int(r)
      return {
        'STATUS':f'ADC VALUE : {adc}',
        'ADC':adc,
      }

   def object_distance(self):
      self.ws.send('h')
      time.sleep(0.1)
      r = self.ws.recv().replace('I','')
      return {
       'STATUS':f'Distance : {r} cm'
      }
      
   def object_avoidance_mode(self):
     self.ws.send('A')
     self.oa_mode = not self.oa_mode
     ES = ["DISABLED","ENABLED"]
     return {
        'STATUS':f"Object Avoidance Mode {E_S[self.oa_mode]}"
     }

   def cmd_control(self):
     self.cmd_mode = True
     os.system('clear')
     print("""
     
        \----[ NROBOT CMD_CONTROL ]----/
           \------------------------/
                   
     """)
     while self.cmd_mode == True:
       cmd_inp = input(" > ").upper()
       if cmd_inp in list('LRFBS'):
          r = self.move(cmd_inp)
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "LED":
          r = self.led(cmd_inp.split(' ')[1])
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "SPEED":
          r = self.speed(cmd_inp.split(' ')[1])
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "MODE":
          r = self.mode(cmd_inp.split(' ')[1])  
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "STEP_DELAY":
          r = self.step_delay(cmd_inp.split(' ')[1])
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "GO":
          r = self.go(cmd_inp.split(' ')[1])
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "OBJECT_AVOIDANCE_MODE":
          r = self.object_avoidance_mode()
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "OBJECT_DISTANCE":
          r = self.object_distance()
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "GET_BATTERY":
          r = self.get_battery()
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp.split(' ')[0] == "GET_ADC":
          r = self.get_adc()
          if r.get('STATUS') != None: print(f" > STATUS | {r.get('STATUS')}")
       elif cmd_inp == "HELP":
          print('''
            ====== [  COMMANDS ] ======

                 L     | MOVE LEFT
                 R     | MOVE RIGHT
                 F     | MOVE FORWARD
                 B     | MOVE BACKWARD
               LED 1-0 | TURN ON/OFF LED
           SPEED 0-255 | SET SPEED IN RANGE 0 TO 255
                MODE 0 | SET ROBOT IN STEP MODE
                MODE 1 | SET ROBOT IN SMOOTH MODE
                MODE 2 | SET ROBOT IN CONTINOUS MODE
        STEP_DELAY 100 | SET ROBOT HAVE STEP DELAY OF 100ms
                GO LR  | MOVE ROBOT TO LEFT AND THEN RIGHT
 OBJECT_AVOIDANCE_MODE | SET ROBOT TO AVOID OBSTACLE AND MOVE RANDOMLY
       OBJECT_DISTANCE | GET DISTANCE FROM OBJECT INFRONT OF ROBOT
           GET_BATTERY | GET BATTERY VALUE AND PERCENTAGE
           GET_ADC     | GET ADC VALUE 
          
          ''')
       elif cmd_inp == "EXIT":
          self.cmd_mode = False
       else:
          print(f" > ERROR | INVALID INSTRUCTION COMMAND !")
    
       
