#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import socket
from pynput.keyboard import Key, Controller
import time
import os

keyboard = Controller()


def moveRestPos(rest_pos, dx, dy, dz):
    str_out = ' '
    for i in xrange(0,len(rest_pos)) :
        str_out= str_out + ' ' + str(rest_pos[i][0]+dx)
        str_out= str_out + ' ' + str(rest_pos[i][1]+dy)
        str_out= str_out + ' ' + str(rest_pos[i][2]+dz)
    return str_out

def rotateRestPos(rest_pos,rx,centerPosY,centerPosZ):
    str_out = ' '
    for i in xrange(0,len(rest_pos)) :
        newRestPosY = (rest_pos[i][1] - centerPosY)*math.cos(rx) - (rest_pos[i][2] - centerPosZ)*math.sin(rx) +  centerPosY
        newRestPosZ = (rest_pos[i][1] - centerPosY)*math.sin(rx) + (rest_pos[i][2] - centerPosZ)*math.cos(rx) +  centerPosZ
        str_out= str_out + ' ' + str(rest_pos[i][0])
        str_out= str_out + ' ' + str(newRestPosY)
        str_out= str_out + ' ' + str(newRestPosZ)
    return str_out

class controller(Sofa.PythonScriptController):





    def initGraph(self, node):

            self.node = node
            self.index = 0
            self.actuatorNode=self.node.getChild('actuator')
            self.pressureConstraint1Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity3')
            self.pressureConstraint2Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity4')
            self.centerPosY = 70
            self.centerPosZ = 0
            self.rotAngle = 0

    def onKeyPressed(self,c):
            self.dt = self.node.findData('dt').value
            incr = self.dt*1000.0;

            self.MecaObject1=self.actuatorNode.ElasticMaterialObject.getObject('dofs');
            self.MecaObject2=self.actuatorNode.ElasticMaterialObject.getObject('dofs');

            self.pressureConstraint1 = self.pressureConstraint1Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint2 = self.pressureConstraint2Node.getObject('SurfacePressureConstraint')

            #if (c == "Z"):
            if ord(c)==90:
                print 'left'
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] + 0.01
                if pressureValue > 1:
                    pressureValue = 1
                self.pressureConstraint1.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] - 0.01
                if pressureValue < 0:
                    pressureValue = 0
                self.pressureConstraint2.findData('value').value = str(pressureValue)

            #if (c == "X"):
            if ord(c)==88:
                print 'right'
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] + 0.01
                if pressureValue > 1:
                    pressureValue = 1
                self.pressureConstraint2.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] - 0.01
                if pressureValue < 0:
                    pressureValue = 0
                self.pressureConstraint1.findData('value').value = str(pressureValue)

            #if (c == "C"):
            #if ord(c)==67:
            #    print 'increase'
            #    pressureValue = self.pressureConstraint1.findData('value').value[0][0] + 0.01
            #    if pressureValue > 0.6:
            #        pressureValue = 0.6
            #    self.pressureConstraint1.findData('value').value = str(pressureValue)
            #    pressureValue = self.pressureConstraint2.findData('value').value[0][0] + 0.01
            #    if pressureValue > 0.6:
            #        pressureValue = 0.6
            #    self.pressureConstraint2.findData('value').value = str(pressureValue)

            #if (c == "B"):
            #if ord(c)==66:
            #    print 'squeezing...'
            #    pressureValue = self.pressureConstraint1.findData('value').value[0][0] - 0.01
            #    if pressureValue < 0:
            #        pressureValue = 0
            #    self.pressureConstraint1.findData('value').value = str(pressureValue)
            #    pressureValue = self.pressureConstraint2.findData('value').value[0][0] - 0.01
            #    if pressureValue < 0:
            #        pressureValue = 0
            #    self.pressureConstraint2.findData('value').value = str(pressureValue)
                

            # UP key :
            if ord(c)==19:
                test1 = moveRestPos(self.MecaObject1.rest_position, 3.0, 0.0, 0.0)
                self.MecaObject1.findData('rest_position').value = test1
                test2 = moveRestPos(self.MecaObject2.rest_position, 3.0, 0.0, 0.0)
                self.MecaObject2.findData('rest_position').value = test2


            # DOWN key : rear
            if ord(c)==21:
                test = moveRestPos(self.MecaObject1.rest_position, -3.0, 0.0, 0.0)
                self.MecaObject1.findData('rest_position').value = test
                test = moveRestPos(self.MecaObject2.rest_position, -3.0, 0.0, 0.0)
                self.MecaObject2.findData('rest_position').value = test


            # LEFT key : left
            if ord(c)==20:
                dy = 3.0*math.cos(self.rotAngle)
                dz = 3.0*math.sin(self.rotAngle)
                test = moveRestPos(self.MecaObject1.rest_position, 0.0, dy, dz)
                self.MecaObject1.findData('rest_position').value = test
                test = moveRestPos(self.MecaObject2.rest_position, 0.0, dy, dz)
                self.MecaObject2.findData('rest_position').value = test
                self.centerPosY = self.centerPosY + dy
                self.centerPosZ = self.centerPosZ + dz

            # RIGHT key : right
            if ord(c)==18:
                dy = -3.0*math.cos(self.rotAngle)
                dz = -3.0*math.sin(self.rotAngle)
                test = moveRestPos(self.MecaObject1.rest_position, 0.0, dy, dz)
                self.MecaObject1.findData('rest_position').value = test
                test = moveRestPos(self.MecaObject2.rest_position, 0.0, dy, dz)
                self.MecaObject2.findData('rest_position').value = test
                self.centerPosY = self.centerPosY + dy
                self.centerPosZ = self.centerPosZ + dz

            # a key : direct rotation
            if (ord(c) == 65):
                test = rotateRestPos(self.MecaObject1.rest_position, math.pi/16, self.centerPosY,self.centerPosZ)
                self.MecaObject1.findData('rest_position').value = test
                test = rotateRestPos(self.MecaObject2.rest_position, math.pi/16, self.centerPosY,self.centerPosZ)
                self.MecaObject2.findData('rest_position').value = test
                self.rotAngle = self.rotAngle + math.pi/16

            # q key : indirect rotation
            if (ord(c) == 81):
                test = rotateRestPos(self.MecaObject1.rest_position, -math.pi/16, self.centerPosY,self.centerPosZ)
                self.MecaObject1.findData('rest_position').value = test
                test = rotateRestPos(self.MecaObject2.rest_position, -math.pi/16, self.centerPosY,self.centerPosZ)
                self.MecaObject2.findData('rest_position').value = test
                self.rotAngle = self.rotAngle - math.pi/16


    def onEndAnimationStep(self, dt):
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.connect(('0.0.0.0',7777))

        #sock.send('I am here')
        #ack = sock.recv(1024)
        #print(ack)
        #sock.close()

        # Save screenshots
        index = self.index
        path = "/home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots"
        command = "mv /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/* /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/" + str(index) + ".png"
        #os.system(command)

        self.index = self.index + 1
        print("index: ", self.index)
        # print("dt: ", dt)
        return


  
