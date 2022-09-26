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

# Open and close tags
OPEN  = "OPEN"
CLOSE = "CLOSE"

# Decitions for whether
RETAINED = "RETAINED"
RELEASED = "RELEASED"
UNSTATED = "UNSTATED"



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
        # This method adds a transport to the beginning of the queue.
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

    def advanceClock(self):
        # This method advances the clock of all the transports currently in the
        # queue.
        for transport in self._queueContent:
            transport.advanceClock()

    def queueLength(self):
        # This method returns the number of elements currently in the queue.
        return len(self._queueContent)

    def addNewTransport(self,transport):
        # This method uses the transport method to be liberated (that means,
        # the transport can move at any time) and adds it to the queue.
        transport.liberate()
        self._queueContent.append(transport)

    def availableTransport(self):
        # This method returns true if there is at least one transport in the
        # queue that can move at the present time. As any transport in the queue
        # can move as soon as it is the first in line, it returns false if and
        # only if the queue is empty.
        return len(self._queueContent) > 0

    def liberateTransport(self):
        # This returns the first transport in the queue.
        transport = self._queueContent.pop(0)
        return transport


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
    def __init__(self,name,capacity, mean, stdev):
        self._name = name
        self._capacity = capacity
        self._attendingList = []
        self._myType = PROCESO
        self._mean = mean
        self._stdev = stdev

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
        return len(self._attendingList) < self._capacity

    def advanceClock(self):
        # This method advances the clock of all the transports currently in the
        # process.
        for transport in self._attendingList:
            transport.advanceClock()

    def queueLength(self):
        # This method returns the number of elements currently in the process.
        return len(self._attendingList)

    def availableTransport(self):
        # This method checks if any of the elements in the process has finished
        # and can move.
        available = False
        for transport in self._attendingList:
            available |= transport.canMove()

    def addNewTransport(self, transport):
        # This method adds a new transport to the process.
        time = max(1,np.random.normal(self._mean, self._stdev))
        transport.setProcessWait(time)
        transport.detain()
        self._attendingList.append(transport)

    def liberateTransport():
        index = -1
        k = 0
        while k < range(len(self._attendingList)) and index < 0:
            if self._attendingList[k].canMove():
                index = k
        transport = self._attendingList.pop(index)
        return transport

    def checkIfAnyoneIsDone(self):
        for transport in self._attendingList:
            transport.checkIfDone()


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
        self._decision = UNSTATED

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
    def isThereSpace(self):
        return len(self._queueContent) == 0

    def decide(self):
        # This method decides if the transport goes one way or the other.
        x = np.random.rand()
        if x < self._chance:
            self._decision = RETAINED
        else:
            self._decision = RELEASED

    def isRetained(self):
        return self._decision == RETAINED

    def release(self):
        self._decision == UNSTATED
        return self._queueContent.pop()

    def advanceClock(self):
        # This method advances the clock of all the transports currently in the
        # fork.
        for transport in self._queueContent:
            transport.advanceClock()

    def queueLength(self):
        # This method returns the number of elements currently in the queue.
        return len(self._queueContent)

    def availableTransport(self):
        # This method returns true if there is at least one transport in the
        # fork that can move at the present time. As there can be only one
        # transport in the fork, and  it can move immediately (but it can only
        # to the preset site given by the decision, the method returns false if
        # and only if the queue is empty.
        return len(self._queueContent) > 0

    def addNewTransport(self,transport):
        if np.random.uniform() < self._chance:
            self._decision = RETAINED
        else:
            self._decision = RELEASED
        transport.liberate()
        self._queueContent.append(transport)

    def liberateTransport(self):
        self._decision = UNSTATED
        transport = self._queueContent.pop()
        return transport




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
        self.resetWait()

    def detain(self):
        # This method sets the transport as detained, that is, is not able to
        # move on the process until the time process waiting time is over.
        self._readyToMove = False
        self.resetWait()

    def canMove(self):
        # This method returns True if the transport is able to move at the
        # specific time.
        return self._readyToMove

    def advanceClock(self):
        # This method advances the clock of the transport.
        self._currentWait += 1

    def resetWait(self):
        # This method records the current wait time, and resets it to zero.
        self._watingTimes.append(self._currentWait)
        self._currentWait = 0

    def checkIfDone(self):
        if self._processWait < self._currentWait:
            self.liberate()


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
        self._currentClockTime = 0
        self._cyclesPerPeriod = 0
        self._periodsPerDay = 1
        self._schedules = {}
        self._transportAdditionLambdas = []

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

    def getCyclesPerPeriod(self):
        return self._cyclesPerPeriod

    def getAdditionLambdas(self):
        return self._transportAdditionLambdas

    def setAdditionLambdas(self,lambdas):
        self._transportAdditionLambdas = lambdas

    ###########
    # METHODS #
    ###########
    def isOperating(self):
        # This method checks if, within the simulation, the services (processes)
        # are open at the time.
        return self._operating

    def openOperation(self):
        # This method opens the services within the simulation.
        self._operating = True

    def closeOperation(self):
        # This method closes the services within the simulation.
        self._operating = False

    def advanceClock(self):
        # This method simply advances the clock on the whole simulation. It
        # should be run at the end of each cycle.
        self._currentClockTime += 1
        for thing in self._sequence:
            thing.advanceClock()

    def addSequenceElement(self,element):
        self._sequence.append(element)

    def run(self):
        # This method contains most of the logic of the simulation, regulating
        # the flow of transport through the sequence of queues, forks and
        # processes.

        # We define the place where we will store the information
        resultTable = []

        # First we check if it is time to close or to open the place.
        N = self._currentClockTime // self._cyclesPerPeriod
        R = self._currentClockTime %  self._cyclesPerPeriod
        M = N % self._periodsPerDay

        if R == 0:
            if M in self._schedules[CLOSE]:
                self.closeOperation()
            else:
                self.openOperation()

        # Second, we add as many
        P = N % len(self._transportAdditionLambdas)
        L = self._transportAdditionLambdas[P]
        K = np.random.poisson(L)
        for k in range(K):
            if self._currentTransportCount < self._transportNumber:
                transport = Transporte(self._currentTransportCount)
                self._sequence[0].addNewTransport(transport)
                self._currentTransportCount += 1

        # Now, if the service is closed, all you have to do is to advance the
        # clock.
        if not self.isOperating():
            for estado in self._sequence:
                if estado.getMyType() == PROCESO:
                    estado.checkIfAnyoneIsDone()
            self.advanceClock()
        else:
            # This is the case where the service is actually operating.

            # First, for each transport on a process, we figure out if it is
            # done with it.
            for estado in self._sequence:
                if estado.getMyType() == PROCESO:
                    estado.checkIfAnyoneIsDone()

            # Second check if there are transports that are getting out of the
            # entire sequence. We assume that the last element in the sequence
            # is of class Proceso.
            while self._sequence[-1].availableTransport():
                transport = self._sequence[-1].liberateTransport()
                transport.resetWait()
                L = transport.getWaitingTimes()
                L.reverse()
                K = sum(L)
                L.append(K)
                L.append(self._currentClockTime)
                L.append(transport.getCode())
                L.reverse()
                resultTable.append(L)

            # Third, in a reverse the sequence to see if transports can move.
            k = len(self._sequence)
            while k > 1:
                k -= 1
                currentProcess = self._sequence[k]
                if currentProcess.isThereSpace():
                    indices = self._backwardSequence[k]
                    if len(indices) >1:
                        for index in indices:
                            previousProcess - self._sequence[index]
                            while currentProcess.isThereSpace() and \
                                    previousProcess.availableTransport():
                                transport = previousProcess.liberateTransport()
                                currentProcess.addNewTransport(transport)

                    else:
                        previousProcess = self._sequence[indices[0]]
                        while currentProcess.isThereSpace() and \
                               previousProcess.availableTransport():
                            transport = previousProcess.liberateTransport()
                            currentProcess.addNewTransport(transport)

            # In this case, the last thing to do is to advance the clock.
            self.advanceClock()

        # Finally, we check if the simulation run is over.
        if not self._currentTransportCount < self._transportNumber:
            totalTransportCount = 0
            # Do whatever we need to finish the run.
            for stage in self._sequence:
                totalTransportCount += stage.queueLength()
            if totalTransportCount == 0:
                return resultTable
        if self._currentClockTime > self._transportNumber**2:
            # This is a fail safe in case we are buggy.This section can be
            # deleted once tested.
            return resultTable
