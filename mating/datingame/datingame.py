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


#
# USAGE:
#
# For the proyect in question, the following commands were run once for each
# stragegy:
#
# >>> from datingame import *
# >>> results = multiSim(100)
# >>> processed = processResults(results)
#
# Remember, on these simulations, the suitors could proceed according to two
# different strategies, that we coined SETTLER and REACHER, in honor to the
# 13th episode of the fifth season of How I met your mother.
#
# If you are going to run this code, remember to change the STRATEGY line
# accodingly.
#



#############
#############
##         ##
## IMPORTS ##
##         ##
#############
#############
from random import randint, shuffle
import multiprocessing as mp
import pdb


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################

SCORERANGE = 10
TAU = 1



SETTLER = 'SETTLER'
REACHER = 'REACHER'

# STRATEGY  = REACHER
STRATEGY  = SETTLER



DESCORE  = 0 # Position of the actual desireability score.
ASSCORE  = 1 # Position of the self assessed desirability score list.
SCORELST = 2 # Position of the list of the scores of the individuals who where
             # proposed for a given suitor.
RESPLIST = 3 # Position of the list of the responses received by a suitor.
PROPHIST = 2 # Position of the proposal history list.
PROPLIST = 3 # Position of the proposal list.


#############
#############
##         ##
## METHODS ##
##         ##
#############
#############


def runSimulation(idx):
    dagame = DatingGame(500,500,25)
    dagame.run()
    st = dagame.doStatistics([10,25])
    return st


def multiSim(L):
    indices = list(range(L))
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(runSimulation, [idx for idx in indices])
    return results

def processResults(results):
    K = len(results[0][0][0])
    N = len(results[0][0])
    M = len(results[0])
    R = len(results)
    processed = [[[0 for k in range(K)] for n in range(N)] for m in range(M)]
    for result in results:
        for k in range(K):
            for n in range(N):
                for m in range(M):
                    processed[m][n][k] += result[m][n][k]
    for k in range(K):
        for n in range(N):
            for m in range(M):
                processed[m][n][k] /= R
    return processed




#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
class DatingGame:
    # This class it trying to implement the game.

    ###########
    # CREATOR #
    ###########
    def __init__(self,suitors,pursued,cycles):
        self._suitorN  = suitors
        self._pursuedM = pursued
        self._cycleK   = cycles
        actual = [randint(0,SCORERANGE) for k in range(suitors)]
        assess = [randint(0,SCORERANGE) for k in range(suitors)]
        self._suitors = [
                            [actual[k], [assess[k]], [], [] ]
                            for k in range (suitors)
                        ]
        actual = [randint(0,SCORERANGE) for k in range(pursued)]
        assess = [randint(0,SCORERANGE) for k in range(pursued)]
        self._pursued = [
                            [actual[k], [assess[k]], [], [] ]
                            for k in range (pursued)
                        ]

    ###########
    # METHODS #
    ###########
    def makeProposals(self):
        # This method goes through the entire list of suitors, and analizes
        # who should the suitor propose to.
        for n in range(self._suitorN):
            courtingList = list(range(self._pursuedM))
            shuffle(courtingList)
            scoreS = self._suitors[n][ASSCORE][-1]
            for m in courtingList:
                scoreP = self._pursued[m][DESCORE]
                if STRATEGY == SETTLER:
                    if 0 <= scoreP-scoreS <= TAU:
                        self._pursued[m][PROPLIST].append(n)
                        self._suitors[n][SCORELST].append(scoreP)
                        break
                else:
                    if scoreS <= scoreP:
                        self._pursued[m][PROPLIST].append(n)
                        self._suitors[n][SCORELST].append(scoreP)
                        break


    def considerProposals(self):
        for m in range(self._pursuedM):
            suitorsList = self._pursued[m][PROPLIST]
            if len(suitorsList) > 0:
                myScore = self._pursued[m][ASSCORE][-1]
                shuffle(suitorsList)
                currentScore = -1
                maxScore     = -1
                maxChoice    = -1
                for n in suitorsList:
                    currentScore = self._suitors[n][DESCORE]
                    if currentScore > maxScore:
                        if maxChoice >= 0:
                            self._suitors[maxChoice][RESPLIST].append(0)
                        maxChoice = n
                        maxScore = currentScore
                    else:
                        self._suitors[n][RESPLIST].append(0)
                if maxChoice >= 0:
                    self._suitors[maxChoice][RESPLIST].append(1)
            self._pursued[m][PROPHIST].append(self._pursued[m][PROPLIST])
            self._pursued[m][PROPLIST] = []


    def updateScores(self):
        for n in range(self._suitorN):
            # Let's first update the scores of the suitors.
            myScore = self._suitors[n][ASSCORE][-1]
            if self._suitors[n][RESPLIST][-1] == 1:
                if self._suitors[n][SCORELST][-1] > myScore:
                    if myScore < SCORERANGE:
                        myScore += 1
            elif self._suitors[n][SCORELST][-1] <= myScore:
                myScore -= 1
            self._suitors[n][ASSCORE].append(myScore)
        for m in range(self._pursuedM):
            # Let's update now the scores of the pursued.
            myScore = self._pursued[m][ASSCORE][-1]
            if len(self._pursued[m][PROPHIST][-1]) > 0:
                if max(self._pursued[m][PROPHIST][-1]) > myScore:
                    if myScore < SCORERANGE:
                        myScore += 1
                elif max(self._pursued[m][PROPHIST][-1]) < myScore:
                    if myScore > 0:
                        myScore -= 1
            elif myScore > 0:
                myScore -= 1
            myScore = self._pursued[m][ASSCORE].append(myScore)


    def doCycle(self):
        self.makeProposals()
        self.considerProposals()
        self.updateScores()


    def run(self):
        for k in range(self._cycleK):
            self.doCycle()


    def doStatistics(self,values):
        statistics = []
        ofPursued = []
        ofSuitors = []
        for val in values:
            stats = [[] for k in range(SCORERANGE + 1)]
            for suitor in self._suitors:
                stats[suitor[DESCORE]].append(suitor[ASSCORE][val])
            suiStats = [sum(aStat)/len(aStat) for aStat in stats]
            ofSuitors.append(suiStats)
            stats = [[] for k in range(SCORERANGE + 1)]
            for pursued in self._pursued:
                stats[pursued[DESCORE]].append(pursued[ASSCORE][val])
            purStats = [sum(aStat)/len(aStat) for aStat in stats]
            ofPursued.append(purStats)
        statistics.append(ofSuitors)
        statistics.append(ofPursued)
        return statistics
