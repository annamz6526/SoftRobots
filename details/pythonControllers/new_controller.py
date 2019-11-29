#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import socket
import time
import os


class controller(Sofa.PythonScriptController):





    def initGraph(self, node):

            self.node = node
            self.index = 0
            self.actuatorNode=self.node.getChild('actuator')
            self.pressureConstraint3Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity1')
            self.pressureConstraint4Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity2')
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
            self.pressureConstraint3 = self.pressureConstraint3Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint4 = self.pressureConstraint4Node.getObject('SurfacePressureConstraint')


            upper = 1
            #if (c == "Z"):
            if ord(c)==90:
                print 'left'
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint1.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] - 0.01
                # if pressureValue < 0:
                #     pressureValue = 0
                self.pressureConstraint2.findData('value').value = str(pressureValue)

            #if (c == "X"):
            if ord(c)==88:
                print 'right'
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint2.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] - 0.01
                #if pressureValue < 0:
                #    pressureValue = 0
                self.pressureConstraint1.findData('value').value = str(pressureValue)

            #if (c == "Q"):
            if ord(c)==81:
                print 'left'
                pressureValue = self.pressureConstraint3.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint3.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint4.findData('value').value[0][0] - 0.01
                # if pressureValue < 0:
                #     pressureValue = 0
                self.pressureConstraint4.findData('value').value = str(pressureValue)

            #if (c == "W"):
            if ord(c)==87:
                print 'right'
                pressureValue = self.pressureConstraint4.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint4.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint3.findData('value').value[0][0] - 0.01
                #if pressureValue < 0:
                #    pressureValue = 0
                self.pressureConstraint3.findData('value').value = str(pressureValue)


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
        #nodePos = self.actuatorNode.ElasticMaterialObject.getObject('dofs').position[0]
        #print("nodePos: ", nodePos)

        #self.index = self.index + 1
        #print("index: ", self.index)
        # print("dt: ", dt)
        return


  
