#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import socket
import time
import os
import math
import json
import random
from pynput.keyboard import Key, Controller

keyboard = Controller()
actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

def sendMessageOnly(sock, msg, ip, port):
    msg = json.dumps(msg).encode('utf-8')
    sock.sendto(msg, (ip, port))

class controller(Sofa.PythonScriptController):

    def onLoaded(self, node):
        command = "rm -rf ~/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/*"
        os.system(command)
        with keyboard.pressed(Key.shift):
            keyboard.press('v')
            keyboard.release('v')
        node.getRootContext().animate = True
        server_addr = ('', 7777)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((server_addr))

    def listenToEnv(self, server_addr):
        while True:
            received, addr = self.sock.recvfrom(1024)
            data = json.loads(received.decode('utf-8'))
            state = data['state']
            if state == 'reset':
                #TODO reset and send image 
                #print(data)
                self.lastGoalDistance = 0
                self.avgGoalDelta = 0
                self.rewardHistory = 0
                self.node.reset()
                data = {
                    'imgName' : '~/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/' + str(self.episode) + "_" + str(self.index) + '.png',
                    'reward' : None
                }
                sendMessageOnly(self.sock, data, addr[0], addr[1])
                self.episode = self.episode + 1
                self.index = 0
                self.endEpisode = False
                self.maxmin = False
                self.touchGround = False
                reachable_area = [-30, 0, -100, 70, 5, -20]
                if self.collision == True:
                    x_range = range(reachable_area[0], reachable_area[3])
                    y_range = range(reachable_area[1], reachable_area[4])
                    z_range = range(reachable_area[2], reachable_area[5])
                    x_pos = random.sample(x_range, 1)
                    y_pos = random.sample(y_range, 1)
                    z_pos = random.sample(z_range, 1)
                    self.cubeNode.MechanicalObject.findData('position').value = str(x_pos[0]) + " " + str(y_pos[0]) + " " + str(z_pos[0]) + " " + "0 0 0 0"
                    #print("cube position: ", self.cubeNode.MechanicalObject.findData('position').value)
                else:
                    self.cubeNode.MechanicalObject.findData('position').value = str(self.previouscubePosX) + " " + str(self.previouscubePosY) + " " + str(self.previouscubePosZ) + " " + "0 0 0 0"
                self.collision = False
                self.lastGoalDistance = self.calculateDisGoal()
                break
            elif state == 'step':
                #TODO actions and send image 
                self.execute(data['action'])
                data = {
                    'imgName' : '~/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/' + str(self.episode) + "_" + str(self.index) + '.png',
                    'reward' : self.rewardHistory,
                    'done' : self.endEpisode,
                    'success' : self.collision
                }
                sendMessageOnly(self.sock, data, addr[0], addr[1])
                break
                
            else:
                pass
        # sock.close()

    def initGraph(self, node):
        self.node = node
        self.index = 0
        self.cubeNode=self.node.getChild('cube')
        self.actuatorNode=self.node.getChild('actuator')
        self.pressureConstraint3Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity1')
        self.pressureConstraint4Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity2')
        self.pressureConstraint1Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity3')
        self.pressureConstraint2Node = self.actuatorNode.ElasticMaterialObject.getChild('cavity4')
        self.pressureConstraint1 = self.pressureConstraint1Node.getObject('SurfacePressureConstraint')
        self.pressureConstraint2 = self.pressureConstraint2Node.getObject('SurfacePressureConstraint')
        self.pressureConstraint3 = self.pressureConstraint3Node.getObject('SurfacePressureConstraint')
        self.pressureConstraint4 = self.pressureConstraint4Node.getObject('SurfacePressureConstraint')
        self.lastGoalDistance = 0
        self.avgGoalDelta = 0
        self.rewardHistory = 0
        self.collision = False
        #self.maxEpisodeLength =100
        self.endEpisode = False
        self.episode = 0
        self.maxmin = False
        self.touchGround = False
        self.previouscubePosX = 15
        self.previouscubePosY = 0
        self.previouscubePosZ = -70

    def onKeyPressed(self,c):
            self.dt = self.node.findData('dt').value
            incr = self.dt*1000.0;

            self.MecaObject1=self.actuatorNode.ElasticMaterialObject.getObject('dofs');
            self.MecaObject2=self.actuatorNode.ElasticMaterialObject.getObject('dofs');

            self.pressureConstraint1 = self.pressureConstraint1Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint2 = self.pressureConstraint2Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint3 = self.pressureConstraint3Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint4 = self.pressureConstraint4Node.getObject('SurfacePressureConstraint')


            upper = 0.8
            bottom = -0.8
            pressure_change = 0.005
            #if (c == "Z"):
            if ord(c)==90:
                print 'left'
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint1.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint2.findData('value').value = str(pressureValue)

            #if (c == "X"):
            if ord(c)==88:
                print 'right'
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint2.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint1.findData('value').value = str(pressureValue)

            # UP key :
            if ord(c)==19:
                print 'long'
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint1.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint2.findData('value').value = str(pressureValue)


            # DOWN key : rear
            if ord(c)==21:
                print 'short'
                pressureValue = self.pressureConstraint2.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint2.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint1.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint1.findData('value').value = str(pressureValue)

            #if (c == "Q"):
            if ord(c)==81:
                print 'left'
                pressureValue = self.pressureConstraint3.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint3.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint4.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint4.findData('value').value = str(pressureValue)

            #if (c == "W"):
            if ord(c)==87:
                print 'right'
                pressureValue = self.pressureConstraint4.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint4.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint3.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint3.findData('value').value = str(pressureValue)

            # LEFT key :
            if ord(c)==20:
                print 'long'
                pressureValue = self.pressureConstraint3.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint3.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint4.findData('value').value[0][0] + pressure_change
                if pressureValue > upper:
                    pressureValue = upper
                self.pressureConstraint4.findData('value').value = str(pressureValue)


            # RIGHT key : rear
            if ord(c)==18:
                print 'short'
                pressureValue = self.pressureConstraint3.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint3.findData('value').value = str(pressureValue)
                pressureValue = self.pressureConstraint4.findData('value').value[0][0] - pressure_change
                if pressureValue < bottom:
                    pressureValue = bottom
                self.pressureConstraint4.findData('value').value = str(pressureValue)


    def onEndAnimationStep(self, dt):
        # Save screenshots
        #path = "/home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots"
        #if self.index == 0:
        #    command = "rm /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/*"
        #else:
        if self.index > 0:
            command = "mv ~/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/* ~/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/" + str(self.episode) + "_" + str(self.index) + ".png"
            print("command: " ,command)
            os.system(command)

        if self.index > 0:
            server_addr = ('', 7777)
            self.listenToEnv(server_addr)

        self.index = self.index + 1
        #print("index: ", self.index)

        return

    def execute(self, action):
        upper = 0.8
        bottom = -0.8
        pressure_change = 0.02
        self.maxmin = False

        if action == 0:
            print 'top_left'
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint3.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint4.findData('value').value = str(pressureValue)
        elif action == 1:
            print 'top_right'
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint4.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint3.findData('value').value = str(pressureValue)
        elif action == 2:
            print 'top_up'
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint3.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint4.findData('value').value = str(pressureValue)
        elif action == 3:
            print 'top_down'
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint3.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint4.findData('value').value = str(pressureValue)
        elif action == 4:
            print 'bottom_left'
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint2.findData('value').value = str(pressureValue)
        elif action == 5:
            print 'bottom_right'
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint2.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint1.findData('value').value = str(pressureValue)
        elif action == 6:
            print 'bottom_up'
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
                self.maxmin = True
            self.pressureConstraint2.findData('value').value = str(pressureValue)
        elif action == 7:
            print 'bottom_down'
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
                self.maxmin = True
            self.pressureConstraint2.findData('value').value = str(pressureValue)

        distGoal = self.calculateDisGoal()

        # collision detectionendEpisode
        if (distGoal < 10):
            self.collision = True
            self.endEpisode = True

        # interim rewards
        alpha = 0.3
        REWARD_MULT = 150
        
        #print("index: ", self.index)
        if self.index == 0:
            self.lastGoalDistance = distGoal
        if self.index > 0:
            distDelta = self.lastGoalDistance - distGoal;
            print("lastGoalDistance: ", self.lastGoalDistance)
            print("distGoal: ", distGoal)
            print("distDelta: ", distDelta)
            self.avgGoalDelta = (self.avgGoalDelta * alpha) + (distDelta * (1.0 - alpha));
            self.lastGoalDistance = distGoal;

        if self.index > 1000:
            self.endEpisode = True

        if self.collision:
            self.rewardHistory = 500
        elif self.touchGround:
            self.rewardHistory = -300
            self.endEpisode = True
        elif self.maxmin:
            self.rewardHistory = -300
            self.endEpisode = True
        else:
            if self.endEpisode:
                self.rewardHistory = -300
            else:
                self.rewardHistory = self.avgGoalDelta * REWARD_MULT
        print("rewardHistory: ", self.rewardHistory)

    def calculateDisGoal(self):
        # position of the middle point
        nodePos = self.actuatorNode.ElasticMaterialObject.getObject('dofs').position[2934]
        nodePosX = nodePos[0]
        nodePosY = nodePos[1]
        nodePosZ = nodePos[2]
        if nodePosY < -50:
            self.touchGround = True
        #print("nodePos: ", nodePosX, nodePosY, nodePosZ)

        # position of the cube
        cubePos = self.cubeNode.MechanicalObject.findData('position').value;
        cubePosX = cubePos[0][0]
        cubePosY = cubePos[0][1]
        cubePosZ = cubePos[0][2]
        self.previouscubePosX = cubePosX
        self.previouscubePosY = cubePosY
        self.previouscubePosZ = cubePosZ
        #print("cube position: ", cubePosX, cubePosY, cubePosZ)

        # distance
        distGoal = (cubePosX - nodePosX)**2 + (cubePosZ - nodePosZ)**2;
        distGoal = math.sqrt(distGoal)
        #print("distGoal: ", distGoal)
        return distGoal