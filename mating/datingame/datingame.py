#!/usr/bin/python
# module datingame

# Copyright (c) 2019 Universidad de Costa Rica
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
# DISCLAIMED. IN NO EVENT SHALL UNIVERSIDAD DE COSTA RICA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Principal Investigator:
#         David Jimenez <david.jimenezlopez@ucr.ac.cr>



#############
#############
##         ##
## IMPORTS ##
##         ##
#############
#############
from random import randint


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################
SUITOR  = 'SUITOR'
PURSUER = 'PURSUER'



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

class dater:
    ##############
    # ATTRIBUTES #
    ##############
    _desirabilityScore = 0
    _genderIdentity    = ''
    _proposalsReceived = []
    _proposalHistory   = []
    _proposalResponse  = []
    _selfAssessedDesirability = []

    ###########
    # CREATOR #
    ###########
    def __init__(self,gIdentity,desScore,selfAssessedDes):
        self._genderIdentity    = gIdentity
        self._desirabilityScore = desScore
        self._selfAssessedDesirability = [selfAssessedDes]


    #######################
    # GETTERS AND SETTERS #
    #######################

    ###########
    # METHODS #
    ###########





class datingame:
    ##############
    # ATTRIBUTES #
    ##############
    _suitorN  = 0
    _pursuedM = 0
    _suitors  = []
    _pursued  = []
    _iterT    = 0

    ###########
    # CREATOR #
    ###########
    def __init__(self,N,M,T):
        self._suitorN  = N
        self._pursuedM = M
        self._iterT    = T
        for n in range(N):
            self._suitors.append(dater(SUITOR,randint(1,10),randint(1,10)))
        for m in range (M):
            self._suitors.append(dater(PURSUED,randint(1,10),randint(1,10)))



    #######################
    # GETTERS AND SETTERS #
    #######################

    ###########
    # METHODS #
    ###########
