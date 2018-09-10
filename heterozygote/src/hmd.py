# Copyright (c) 2017 David Jimenez.
# All rights reserved.
#
# In this file we will implement the functions necessary for the logic the 
# project. A colleague has the problem that when she receives some 
# electropherograms from individuals with a heterozygote mutation, particularly
# incertions and delitions, she has to detect the mutation manually, as the
# sequencer, when an ambiguity is detected, instead of using the IUPAC ambiguity
# code for the specific case detected, it just places an N. Here we try to go
# directly to the original measurements from the electropherogram, detect the
# picks by ourselves, correlate them with the ones of the original call from the
# sequencer, and then include our own sequence with the right codes. Afterwards,
# we separate the two sequences and detect the mutation automatically. (not
# everything is implemented yet).
#
# LICENSE 
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

from random import choice
from abifpy import Trace


def separateSeqNoRef(iupacSeq):
    # This function takes one sequence in IUPAC standard, comprised only of A,
    # C, G, T, R, Y, S, W, K and M, and returns the two sequences separated and
    # the string of incertion.
    leftSeq  = ["N"]*len(iupacSeq)
    rightSeq = ["N"]*len(iupacSeq)
    ambiguityList = list()
    outputDic = {}
    mutStart = mutEnd = 0
    undetectedMutation = True
    nonIdentifMutation = True
    BASES = ["A", "C", "G", "T"]
    for index in range(len(iupacSeq)):
        if undetectedMutation:
            if iupacSeq[index] in BASES:
                leftSeq[index]  = iupacSeq[index]
                rightSeq[index] = iupacSeq[index]
            else:
                ambiguityList.append(ambSet(iupacSeq[index]))
                mutStart = index
                undetectedMutation = False
        else:
            ambiguityList.append(ambSet(iupacSeq[index]))
    if undetectedMutation:
        outputDic.update({"leftSeq":leftSeq, "rightSeq":rightSeq})
        outputDic.update({"mutStart":0,"mutLength":0,"incertion":""})
    else:
        index = 1
        while index < len(ambiguityList) and nonIdentifMutation:
            compList = list()
            leftAmb  = ambiguityList[:-index]
            rightAmb = ambiguityList[index:]
            for i in range(len(leftAmb)):
                compList.append(leftAmb[i].intersection(rightAmb[i]) != set())
            if all(compList):
                nonIdentifMutation = False
            else:
                index += 1
        if index == len(ambiguityList):
            outputDic.update({"leftSeq":''.join(leftSeq)})
            outputDic.update({"rightSeq":''.join(rightSeq)})
            outputDic.update({"mutStart":mutStart,"error":True})
        else:
            compList = list()
            for i in range(len(leftAmb)):
                # When the intersection is unique, we insert the base into the
                # sequence, assuming that the mutation in on the right sequence.
                theIntersec = leftAmb[i].intersection(rightAmb[i])
                compList.append(theIntersec)
                if len(theIntersec) == 1:
                    leftSeq[mutStart+i] = list(theIntersec)[0]
                    rightSeq[mutStart+index+i] = list(theIntersec)[0]
            changeCount = 1
            while changeCount > 0:
                changeCount = 0
                for i in range(len(ambiguityList)):
                    posHere = list(ambiguityList[i])
                    if leftSeq[mutStart+i] == "N":
                        if rightSeq[mutStart+i] != "N":
                            if len(posHere) == 1:
                                leftSeq[mutStart+i] = rightSeq[mutStart+i]
                                changeCount = changeCount + 1
                            elif posHere[0] == rightSeq[mutStart+i]:
                                leftSeq[mutStart+i] = posHere[1]
                                changeCount = changeCount + 1
                            else:
                                leftSeq[mutStart+i] = posHere[0]
                                changeCount = changeCount + 1
                    elif rightSeq[mutStart+i] == "N":
                        if leftSeq[mutStart+i] != "N":
                            if len(posHere) == 1:
                                rightSeq[mutStart+i] = leftSeq[mutStart+i]
                                changeCount = changeCount + 1
                            elif posHere[0] == leftSeq[mutStart+i]:
                                rightSeq[mutStart+i] = posHere[1]
                                changeCount = changeCount + 1
                            else:
                                rightSeq[mutStart+i] = posHere[0]
                                changeCount = changeCount + 1
                for i in range(len(leftAmb)):
                    leftBase  = leftSeq[mutStart+i]
                    rightBase = rightSeq[mutStart+i+index]
                    if leftBase == "N" and rightBase != "N":
                        leftSeq[mutStart+i] = rightBase
                        changeCount = changeCount + 1
                    elif leftBase != "N" and rightBase == "N":
                        rightSeq[mutStart+i+index] = leftBase
                        changeCount = changeCount + 1
            outputDic.update({"leftSeq":''.join(leftSeq)})
            outputDic.update({"rightSeq":''.join(rightSeq)})
            outputDic.update({"mutStart":mutStart})
            outputDic.update({"mutLength":index})
            outputDic.update({"mutation":''.join(rightSeq[mutStart:mutStart+index])})
    return outputDic


def separateSeqwRef(iupacSeq, refSeq):
    # This function takes two sequences, the first is the sequence, in IUPAC
    # standard, the second, the reference homocigote sequence.
    # This function assumes that the length of the two sequences are the same,
    # and that the first sequence only contains A, C, G, T, R, Y, S, W, K and M,
    # and the second sequence contains only A, C, G and T, and that they
    # conincide in all non ambiguous bases, and the reference sequence conincide
    # with at least one of the posibilities in the ambiguous cases.
    outputSeq = ["N"]*len(iupacSeq)
    startMutation = False
    startMutPos = 0
    undetectedMutation = True
    outputDic = {}

    for index in range(len(iupacSeq)):

        if iupacSeq[index] != refSeq[index] and not startMutation:
            startMutation = True
            startMutPos = index

        if iupacSeq[index] == "A":
            outputSeq[index] = "A"
        elif iupacSeq[index] == "C":
            outputSeq[index] = "C"
        elif iupacSeq[index] == "G":
            outputSeq[index] = "G"
        elif iupacSeq[index] == "T":
            outputSeq[index] = "T"
        elif iupacSeq[index] == "M":
            if refSeq[index] == "A":
                outputSeq[index] = "C"
            elif refSeq[index] == "C":
                outputSeq[index] = "A"
        elif iupacSeq[index] == "R":
            if refSeq[index] == "A":
                outputSeq[index] = "G"
            elif refSeq[index] == "G":
                outputSeq[index] = "A"
        elif iupacSeq[index] == "W":
            if refSeq[index] == "A":
                outputSeq[index] = "T"
            elif refSeq[index] == "T":
                outputSeq[index] = "A"
        elif iupacSeq[index] == "S":
            if refSeq[index] == "C":
                outputSeq[index] = "G"
            elif refSeq[index] == "G":
                outputSeq[index] = "C"
        elif iupacSeq[index] == "Y":
            if refSeq[index] == "C":
                outputSeq[index] = "T"
            elif refSeq[index] == "T":
                outputSeq[index] = "C"
        elif iupacSeq[index] == "K":
            if refSeq[index] == "G":
                outputSeq[index] = "T"
            elif refSeq[index] == "T":
                outputSeq[index] = "G"

    outputSeq = ''.join(outputSeq)
    if startMutation:
        index = 1
        while undetectedMutation:
            if outputSeq[startMutPos:-index] == refSeq[startMutPos+index:]:
                outputDic.update({"output":outputSeq,"mutType":"deletion"})
                outputDic.update({"mutSeq":refSeq[startMutPos:startMutPos+index]})
                outputDic.update({"startPoint":startMutPos,"length":index})
                undetectedMutation = False
            elif outputSeq[startMutPos+index:] == refSeq[startMutPos:-index]:
                outputDic.update({"output":outputSeq,"mutType":"incertion"})
                outputDic.update({"mutSeq":outputSeq[startMutPos:startMutPos+index]})
                outputDic.update({"startPoint":startMutPos,"length":index})
                undetectedMutation = False
            elif index >= len(outputSeq)-startMutPos:
                outputDic.update({"output":outputSeq,"mutType":"uncertain"})
                outputDic.update({"mutSeq":outputSeq[startMutPos:]})
                outputDic.update({"startPoint":startMutPos,"length":index})
                undetectedMutation = False
            else:
                index+=1
    else:
        outputDic.update({"output":outputSeq,"mutSeq":"","length":0})
        outputDic.update({"mutType":"uncertain","startPoint":0})
    return outputDic


def getAbi(fileName):
    # This function opens the file AB1 and returns a dictionary with the fields
    # that are useful to us.
    theTrace = Trace(fileName)
    theRaws = ["raw1", "raw2", "raw3", "raw4"]
    abi = {}
    baseOrder = theTrace.data["baseorder"]
    abi.update({"BaseOrder":baseOrder})
    abi.update({"NumValues":len(theTrace.data["raw1"])})
    abi.update({"NumBases":len(theTrace.seq)})
    abi.update({"Sequence":theTrace.seq})
    abi.update({"TracePeaks":theTrace.data["tracepeaks"]})
    for i in range(4):
        oneRaw = theRaws[i]
        oneBase = baseOrder[i]
        if oneBase == 'A':
            abi.update({"RawA":list(theTrace.data[oneRaw])})
        elif oneBase == 'C':
            abi.update({"RawC":list(theTrace.data[oneRaw])})
        elif oneBase == 'G':
            abi.update({"RawG":list(theTrace.data[oneRaw])})
        else:
            abi.update({"RawT":list(theTrace.data[oneRaw])})
    return abi


def synHetMut(length, start, mutlength):
    # Generation of synthetic triples of sequences: An original random sequence
    # with length given, a mutated sequence, with a random incersion starting
    # at position start, of length mutlength, and the combined sequence on
    # IUPAC ambiguity code standard.
    #
    # Use:
    #   >> ori, mut, iup = synHetMut(20,12,3)
    #
    # Output:
    #   ori = "ATTGCCTTGAGTGCGATTTT"
    #   mut = "ATTGCCTTGAGTCTGGCGAT"
    #   iup = "ATTGCCTTGAGTSYGRYKWT"
    #
	bases = ["A", "C", "G", "T"]
	commonSeq = (''.join(choice(bases) for i in range(start)))
	mutatSeq  = (''.join(choice(bases) for i in range(mutlength)))
	restOfOrg = (''.join(choice(bases) for i in range(length-start)))
	restOfMut = restOfOrg[:-mutlength]
	original = commonSeq + restOfOrg
	mutated  = commonSeq + mutatSeq + restOfMut
	iupac = ["N"]*length
	for index in range(length):
		iupac[index] = ambCode(original[index],mutated[index])
	iupac = ''.join(iupac)
	return original, mutated, iupac


def maxDetection(theArray, tolPercentage = 0.01, minPercentage = 0.05):
    # maxDetection detects the peaks or local maxima in the theArray.
    theLen  = len(theArray)
    theMaxs = list()
    N = len(theArray)
    maxVal = max(theArray)
    delta = maxVal * tolPercentage
    bound = maxVal * minPercentage
    for i in range(1,N-1):
        leftVal  = theArray[i-1]
        rightVal = theArray[i+1]
        theVal   = theArray[i]
        if theVal > bound:
            if theVal > rightVal + delta:
                if theVal > leftVal + delta:
                    theMaxs.append(i)
    return theMaxs


def ambCode(fst,snd):
    # This function generates the IUPAC ambiguity code for up to two different
    # bases.
	bst = set([fst, snd])
	if bst == set(["A"]):
		return "A"
	elif bst == set(["C"]):
		return "C"
	elif bst == set(["G"]):
		return "G"
	elif bst == set(["T"]):
		return "T"
	elif bst == set(["A","C"]):
		return "M"
	elif bst == set(["A","G"]):
		return "R"
	elif bst == set(["A","T"]):
		return "W"
	elif bst == set(["C","G"]):
		return "S"
	elif bst == set(["C","T"]):
		return "Y"
	elif bst == set(["G","T"]):
		return "K"
	else:
		return "N"


def ambSet(iupacCode):
    # This function returns the set of all ambiguity codes with up to two
    # possible outputs.
    if iupacCode == "A":
        return set(["A"])
    elif iupacCode == "C":
        return set(["C"])
    elif iupacCode == "G":
        return set(["G"])
    elif iupacCode == "T":
        return set(["T"])
    elif iupacCode == "M":
        return set(["A","C"])
    elif iupacCode == "R":
        return set(["A","G"])
    elif iupacCode == "W":
        return set(["A","T"])
    elif iupacCode == "S":
        return set(["C","G"])
    elif iupacCode == "Y":
        return set(["C","T"])
    elif iupacCode == "K":
        return set(["G","T"])
    else:
        return set()
