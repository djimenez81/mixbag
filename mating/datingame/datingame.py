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
from random import randint, shuffle


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################
SUITOR     = 'SUITOR'
PURSUER    = 'PURSUER'
SCORERANGE = 10
TAU = 1
PERSV = 3 # Perseverance Parameter
SETTLER = 'SETTLER'
REACHER = 'REACHER'

STRATEGY  = REACHER



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

class Dater:
    # This class is a simple container for the different attributes that a dater
    # has on this experiment. Most of the behavior will be contained in the
    # larger class, with the exception of the updating of the desirability score.

    ##############
    # ATTRIBUTES #
    ##############
    _desirabilityScore = 0
    _genderIdentity    = ''
    _proposalsReceived = []
    _proposalHistory   = []
    _proposalResponse  = []
    _selfAssessedDesirability = []
    _proposalScores    = []

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
    def getGender(self):
        return self._genderIdentity

    def getDesirabilityScore(self):
        return self._desirabilityScore

    def getProposalsReceived(self):
        return self._proposalsReceived

    def getProposalHistory(self):
        return self._proposalHistory

    def getProposalResponses(self):
        return self._proposalResponse

    def getSelfAssessedDesirability(self):
        return self._selfAssessedDesirability

    def getCurrentSelfAssessedDesirability(self):
        return self._selfAssessedDesirability[-1]

    def setNewSelfAssessedScore(self,score):
        self._selfAssessedDesirability.append(score)

    def addProposal(self,proposal):
        self._proposalsReceived.append(proposal)

    def add2ProposalHistory(self):
        self._proposalHistory.append(self._proposalsReceived)
        self._proposalsReceived = []

    def addProposalScore(self,k):
        self._proposalScores.append(k)

    def addProposalResponse(self,k):
        self._proposalResponse.append(k)


    ###########
    # METHODS #
    ###########
    def updateSelfAssessedDesirabilityScore(self):
        scores    = self.getSelfAssessedDesirability()
        responses = self.getProposalResponses()
        myScore   = self.getCurrentSelfAssessedDesirability()
        # NOTE: scores and responses should have the same length. It might
        #       be a good idea to check this, and correct it if not.
        if len(responses) >= PERSV:
            # if there are not yet enough data points, then the suitor will
            # not reconsider its score.
            if sum(responses[-PERSV:]) == 0:
                # In this case, the last PERSV cycles, the suitor has been
                # rejected. We need to analize if the scores has been the
                # same during all these cyces.
                if len(set(scores[-PERSV:])) == 1:
                    # In this case, the score has not changed in the last
                    # PERSV cycles, and thus, needs to change.
                    if myScore > 1:
                        myScore -= 1
            elif responses[-1] == 1 and scores[-1] > myScore:
                # In this case, the suitor has been accepted by a mate with
                # a higher score than himself in the last cycle.
                myScore += 1
        self.setNewSelfAssessedScore(myScore)





class Datingame:
    # This class contains the logic of the simulation, and most of the behavior.

    ##############
    # ATTRIBUTES #
    ##############
    _suitorN  = 0
    _pursuedM = 0
    _cycleK   = 0
    _suitors  = []
    _pursued  = []

    ###########
    # CREATOR #
    ###########
    def __init__(self,suitors,pursued,cycles):
        self._suitorN  = suitors
        self._pursuedM = pursued
        self._cycleK   = cycles

        for n in range(suitors):
            actual   = randint(0,SCORERANGE)
            assessed = randint(0,SCORERANGE)
            self._suitors.append(Dater(SUITOR,actual,assessed))

        for m in range(pursued):
            actual   = randint(0,SCORERANGE)
            assessed = randint(0,SCORERANGE)
            self._pursued.append(Dater(SUITOR,actual,assessed))

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getSuitors(self):
        return self._suitors

    def getPursued(self):
        return self._pursued

    def getSuitorNumber(self):
        return self._suitorN

    def getPursuedNumber(self):
        return self._pursuedM

    def getCycles(self):
        return self._cycleK

    ###########
    # METHODS #
    ###########
    def makeProposals(self):
        for n in range(self._suitorN):
            M = self._pursuedM
            courtingList = list(range(M))
            shuffle(courtingList)
            scoreS = self._suitors[n].getCurrentSelfAssessedDesirability()
            k = 0
            flag = True
            while flag:
                scoreP = self._pursued[courtingList[k]
                            ].getCurrentSelfAssessedDesirability()
                if STRATEGY == SETTLER:
                    if abs(scoreP-scoreS) <= TAU:
                        self._pursued[courtingList[k]].addProposal(courtingList[k])
                        self._suitors[n].addProposalScore(scoreP)
                        flag = False
                    else:
                        k += 1
                        if k >= M:
                            flag = False
                            self._suitors[n].addProposalScore(-1)
                            self._suitors[n].addProposalResponse(0)
                else:
                    if scoreS <= scoreP:
                        self._pursued[courtingList[k]].addProposal(courtingList[k])
                        self._suitors[n].addProposalScore(scoreP)
                        flag = False
                    else:
                        k += 1
                        if k >= M:
                            flag = False
                            self._suitors[n].addProposalScore(-1)
                            self._suitors[n].addProposalResponse(0)


    def considerProposals(self):
        for m in range(self._pursuedM):
            suitorsList = self._pursued[m].getProposalsReceived()
            L = len(suitorsList)
            if L == 0:
                # This is the case where this particular pursued individual was
                # not proposition by anyone.
                self._pursued[m].add2ProposalHistory()
                self._pursued[m].addProposalResponse(0)
            else:
                # The suitor list should be randomized in order to avoid giving
                # preference because of order.
                myScore = self._pursued[m].getCurrentSelfAssessedDesirability()
                shuffle(suitorsList)
                currentScore = -1
                maxScore = -1
                maxChoice = -1
                for n in range(L):
                    currentScore = self._suitors[suitorsList[n]].getDesirabilityScore()
                    if currentScore > maxScore:
                        if maxChoice >= 0:
                            self._suitors[maxChoice].addProposalResponse(0)
                        maxChoice = suitorsList[n]
                        maxScore  = currentScore
                    else:
                        self._suitors[suitorsList[n]].addProposalResponse(0)
                # self._pursued9
                if maxChoice >= 0:
                    self._pursued[m].add2ProposalHistory()
                    self._pursued[m].addProposalScore(maxScore)
                    if maxScore >= myScore:
                        self._suitors[maxChoice].addProposalResponse(1)
                        self._pursued[m].addProposalResponse(1)
                    else:
                        self._suitors[maxChoice].addProposalResponse(0)
                        self._pursued[m].addProposalResponse(0)


    def updateScores(self):
        for n in range(self._suitorN):
            self._suitors[n].updateSelfAssessedDesirabilityScore()
        for m in range(self._pursuedM):
            self._pursued[m].updateSelfAssessedDesirabilityScore()


    def doCycle(self):
        self.makeProposals()
        self.considerProposals()
        self.updateScores()

    def run(self):
        for k in range(self._cycleK):
            self.doCycle()
