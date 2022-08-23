#!/usr/bin/python
# module colas

# This module contains some methods developed to aid on the queue problem
# related to the costums at the north borther
#
# Copyright (c) 2022 Universidad de Costa Rica.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   - Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   - Neither the name of the <organization> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL DAVID JIMENEZ BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Researchers:
#         David Jimenez <david.jimenezlopez@ucr.ac.cr>
#         Susana Wong   <susana.wong@ucr.ac.cr>
#

###############
###############
##           ##
##  IMPORTS  ##
##           ##
###############
###############
import pandas as pd
import numpy as np
import math


######################
######################
##                  ##
## GLOBAL VARIABLES ##
##                  ##
######################
######################

# Sequence TYPES
COLA    = "COLA"
PROCESO = "PROCESO"
DESVIO  = "DESVIO"


#############
#############
##         ##
## METHODS ##
##         ##
#############
#############



#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
class Cola:
    # This class implements a simple FIFO queue with a maximum number of
    # transports that can be absorbed at any time.

    ##############
    # ATTRIBUTES #
    ##############
#    _maximumCapacity = 0

    ###########
    # CREATOR #
    ###########
    def __init__(self, colaName, maxCap):
        self._name = colaName
        self._maximumCapacity = maxCap
        self._queueContent = []
        self._myType = COLA


    #######################
    # GETTERS AND SETTERS #
    #######################
    def getName(self):
        return self._name

    def getMaximumCapacity(self):
        return self._maximumCapacity

    def getQueue(self):
        return self._queueContent

    def setName(self,nombre):
        self._name = nombre

    def setMaximumCapacity(self,maxCap):
        self._maximumCapacity = maxCap

    def getMyType(self):
        return self._myType


    ###########
    # METHODS #
    ###########
    def isThereSpace():
        # This methods verifies that there is space in the queue.
        return len(self._queueContent) < self._maximumCapacity

    def addTransport(self,transport):
        # This method adds a transpor to the beginning of the queue.
        if len(self._queueContent) < self._maximumCapacity:
            self._queueContent.append(transport)
        else:
            print("This is a problem: There is no more space")

    def passTransport(self):
        # This method takes the first transport in the queue.
        return self._queueContent.pop(0)

    def isQueueEmpty(self):
        # This method returns true if and only if the queue is empty at the
        # moment.
        return len(self._queueContent) == 0


class Proceso:
    # This class implements a particular process in the simulation. It simply
    # retains a maximum number of transports at a time, each for a set number of
    # cycles, each computed when the transport arrives, according to a normal
    # distribution where the mean and standard deviation are given and fixed.

    ##############
    # ATTRIBUTES #
    ##############

    ###########
    # CREATOR #
    ###########
    def __init__(self,name,capacity):
        self._name = name
        self._capacity = capacity
        self._attendingList = []
        self._myType = PROCESO

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getCapacity(self):
        return self._capacity

    def setCapacity(self,capacity):
        self._capacity = capacity

    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    def getMyType(self):
        return self._myType

    ###########
    # METHODS #
    ###########
    def isThereSpace(self):
        # This method vefiries if there is space in the queue
        return len(self._present) < self._capacity


class Transporte:
    # This class implements a transport. For our purposes, it is simply a place
    # holder that records how long it takes it to pass through each process and
    # how long is the wait on each queue.

    ##############
    # ATTRIBUTES #
    ##############

    ###########
    # CREATOR #
    ###########
    def __init__(self,code):
        self._code = code
        self._watingTimes = []
        self._readyToMove = True
        self._currentWait = 0
        self._processWait = 0

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getCode(self):
        return self._code

    def getWaitingTimes(self):
        return self._watingTimes

    def getReadyToMove(self):
        return self._readyToMove

    def getCurrentWait(self):
        return self._currentWait

    def getProcessWait(self):
        return self._processWait

    def setCode(self,code):
        self._code = code

    def setWaitingTimes(self,waiting):
        self._watingTimes = waiting

    def setReadyToMove(self,ready):
        self._readyToMove = ready

    def setCurrentWait(self,current):
        self._currentWait = current

    def setProcessWait(self,processWait):
        self._processWait = processWait

    ###########
    # METHODS #
    ###########
    def liberate(self):
        # This method sets the transport ready to move when in a process.
        self._readyToMove = True

    def detain(self):
        # This method sets the transport as detained, that is, is not able to
        # move on the process until the time process waiting time is over.
        self._readyToMove = False

    def canMove(self):
        # This method returns True if the transport is able to move at the
        # specific time.
        return self._readyToMove

    def resetWait(self):
        # This method records the current wait time, and resets it to zero.
        self._watingTimes.append(self._currentWait)
        self._currentWait = 0


class DesvioAleatorio:
    # This class implements a point where a transport can either go for an
    # additional steo pr not.

    ##############
    # ATTRIBUTES #
    ##############

    ###########
    # CREATOR #
    ###########
    def __init__(self, name, chance):
        self._name = name
        self._chance = chance
        self._queueContent = []
        self._maximumCapacity = 1
        self._myType = DESVIO

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getMyType(self):
        return self._myType


    ###########
    # METHODS #
    ###########


class Simulacion:
    # This class implements the simulation proper. The sequence of processes,
    # random forks and queues should be placed in the order they are supposed to
    # be traversed.

    ##############
    # ATTRIBUTES #
    ##############

    ###########
    # CREATOR #
    ###########
    def __init__(self,transportNumber):
        self._transportNumber = transportNumber
        self._sequence = []
        self._currentTransportCount = 0
        self._backwardSequence = []
        self._operating = False

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getTransportNumber(self):
        return self._transportNumber

    def getSequence(self):
        return self._sequence

    def getCurrentTransportCount(self):
        return self._currentTransportCount

    def getBackwardSequence(self):
        return self._backwardSequence



    ###########
    # METHODS #
    ###########
    def isOperating(self):
        return self._operating

    def openOperation(self):
        self._operating = True

    def closeOperation(self):
        self._operating = False 

    def run(self):
        # This method contains most of the logic of the simulation, regulating
        # the flow of transport through the sequence of queues, forks and
        # processes.
        pass
