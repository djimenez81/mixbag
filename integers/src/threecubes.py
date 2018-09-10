#!/usr/bin/python
# module threecubes

# This is a module that pretends to implement algorithms to find the expression
# of all possitive integers not congruent with 4 or 5 mod 9 as sum of three
# cubes up to, first, one thousand.

# Copyright (c) 2017 David Jimenez.
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


# IMPORTS
import time
import xml.etree.ElementTree as ET
# Importo este modulo para poder trabajar con archivos xml
from xml.dom import minidom
from dumbint import *



# Module global variables
UPPERBOUND = 2**10 + 1


# CLASSES
class ThreeCubeDataBase:
    # This class implements a data base for the cases that we are interested on
    # considering for the sum of three cubes. It implements the methods to
    # update itself, to merge two of them, etc.

    # ATTRIBUTES
    _theNumberList  = []
    _theRegisters   = []
    _theIntervals   = []
    _theMissing     = []

    # CREATOR
    def __init__(self):
        self._theNumberList = []
        self._theRegisters  = []
        self._theIntervals  = []
        self._theMissing    = [k for k in range(1, UPPERBOUND)
                                  if k%9!=4 and k%9!=5]

    # GETTERS
    def getNumberList(self):
        return self._theNumberList

    def getRegisters(self):
        return self._theRegisters

    def getMissing(self):
        return self._theMissing

    def getIntervals(self):
        return self._theIntervals

    # METHODS
    def addCase(self, n, x, y, z):
        # This method takes the n, x, y and z and tries to insert it in the
        # database. It checks if indeed n == x**3 + y**3 + z**3, and if it is
        # already in the database.
        if n != x**3 + y**3 + z**3 or n >= UPPERBOUND:
            returnValue = False
        if n in self._theNumberList:
            k = self._theNumberList.index(n)
            returnValue = self._theRegisters[k].addCase(x,y,z)
        else:
            self._theNumberList.append(n)
            self._theRegisters.append(ThreeCubeRegister(n,x,y,z))
            if n in self._theMissing:
                self._theMissing.remove(n)
            returnValue = True
        return returnValue


    def reportInterval(self, lowEndPoint, highEndPoint):
        # This method reports an interval to the database, and sorts the
        # intervals already searched
        if lowEndPoint <= highEndPoint:
            self._theIntervals.append([lowEndPoint, highEndPoint])
            self.sortIntervals()
            return True
        else:
            return False


    def addList(self,aList):
        # Given a list where each element is of the form [n,x,y,z], where
        # n == x**3 + y**3 + z**3, it adds each of them to the database.
        for tC in aList:
            if len(tC) == 4:
                n = tC[0]
                x = tC[1]
                y = tC[2]
                z = tC[3]
                if n == x**3 + y**3 + z**3:
                    self.addCase(tC[0], tC[1], tC[2], tC[3])


    def sortIntervals(self):
        # This method sorts the intervals that have been searched. It also
        # merges intervals when necessary. It sorts using a bubblesort type
        # approach, as it is expected that the intervals will always be almost
        # sorted
        k = len(self._theIntervals)
        # Sort first
        for j in range(k):
            i = j
            checking = True
            while checking and i > 0:
                curr = self._theIntervals[i]
                prev = self._theIntervals[i-1]
                if ((prev[0] > curr[0]) or ((prev[0] == curr[0]) and
                                            (prev[1] > curr[1]))):
                    self._theIntervals[i]   = prev
                    self._theIntervals[i-1] = curr
                    i = i - 1
                else:
                    checking = False
        # Now merge
        k = 1
        while k < len(self._theIntervals):
            curr = self._theIntervals[k]
            prev = self._theIntervals[k-1]
            if curr[0] <= prev[1] + 1:
                newer = [min(curr[0],prev[0]), max(curr[1],prev[1])]
                self._theIntervals[k-1] = newer
                self._theIntervals.remove(curr)
            else:
                k = k + 1


    def sortRegisters(self):
        # This function sorts the registers in the data base.
        newNumberList = sorted(self._theNumberList)
        newRegisters  = []
        for theNumber in newNumberList:
            index = self._theNumberList.index(theNumber)
            theRegister = self._theRegisters[index]
            theRegister.sortStack()
            newRegisters.append(self._theRegisters[index])
        self._theRegisters  = newRegisters
        self._theNumberList = newNumberList


    def mergeDB(self, otherDB):
        # This function takes another database object (specific of this class),
        # and merges it with self. Basically, it basically just goes recod by
        # record on the argument and uses addCase to insert them in self.
        otherNumberList = otherDB.getNumberList()
        otherRegisters  = otherDB.getRegisters()
        self._theIntervals = self._theIntervals + otherDB.getIntervals()
        N = len(otherNumberList)
        for k in range(N):
            n   = otherNumberList[k]
            tCR = otherRegisters[k].getCurrentStack()
            for theCase in tCR:
                self.addCase(n,theCase[0],theCase[1],theCase[2])
        self.sortRegisters()
        self.sortIntervals()


    def createXMLfromDB(self, filename):
        # This function takes all the information in self, formats it and stores
        # it in an XML files saved witht the name provided in filename.
        self.sortRegisters()
        self.sortIntervals()
        numberOfSols = sum([reg.getCases() for reg in self._theRegisters])
        root         = ET.Element("ThreeCubeDataBase")
        numsol       = ET.SubElement(root,"solutionsfound",
                                         {"number":str(numberOfSols)})
        intervalList = ET.SubElement(root,"checkedintervals")
        for intv in self._theIntervals:
            interval = ET.SubElement(intervalList,"interval",
                          {"begins":str(intv[0]),"ends":str(intv[1])})
        misslist     = ET.SubElement(root,"missinglist")
        for k in self._theMissing:
            missing = ET.SubElement(misslist, "missing",{"n":str(k)})
        n    = len(self._theNumberList)
        for k in range(n):
            record = ET.SubElement(root, "record",
                       {"number":str(self._theNumberList[k])})
            register = self._theRegisters[k].getStack()
            for tR in register:
                sol = ET.SubElement(record, "solution",
                        {"x":str(tR[0]), "y":str(tR[1]), "z":str(tR[2])})
        rough    = ET.tostring(root)
        reparsed = minidom.parseString(rough)
        pretty   = reparsed.toprettyxml(indent="  ")
        root     = ET.fromstring(pretty)
        tree = ET.ElementTree(root)
        tree.write(filename)


    def getDBfromXML(self,filename):
        # This function loads an XML file with the same format that the function
        # createXMLfromDB uses, and loads it into self.
        tree = ET.parse(filename)
        root = tree.getroot()
        for child in root:
            if child.tag == "checkedintervals":
                for grandchild in child:
                    startPoint = int(grandchild.attrib["begins"])
                    endPoint   = int(grandchild.attrib["ends"])
                    self.reportInterval(startPoint,endPoint)
            elif child.tag == "missinglist":
                ourMissing = []
                for grandchild in child:
                    ourMissing.append(int(grandchild.attrib["n"]))
                ourMissing = [k for k in ourMissing if k in self._theMissing]
                self._theMissing = ourMissing
            elif child.tag == "record":
                n = int(child.attrib["number"])
                for grandchild in child:
                    x = int(grandchild.attrib["x"])
                    y = int(grandchild.attrib["y"])
                    z = int(grandchild.attrib["z"])
                    self.addCase(n,x,y,z)
        self.sortRegisters()
        self.sortIntervals()


    def solutionSearch(self,M,N):
        # This method searches for solutions. It tries to improve on the brute
        # force approach.
        theList = []
        tic = time.time()
        for x in range(M,N+1):
            xx = cubeRoot((x**3 - UPPERBOUND)//2) + 1
            for y in range(xx,x):
                Lz = max(0  , cubeRoot(x**3 - y**3 - UPPERBOUND) + 1)
                Uz = min(y+1, cubeRoot(x**3 - y**3 + UPPERBOUND) + 1)
                for z in range(Lz,Uz):
                    n = x**3 - y**3 - z**3
                    if abs(n) < UPPERBOUND:
                        if n > 0 and not ( n, x,-y,-z) in theList:
                            theList.append(( n, x,-y,-z))
                        elif n < 0 and not (-n,-x, y, z) in theList:
                            theList.append((-n,-x, y, z))
        toc = time.time()
        print(toc-tic)
        print(len(theList))
        return [[M,N],theList]


    def initialSolutionSearch(self,M,N):
        # This method searches for solutions. It should be used only for M and N
        # positive, M < N and N < sqrt(UPPERBOUND)
        theList = []
        for x in range(M,N+1):
            for y in range(x):
                for z in range(y+1):
                    n1 = x**3 + y**3 + z**3
                    n2 = x**3 + y**3 - z**3
                    n3 = x**3 - y**3 + z**3
                    n4 = x**3 - y**3 - z**3
                    if z < y:
                        if abs(n1) < UPPERBOUND:
                            if n1 >= 0 and not ( n1,  x,  y,  z) in theList:
                                theList.append(( n1,  x,  y,  z))
                            elif n1 < 0 and not (-n1, -x, -y, -z) in theList:
                                theList.append((-n1, -x, -y, -z))
                        if abs(n2) < UPPERBOUND:
                            if n2 >= 0 and not ( n2,  x,  y, -z) in theList:
                                theList.append(( n2,  x,  y, -z))
                            elif n2 < 0 and not (-n2, -x, -y,  z) in theList:
                                theList.append((-n2, -x, -y,  z))
                        if abs(n3) < UPPERBOUND:
                            if n3 >= 0 and not ( n3,  x, -y,  z) in theList:
                                theList.append(( n3,  x, -y,  z))
                            elif n3 < 0 and not (-n3, -x,  y, -z):
                                theList.append((-n3, -x,  y, -z))
                        if abs(n4) < UPPERBOUND:
                            if n4 >= 0 and not ( n4,  x, -y, -z) in theList:
                                theList.append(( n4,  x, -y, -z))
                            elif n4 < 0 and not (-n4, -x,  y,  z) in theList:
                                theList.append((-n4, -x,  y,  z))
                    else:
                        if abs(n1) < UPPERBOUND:
                            if n1 >= 0 and not ( n1,  x,  y,  z) in theList:
                                theList.append(( n1,  x,  y,  z))
                            elif n1 < 0 and not (-n1, -x, -y, -z) in theList:
                                theList.append((-n1, -x, -y, -z))
                        if abs(n4) < UPPERBOUND:
                            if n4 >= 0 and not ( n4,  x, -y, -z) in theList:
                                theList.append(( n4,  x, -y, -z))
                            elif n4 < 0 and not (-n4, -x,  y,  z) in theList:
                                theList.append((-n4, -x,  y,  z))
        return [[M,N],theList]


    def dumList(self):
        # This method generates the simple solutions in the rage. That is,
        # cubes, double of a cube, triple of a cube, or duble of a cube plus or
        # minus a lesser cube.
        theList = []
        N = 1
        X = 1
        while N < UPPERBOUND:
            theList.append((N,X,0,0))
            X = X + 1
            N = X**3
        N = 2
        X = 1
        while N < UPPERBOUND:
            theList.append((N,X,X,0))
            X = X + 1
            N = 2*(X**3)
        N = 3
        X = 1
        while N < UPPERBOUND:
            theList.append((N,X,X,X))
            for Y in range(1,X):
                N = X**3 + X**3 + Y**3
                theList.append((N,X,X,Y))
                N = X**3 + X**3 - Y**3
                theList.append((N,X,X,-Y))
            X = X + 1
            N = 3*(X**3)
        return theList
# end of class ThreeCubeDataBase




class ThreeCubeRegister:
    # We are not interested on all the possible cases for each n. We are
    # interested on just the first, say, two cases. This class is to register
    # the cases that we "like best".

    # ATTRIBUTES
    _N            = None     # What is the number of the register.
    _stack = []       # Each representation.

    # CONSTRUCTOR
    def __init__(self, n, x, y, z):
        self._N            = n
        self._stack = [(x,y,z)]

    # GETTERS
    def getN(self):
        return self._N

    def getCases(self):
        return len(self._stack)

    def getStack(self):
        return self._stack

    # METHODS
    def addCase(self, x, y, z):
        # This methods adds a new case to the current register. It does check if
        # the case is actually a solution for this register.
        if self._N == x**3 + y**3 + z**3 and not (x,y,z) in self._stack:
            self._stack.append((x,y,z))
            returnValue = True
        else:
            returnValue = False
        return returnValue

    def sortStack(self):
        # This method sorts the cases in the stack. It uses a bubblesort type
        # approach, because it is expected that the stack will be almost sorted
        # most of the time.
        k = len(self._stack)
        for j in range(k):
            i = j
            checking = True
            while checking and i > 0:
                curr = self._stack[i]
                prev = self._stack[i-1]
                if ((abs(prev[0]) > abs(curr[0])) or
                    ((abs(prev[0]) == abs(curr[0])) and
                     (abs(prev[1]) > abs(curr[1])))):
                    self._stack[i]   = prev
                    self._stack[i-1] = curr
                    i = i - 1
                else:
                    checking = False
# end of class threeCubeRegister
