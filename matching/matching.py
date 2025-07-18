#!/usr/bin/python
# module matching

# Copyright (c) 2022 David Jimenez
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
#         David Jimenez <djimenez81@gmail.com>


#
# USAGE:
#
#
# >>> from matching import *
#
#



#############
#############
##         ##
## IMPORTS ##
##         ##
#############
#############
from random import randint, shuffle
from copy import deepcopy
from math import sqrt
# import multiprocessing as mp
# import pdb


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################



#############
#############
##         ##
## METHODS ##
##         ##
#############
#############
# def methodName(attribute):
#     pass

def polyMatching(degrees,choices):
    # This method attempts to reproduce the Gale-Shapley algorithm for when:
    #  1 - Everyone can propose by or be proposed to anyone by themselves.
    #  2 - Not everyone is a suitable partner for someone else, this is, n might
    #      not consider k at all and would never be paired with them.
    #  3 - Each node has a maximum number of edges for which it can be an
    #      extreme.
    #
    # INPUT
    #  - degrees: list of the individual maximum degree of each node.
    #  - choices: The prioritized list of possible matches for a node.
    #
    # OUTPUT
    #  - matches: List of the matches given for each node.
    #
    flag = True
    N = len(degrees)
    choices   = [[k for k in choices[n] if n in choices[k]] for n in range(N)]
    matched   = [[] for n in range(N)]
    proposals = deepcopy(choices)
    maxima = [N for k in range(N)]
    K = 0
    while flag:
        for n in range(N):
            tempList = matched[n] + proposals[n]
            templist = [k for k in choices[n] if k in tempList]
            matched[n] = deepcopy(templist)
        diff = [max([len(matched[n])-degrees[n],0])  for n in range(N)]
        while sum(diff) > 0:
            idx = diff.index(max(diff))
            val = matched[idx].pop()
            matched[val].remove(idx)
            diff = [max([len(matched[n])-degrees[n],0])  for n in range(N)]
        for n in range(N):
            if len(matched[n]) > 0:
                maxima[n] = choices[n].index(matched[n][-1])
            else:
                maxima[n] = N
        proposals = [[] for n in range(N)]
        for n in range(N):
            for k in range(n+1,N):
                if k in choices[n] and n in choices[k]:
                    if choices[n].index(k) < maxima[n]:
                        if choices[k].index(n) < maxima[k]:
                            proposals[n].append(k)
                            proposals[k].append(n)
        tempList = [len(proposals[n]) for n in range(N)]
        if sum(tempList) == 0:
            flag = False
        K += 1
        if K > sqrt(N):
            flag = False
    return K


def polyMatchingOld(degrees,choices):
    # This method attempts to reproduce the Gale-Shapley algorithm for when:
    #  1 - Everyone can propose by or be proposed to anyone by themselves.
    #  2 - Not everyone is a suitable partner for someone else, this is, n might
    #      not consider k at all and would never be paired with them.
    #  3 - Each node has a maximum number of edges for which it can be an
    #      extreme.
    #
    # INPUT
    #  - degrees: list of the individual maximum degree of each node.
    #  - choices: The prioritized list of possible matches for a node.
    #
    # OUTPUT
    #  - matches: List of the matches given for each node.
    #
    flag = True
    N = len(degrees)
    unmatched  = [[k for k in choices[n] if n in choices[k]] for n in range(N)]
    rejected   = [[] for n in range(N)]
    matched    = [[] for n in range(N)]
    choices    = deepcopy(unmatched)
    # Test Commands
    J = 0
    while flag:
        # First, compute the proposals.
        proposals = []
        for n in range(N):
            if len(matched[n]) < degrees[n] and len(unmatched[n]) > 0:
                proposals.append([n,unmatched[n][0]])
        proplist = [[] for n in range(N)]
        for n in range(N):
            for prop in proposals:
                if prop[1] == n:
                    proplist[n].append(prop[0])
        # Second, compute the accepts and rejects for each member.
        for n in range(N):
            for k in proplist[n]:
                if k not in matched[n]:
                    matched[n].append(k)
                    matched[k].append(n)
        for n in range(N):
            tempList = [k for k in choices[n] if k in matched[n]]
            matched[n] = tempList
        diff = [max([len(matched[n])-degrees[n],0])  for n in range(N)]
        while sum(diff) > 0:
            idx = diff.index(max(diff))
            val = matched[idx].pop()
            matched[val].remove(idx)
            rejected[idx].append(val)
            rejected[val].append(idx)
            diff = [max([len(matched[n])-degrees[n],0])  for n in range(N)]
        # Third, reconfigure the bookkeeping for next round.
        for n in range(N):
            tempList = []
            for k in choices[n]:
                if k not in matched[n]:
                    if k not in rejected[n]:
                        tempList.append(k)
            if len(tempList) > 0:
                unmatched[n] = deepcopy(tempList)
            elif len(rejected[n]) > 0:
                tempList = [k for k in choices[n] if k in rejected[n]]
                unmatched[n] = deepcopy(tempList)
                rejected[n] = []
        # Fourth, calculate if it is time to stop
        K = 0
        for n in range(N):
            L = [choices[n].index(k) for k in matched[n]]
            if len(L) > 0:
                daMax = max(L)
            else:
                daMax = N
            L = [k for k in choices[n] if k not in matched[n] and
                                          choices[n].index(k) < daMax]
            for k in L:
                LL = [choices[k].index(j) for j in matched[k]]
                if len(LL) == 0:
                    K += 1
                else:
                    theirMax = max(LL)
                    ourPos = choices[k].index(n)
                    if ourPos < theirMax:
                        K += 1
        if K == 0:
            flag = False
        # Test Commands
        J += 1
        if J > 2*N:
            flag = False
    return matched


def generatePolyMatchingData(N, degMin, degMax, matchMin, matchMax):
    # This method is used to generate data to for the polyamorous version of the
    # Gale-Shapley algorithm to solve the Stable Marriage Problem. The algorithm
    # does not check for the suitability of the inputs, assumes they are given
    # correctly.
    #
    # INPUT
    #  - N: Total number of individuals involved. N is a positive integer, N>2.
    #
    #  - degMin: The minimum number of relations anyone can stablish. That is,
    #            the maximum degree of any vertex in the graph with
    #            1<degMin<=degMax. It should be a positive integer.
    #
    #  - degMax: The maximum number of relations anyone can stablish. That is,
    #            the maximum degree of any vertex in the graph. degMax < N-1. It
    #            should be a positive integer.
    #
    #  - matchMin: Minumum number of prospects that any participant should ask.
    #              In general, the individual minimum of matches should be less
    #              than or equal to the individual degree, but in this case, for
    #              simplicity, we agree that matchMin > degMax. It should be an
    #              integer.
    #
    #  - matchMax: Maximum number of prospects that can be chosen by each
    #              individual. It should be an integer satisfying
    #              matchMin <= matchMax < N.
    #
    #
    # OUTPUT
    #  - degrees: A list containing the maximum number of edges per vertex.
    #
    #  - choices: The prioritized list of possible matches for someone.
    #
    choices = []
    # Generate the degrees
    degrees = [randint(degMin,degMax) for n in range(N)]
    # Generate the choices
    for n in range(N):
        thisChoice = list(range(N))
        thisChoice.remove(n)
        shuffle(thisChoice)
        choiceNum = randint(matchMin,matchMax)
        choices.append(thisChoice[:choiceNum])
    return degrees, choices



def galeShapley(maleOptions, femaleOptions):
    # This is my implementation of the Gale Shapley algorithm. It assumes the
    # inputs are given correctly.
    #
    # INPUT
    #  - maleOptions: A list of the options of every male. That is, a list of N
    #                 sublists, each of which is a rearrangement of the integers
    #                 between 0 and N-1.
    #
    # - femaleOptions: Same characteristics as maleOptions. Important that the N
    #                  is the same for both.
    #
    #
    # OUTPUT:
    #  - matches: List of all the matches.
    #
    N = len(maleOptions)
    maleMatches   = [-1 for n in range(N)]
    femaleMatches = [-1 for n in range(N)]
    unmatched = N
    while unmatched > 0:
        # The zeroth step is to define the variables that are needed.
        propos     = []
        proposals  = []
        rejections = []
        # The first step is to make the proposals.
        for n in range(N):
            if maleMatches[n] < 0:
                k = maleOptions[n][0]
                propos.append([n,k])
        for k in range(N):
            proposals.append([pair[0] for pair in propos if pair[1] == k])
        # The second step is to see which proposals will be accepted.
        for k in range(N):
            thisProposals = proposals[k]
            if len(thisProposals) > 0:
                thisPlaces = [femaleOptions[k].index(j) for j in thisProposals]
                theMin = min(thisPlaces)
                if femaleMatches[k] == -1:
                    femaleMatches[k] = femaleOptions[k][theMin]
                    maleMatches[femaleMatches[k]] = k
                    proposals[k].remove(femaleMatches[k])
                else:
                    theCurrent = femaleOptions[k].index(femaleMatches[k])
                    if theCurrent > theMin:
                        maleMatches[femaleMatches[k]] = -1
                        proposals[k].append(femaleMatches[k])
                        femaleMatches[k] = femaleOptions[k][theMin]
                        maleMatches[femaleMatches[k]] = k
                        proposals[k].remove(femaleMatches[k])
        # The third step is to deal with rejections.
        for k in range(N):
            thisRejections = proposals[k]
            for n in thisRejections:
                rejections.append([n,k])
        for pair in rejections:
            maleOptions[pair[0]].remove(pair[1])
            femaleOptions[pair[1]].remove(pair[0])
        # The fourth step is to compute the unmatched ammount.
        unmatched = femaleMatches.count(-1)
    matches = []
    for n in range(N):
        matches.append([maleMatches[n],femaleMatches[n]])
    return matches



def generateOptions(N):
    # This method gets a positive integer N and returns a list containing N
    # lists, each of which is a rearrangement of the integers between 1 and N.
    options = []
    oneOption = list(range(N))
    for k in range(N):
        shuffle(oneOption)
        options.append(deepcopy(oneOption))
    return options



#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
# class ClassName:
    # This class it trying to implement the game.

    ###########
    # CREATOR #
    ###########
#     def __init__(self,suitors,pursued,cycles):
#         pass

    ###########
    # METHODS #
    ###########
