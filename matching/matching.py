#!/usr/bin/python
# module matching

# Copyright (c) 2022 Universidad de Costa Rica
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
        prop2 = deepcopy(proposals)
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
                        # Random line of code to test shit

        # The third step is to deal with rejections.
        # The fourth step is to compute the unmatched ammount.
        # These are test commands
        unmatched = 0
    matches = [propos,prop2, proposals,maleMatches,femaleMatches]
#    matches = [propos,proposals]
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
