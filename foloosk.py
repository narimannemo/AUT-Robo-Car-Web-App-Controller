from flask import Flask, render_template, request, redirect, Response
import tty , termios,sys, time, serial,numpy,threading,webbrowser
import random, json,os,sys
from flask_cors import CORS
from werkzeug import *
 
class robot:
    JOYSTICK_DELAY = .05
    MOTOR_SPEED_MAX = 200
    MOTOR_SPEED_STEP = 17
    MOTOR_SPEED_TURN = 70
    MOTOR_SPEED_MINISTEP = 10

    portfd=0
    espPort = "";

    motorLeftError = [0,0,0]
    motorRightError = [0,0,0]
    Ts = .1
    K_p = .127
    K_i = 1.27
    K_d = .00317
    a = K_p + K_i * Ts / 2 + K_d / Ts
    b = -K_p + K_i * Ts / 2 - 2 * K_d / Ts
    c = K_d / Ts



    motorSpeedLeft=0
    motorSpeedRight=0
    motorSpeedLeft_d=0
    motorSpeedRight_d=0

    motorShaftLeft=0
    motorShaftRight=0

    omegaL=0		
    omegaR=0

    sonarRear=0			
    sonarRearL=0
    sonarRearR=0
    sonarFront=0
    sonarFrontL=0					
    sonarFrontR=0

    updateTime=0		

    battery=0
    reset=0

class robotFunction:

    def robotToString(self,robot):
        print("The left motor speed is: "+str(int(robot.motorSpeedLeft))+"\n"\
              "The right motor speed is: "+str(int(robot.motorSpeedRight))+"\n"\
              "The left motor shaft speed is: "+str(int(robot.motorShaftLeft))+"\n"\
              "The right motor shaft speed is: "+str(int(robot.motorShaftRight))+"\n"\
              "The voltage battery is: "+str(robot.battery)+"\n")
    def updateRobot(self,robot):
        if robot.reset ==1:
            command = r"R%d %d\n" % (robot.motorSpeedLeft, robot.motorSpeedRight)
            robot.reset = 0
        else:
            command=r"S%d %d\n"%(robot.motorSpeedLeft,robot.motorSpeedRight)
        bcommand=command.encode()
        print(bcommand)
        try:
            robot.portfd.write(bcommand)
            close = False     
        except:
            print("Error: Can't write on serial")
            close = True
        data = [0,0,0,0,0,0,0,0,0]
        for i in range(0,9):
            try:
                bufptr = robot.portfd.readline()
            except:
                print("Error: Can't read from serial")
                close = True
                break
            if  not close:
                if i<8:
                    data[i] = int(bufptr)
                else:
                    robot.battery = float(bufptr)
        if not close:
            robot.motorShaftLeft = float(data[0]/10)
            robot.motorShaftRight = float(data[1]/10)
            robot.sonarRear = data[2]
            robot.sonarRearL = data[3]
            robot.sonarFrontL = data[4]
            robot.sonarFront = data[5]
            robot.sonarFrontR = data[6]
            robot.sonarRearR = data[7]
    def setMotorSpeeds(self,robot, left, right):
        robot.motorSpeedLeft_d = left
        robot.motorSpeedRight_d = right
        #time.sleep(0.5)
    def getchar(self):
       #Returns a single character from standard input
       fd = sys.stdin.fileno()
       old_settings = termios.tcgetattr(fd)
       try:
          tty.setraw(sys.stdin.fileno())
          ch = sys.stdin.read(1)
       finally:
          termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
       #self.robotToString(robot)
       return ch  
    def joysticMode(self,robot,ch):
        ch = str(ch[0])
        left = robot.motorSpeedLeft_d
        right = robot.motorSpeedRight_d
        if ch == 'w':
            if left < robot.MOTOR_SPEED_MAX or right < robot.MOTOR_SPEED_MAX:
                left = min(robot.MOTOR_SPEED_MAX, left + robot.MOTOR_SPEED_STEP)
                right = min(robot.MOTOR_SPEED_MAX, right + robot.MOTOR_SPEED_STEP)
            self.setMotorSpeeds(robot, left, right)
            #return False
        elif ch == 't':
            left = right = 0
            self.setMotorSpeeds(robot, left, right)
            exit()
            #return True
        elif ch=='s':
                if left > -1*robot.MOTOR_SPEED_MAX or right > -1*robot.MOTOR_SPEED_MAX:
                    left = max(-1*robot.MOTOR_SPEED_MAX, left - robot.MOTOR_SPEED_STEP)
                    right = max(-1*robot.MOTOR_SPEED_MAX, right - robot.MOTOR_SPEED_STEP)
                self.setMotorSpeeds(robot, left, right)
                #return False
        elif ch=='a':
                if left > -1*robot.MOTOR_SPEED_MAX or right < robot.MOTOR_SPEED_MAX:
                    left = max(-1*robot.MOTOR_SPEED_MAX, left - robot.MOTOR_SPEED_STEP)
                    right = min(robot.MOTOR_SPEED_MAX, right + robot.MOTOR_SPEED_STEP)
                self.setMotorSpeeds(robot, left, right)
                #return False
        elif ch=='d':
                if left < robot.MOTOR_SPEED_MAX or right > -1*robot.MOTOR_SPEED_MAX:
                    left = min(robot.MOTOR_SPEED_MAX, left + robot.MOTOR_SPEED_STEP)
                    right = max(-1*robot.MOTOR_SPEED_MAX, right - robot.MOTOR_SPEED_STEP)
                self.setMotorSpeeds(robot, left, right)
               # return False
        elif ch=='q':
                if left != robot.MOTOR_SPEED_TURN or right < robot.MOTOR_SPEED_MAX:
                    if left < robot.MOTOR_SPEED_TURN:
                        left = min(robot.MOTOR_SPEED_TURN, left + robot.MOTOR_SPEED_MINISTEP)
                    elif left > robot.MOTOR_SPEED_TURN:
                        left = max(robot.MOTOR_SPEED_TURN, left - robot.MOTOR_SPEED_MINISTEP)
                    right = min(robot.MOTOR_SPEED_MAX, right + robot.MOTOR_SPEED_STEP)
                self.setMotorSpeeds(robot, left, right)
                #return False
        elif ch=='e':
                if left < robot.MOTOR_SPEED_MAX or right != robot.MOTOR_SPEED_TURN:
                    left = min(robot.MOTOR_SPEED_MAX, left + robot.MOTOR_SPEED_STEP)
                    if right < robot.MOTOR_SPEED_TURN:
                        right = min(robot.MOTOR_SPEED_TURN, right + robot.MOTOR_SPEED_MINISTEP)
                    elif right > robot.MOTOR_SPEED_TURN:
                        right = max(robot.MOTOR_SPEED_TURN, right - robot.MOTOR_SPEED_MINISTEP)
                self.setMotorSpeeds(robot, left, right)
                #return False
        else:
                left = right = 0
                self.setMotorSpeeds(robot, left, right)
                #return False




class SpeedController:
    def speed_changer(self,robot,robotFunction,left,right):
        leftSteps = abs(int((left - robot.motorSpeedLeft)/robot.MOTOR_SPEED_STEP))
        rightSteps = abs(int((right - robot.motorSpeedRight)/robot.MOTOR_SPEED_STEP))
        steps = min(leftSteps,rightSteps)
        L = robot.motorSpeedLeft
        R = robot.motorSpeedRight
        for i in range(0,steps):
           L += numpy.sign(left - L)*17
           R += numpy.sign(right - R)*17
           robotFunction.setMotorSpeeds(robot,L,R)
           #robotFunction.updateRobot(robot)
        if leftSteps > rightSteps:
            R += numpy.sign(right - R)\
                                     *(abs(right - R)%robot.MOTOR_SPEED_STEP)
            robotFunction.setMotorSpeeds(robot,L,R)
            #robotFunction.updateRobot(robot)
            for j in range(0, max(leftSteps,rightSteps) - steps):
                L += numpy.sign(left - L)*17
                robotFunction.setMotorSpeeds(robot,L,R)
                #robotFunction.updateRobot(robot)
            L += numpy.sign(left - L)\
                                    *(abs(left - L)%robot.MOTOR_SPEED_STEP)        
            robotFunction.setMotorSpeeds(robot,L,R)
            #robotFunction.updateRobot(robot)
        elif leftSteps < rightSteps:
            L += numpy.sign(left - L)\
                                    *(abs(left - L)%robot.MOTOR_SPEED_STEP)        
            robotFunction.setMotorSpeeds(robot,L,R)
            #robotFunction.updateRobot(robot)
            for j in range(0, max(leftSteps,rightSteps) - steps):
                R+= numpy.sign(right - R)*17
                robotFunction.setMotorSpeeds(robot,L,R)
                #robotFunction.updateRobot(robot)
            R += numpy.sign(right - R)\
                                     *(abs(right - R)%robot.MOTOR_SPEED_STEP)
            robotFunction.setMotorSpeeds(robot,L,R)
            #robotFunction.updateRobot(robot)
        else:
            
            R += numpy.sign(right - R)\
                                     *(abs(right - R)%robot.MOTOR_SPEED_STEP)
            L += numpy.sign(left - L)\
                                    *(abs(left - L)%robot.MOTOR_SPEED_STEP)
            robotFunction.setMotorSpeeds(robot,L,R)
            #robotFunction.updateRobot(robot)
            
def PID(robot,robotFunction):
    while True:
        start = time.time()
        # must be deleted to PID works
        # simulated error since encoder was not available 
        robot.motorShaftLeft = robot.motorSpeedLeft_d - .6*robot.motorShaftLeft
        robot.motorShaftRight = robot.motorSpeedRight_d - .4*robot.motorShaftRight
        #reading Input
        errRight = robot.motorLeftError
        errLeft = robot.motorRightError
        errRight[0] = errRight[1]
        errLeft[0] = errLeft[1]
        errRight[1] = errRight[2]
        errLeft[1] = errLeft[2]
        errLeft[2] = robot.motorSpeedLeft_d - robot.motorShaftLeft
        errRight[2] = robot.motorSpeedRight_d - robot.motorShaftRight
        #calculate Output
        j = robot.motorSpeedLeft_d
        k = robot.motorSpeedRight_d
        j += robot.a * errLeft[2] + robot.b * errLeft[1] + robot.c * errLeft[0]
        k += robot.a * errRight[2] + robot.b*errRight[1] + robot.c * errRight[0]
        robot.motorSpeedLeft = numpy.sign(j)*min(abs(j),200)
        robot.motorSpeedRight = numpy.sign(k)*min(abs(k),200)
        #updating State
        robot.motorLeftError = errRight
        robot.motorRightError = errLeft
        #print("left Error is: "+str(errLeft[2])+"\n"\
        #      "Right Error is: "+str(errRight[2])+"\n")
        end = time.time()
        time.sleep(robot.Ts-end+start)
        robotFunction.updateRobot(robot)
        robotFunction.robotToString(robot)
        
def main(method,robot,robotFunction,speedController):          
    if method ==1:
        while True:
             ch = robotFunction.getchar()
             #print(ch)
             robotFunction.joysticMode(robot,ch)
             #print("done")
    elif method==2:
        while True:
            try:
                left = int(input("Enter desired speed value for Left motor\n"))
                right = int(input("Enter desired speed value for right motor\n"))
                break
            except:
                print("Enter integer please!")

        corrected_left = numpy.sign(left)*min(abs(left),robot.MOTOR_SPEED_MAX)
        corrected_right = numpy.sign(right)*min(abs(right),robot.MOTOR_SPEED_MAX)
        #print(corrected_left,corrected_right)
        speedController.speed_changer(robot,robotFunction,corrected_left,corrected_right)
        print("Press any key to Stop ...\nFor emergency enter 'e'\n")
        if(robotFunction.getchar() == 'e'):
            robotFunction.setMotorSpeeds(robot,0,0)
            robotFunction.updateRobot(robot)
        else:
            speedController.speed_changer(robot,robotFunction,0,0)

      
def method(robot):
    robotPort = input("Enter Robot port: ")
    espPort = input("Enter ESP Port: ")
    robot.espPort = espPort
    try:
        robotPort = "/dev/ttyUSB%s"%robotPort
        ser=serial.Serial(robotPort)
        ser.baudrate=38400
        robot.portfd=ser
    except:
#        try:
 #           #time.sleep(.1)
  #          ser=serial.Serial('/dev/ttyUSB0')
   #         ser.baudrate=38400
    #        robot.portfd=ser
     #   except:
         print("Error: Serial port not found")
        #exit()
    while True:
        print("Select how to control robot: \n1-Using keyboard\n2-Using speed controller\n3-Using Web\n4-Useing Wemos D1 (note that you need internet connection!!)")
        try:
            method = int(input())
            if method == 1 or method == 2 or method == 3 or method == 4:
                if method == 3:
                    webbrowser.open('/home/pi/Desktop/robot/templates/index.html', new=2,autoraise = True)
                return method
                break
                #print("Here you must select 3 :)")
        except:
            print("You must select 1, 2, 3,or 4 :)")
        
def esp(robotFunction,espPort):
    espPort = "/dev/ttyUSB%s"%espPort
    espser =  serial.Serial(espPort,baudrate = 115200)
    while True:
        try:
            j = espser.readline().decode('utf-8')
            print(j)
        except:
            j='08'
        try:
            v = j[1]
        except:
            v='8'
        if j[0] == '1' and (v=='9' or v=='7'):
            print('ip address is: \n')
            print(j)
            webbrowser.open("http://%s:80"%j, new=2,autoraise = True)
            print("get the IP address it will go fast...")
        #if ("/w" in j) or j == 'a\n' or j == 's\n' or j == 'd\n' :
        if ('w\r' in j) or ('a\r' in j) or ('s\r' in j) or ('d\r' in j) :
            robotFunction.joysticMode(robot,j)
            com = r"%dt%dt"%(robot.motorSpeedLeft_d,robot.motorSpeedRight_d)
            print(com.encode())
            espser.write(com.encode())

robot = robot()
robotFunction = robotFunction()
SpeedController = SpeedController()
lock = threading.Lock()
meth = method(robot)
#print(meth)
if meth == 2 or meth == 1:
    t_main = threading.Thread(target = main , args = (meth,robot,robotFunction,SpeedController,))
t_PID = threading.Thread(target = PID, args = (robot,robotFunction,) )
if not meth == 4:
    t_PID.start()
if meth == 2 or meth == 1:
    t_main.start()
if meth == 4:
    t_esp = threading.Thread(target = esp,args = (robotFunction,robot.espPort,))
    t_esp.start()
    time.sleep(5)
    t_PID.start()
app = Flask(__name__)
CORS(app)
if meth == 3: 
    @app.route('/', methods=['POST','GET'])
    def output():
        ch = request.form.to_dict().keys()
        ch=list(ch)[0]
        robotFunction.joysticMode(robot,ch)
        a = [robot.motorSpeedRight_d,robot.motorSpeedLeft_d]
        return json.dumps({'rm':a[0],'lm':a[1]})
if __name__ == '__main__':
    app.run()


    
