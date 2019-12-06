#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Sofa
import math
import socket
import time
import os
import math
import json
from pynput.keyboard import Key, Controller

keyboard = Controller()
actions = ['top_left', 'top_right','top_up', 'top_down', 'bottom_left', 'bottom_right', 'bottom_up', 'bottom_down']

def sendMessageOnly(sock, msg, ip, port):
    msg = json.dumps(msg).encode('utf-8')
    sock.sendto(msg, (ip, port))

class controller(Sofa.PythonScriptController):

    def onLoaded(self, node):
        # with keyboard.pressed(Key.shift):
        #     keyboard.press('v')
        #     keyboard.release('v')
        # node.getRootContext().animate = True
        server_addr = ('', 7777)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((server_addr))

    def listenToEnv(self, server_addr):
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.bind((server_addr))
        print("here")
        while True:
            received, addr = self.sock.recvfrom(1024)
            data = json.loads(received.decode('utf-8'))
            state = data['state']
            if state == 'reset':
                #TODO reset and send image 
                print(data)
                # self.index = 0
                self.lastGoalDistance = 0
                self.avgGoalDelta = 0
                self.rewardHistory = 0
                self.collision = False
                self.node.reset()
                data = {
                    'imgName' : '/home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/' + str(self.episode) + "_" + str(self.index) + '.png',
                    'reward' : None
                }
                print(data)
                sendMessageOnly(self.sock, data, addr[0], addr[1])
                self.episode = self.episode + 1
                self.index = 0
                break
            elif state == 'step':
                #TODO actions and send image 
                print(data['action'])
                self.execute(data['action'])
                data['action']
                data = {
                    'imgName' : '/home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/' + str(self.episode) + "_" + str(self.index) + '.png',
                    'reward' : self.rewardHistory,
                    'done' : self.endEpisode
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

    def onKeyPressed(self,c):
            self.dt = self.node.findData('dt').value
            incr = self.dt*1000.0;

            self.MecaObject1=self.actuatorNode.ElasticMaterialObject.getObject('dofs');
            self.MecaObject2=self.actuatorNode.ElasticMaterialObject.getObject('dofs');

            self.pressureConstraint1 = self.pressureConstraint1Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint2 = self.pressureConstraint2Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint3 = self.pressureConstraint3Node.getObject('SurfacePressureConstraint')
            self.pressureConstraint4 = self.pressureConstraint4Node.getObject('SurfacePressureConstraint')


            upper = 0.2
            bottom = -0.2
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


    def onEndAnimationStep(self, dt):
        # Save screenshots
        #path = "/home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots"
        #if self.index == 0:
        #    command = "rm /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/*"
        #else:
        # if self.index > 0:
        #     command = "mv /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/screenshots/* /home/zshen15/SOFA_v19.06.99_custom_Linux_v5.1/new_screenshots/" + str(self.episode) + "_" + str(self.index) + ".png"
        #     print("command: " ,command)
        #     os.system(command)

        if self.index > 0:
            server_addr = ('', 7777)
            #self.listenToEnv(server_addr)

        self.index = self.index + 1
        print("index: ", self.index)

        return

    def execute(self, action):
        upper = 1
        bottom = -1
        pressure_change = 0.01

        if action == 0:
            print 'top_left'
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint3.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint4.findData('value').value = str(pressureValue)
        elif action == 1:
            print 'top_right'
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint4.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint3.findData('value').value = str(pressureValue)
        elif action == 2:
            print 'top_up'
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint3.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint4.findData('value').value = str(pressureValue)
        elif action == 3:
            print 'top_down'
            pressureValue = self.pressureConstraint3.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint3.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint4.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint4.findData('value').value = str(pressureValue)
        elif action == 4:
            print 'bottom_left'
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint2.findData('value').value = str(pressureValue)
        elif action == 5:
            print 'bottom_right'
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint2.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint1.findData('value').value = str(pressureValue)
        elif action == 6:
            print 'bottom_up'
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] + pressure_change
            if pressureValue > upper:
                pressureValue = upper
            self.pressureConstraint2.findData('value').value = str(pressureValue)
        elif action == 7:
            print 'bottom_down'
            pressureValue = self.pressureConstraint1.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint1.findData('value').value = str(pressureValue)
            pressureValue = self.pressureConstraint2.findData('value').value[0][0] - pressure_change
            if pressureValue < bottom:
                pressureValue = bottom
            self.pressureConstraint2.findData('value').value = str(pressureValue)

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
        
        print("index: ", self.index)
        if self.index > 0:
            distDelta = self.lastGoalDistance - distGoal;
            print("distDelta: ", distDelta)
            self.avgGoalDelta = (self.avgGoalDelta * alpha) + (distDelta * (1.0 - alpha));
            self.lastGoalDistance = distGoal;

        if self.collision:
            self.rewardHistory = 500
        else:
            self.rewardHistory = self.avgGoalDelta * REWARD_MULT
        print("rewardHistory: ", self.rewardHistory)