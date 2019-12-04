#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import socket
import time
import os
import math


class controller(Sofa.PythonScriptController):





    def initGraph(self, node):

            self.node = node
            self.index = 0
            self.cubeNode=self.node.getChild('cube')
            self.actuatorNode=self.node.getChild('actuator')
            self.pressureConstraint3Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity1')
            self.pressureConstraint4Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity2')
            self.pressureConstraint1Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity3')
            self.pressureConstraint2Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity4')
            self.lastGoalDistance = 0
            self.avgGoalDelta = 0
            self.rewardHistory = 0
            self.collision = False
            self.maxEpisodeLength =100;
            self.endEpisode = False

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
                if pressureValue < 0:
                    pressureValue = 0
                self.pressureConstraint2.findData('value').value = str(pressureValue)

            #if (c == "X"):
            if ord(c)==88:
                print 'right'
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint2.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] - 0.01
                if pressureValue < 0:
                    pressureValue = 0
                self.pressureConstraint1.findData('value').value = str(pressureValue)

            # UP key :
            if ord(c)==19:
                print 'long'
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint1.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] + 0.01
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint2.findData('value').value = str(pressureValue)


            # DOWN key : rear
            if ord(c)==21:
                print 'short'
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] - 0.01
                if pressureValue < 0:
                    pressureValue = 0
                self.pressureConstraint2.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] - 0.01
                if pressureValue < 0:
                    pressureValue = 0
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
        # Save screenshots
        index = self.index
        path = "/home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots"
        command = "mv /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/* /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/" + str(index) + ".png"
        #os.system(command)

        self.index = self.index + 1
        print("index: ", self.index)
        # print("dt: ", dt)

        # position of the middle point
        nodePos = self.actuatorNode.ElasticMaterialObject.getObject('dofs').position[665]
        nodePosX = nodePos[0]
        nodePosY = nodePos[1]
        nodePosZ = nodePos[2]
        #print("nodePos: ", nodePosX, nodePosY, nodePosZ)

        # position of the cube
        cubePos=self.cubeNode.MechanicalObject.findData('position').value;
        cubePosX = cubePos[0][0]
        cubePosY = cubePos[0][1]
        cubePosZ = cubePos[0][2]
        #print("cube position: ", cubePosX, cubePosY, cubePosZ)

        # distance
        distGoal = (cubePosX - nodePosX)**2 + (cubePosZ - nodePosZ)**2;
        distGoal = math.sqrt(distGoal)
        #print("distGoal: ", distGoal)

        # collision detection
        if (distGoal < 5):
            self.collision = True
            self.endEpisode = True

        # interim rewards
        alpha = 0.3
        REWARD_MULT = 200
        

        if index > 1:
            distDelta = self.lastGoalDistance - distGoal;
            self.avgGoalDelta = (self.avgGoalDelta * alpha) + (distDelta * (1.0 - alpha));
            self.lastGoalDistance = distGoal;

        if self.collision:
            self.rewardHistory = 500
        else:
            self.rewardHistory = self.avgGoalDelta * REWARD_MULT
        #print("rewardHistory: ", self.rewardHistory)

        # update endEpisode
        if index > self.maxEpisodeLength:
            self.endEpisode = True
        #print("endEpisode: ", self.endEpisode)

        if self.endEpisode:
            self.index = 0
            self.lastGoalDistance = 0
            self.avgGoalDelta = 0
            self.rewardHistory = 0
            self.collision = False
            self.endEpisode = False
            self.node.reset()

        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.connect(('0.0.0.0',7777))

        #sock.send('I am here')
        #ack = sock.recv(1024)
        #print(ack)
        #sock.close()
        return


  
