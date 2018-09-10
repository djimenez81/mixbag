#!/usr/bin/python
# module pcloud

# This module implements a Point Clud class, as well as several related
# functionalities.

# Copyright (c) 2017 Universidad de Costa Rica
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
# DISCLAIMED. IN NO EVENT SHALL UNIVERSIDAD DE COSTA RICA  BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Principal Investigator:
#         David Jimenez <david.jimenezlopez@ucr.ac.cr>
# Assistants:
#         Jorge Arce


# IMPORTS
from math   import sqrt
from random import random, sample, gauss
import pdb



# CLASSES
class PointCloud:
    # This class implements a point cloud, that is, a collection of vectors of
    # the same dimension, either entered one at a time, or created according to
    # some criteria.

    # ATTRIBUTES
    _numOfPts  = 0
    _dimension = 1
    _cloud     = []
    _R         = 0
    _method    = "MANUAL"

    # CREATORS
    def __init__(self,dim):
        # The only thing that the
        self._dimension = dim

    # SETTERS AND GETTERS
    def getDimension(self):
        # Returns the dimension of the points in the cloud.
        return self._dimension


    def getNumberOfPoints(self):
        # Rturns the number of points in the cloud
        return self._numOfPts


    def getCloud(self):
        # Returns the collection of points in the cloud.
        return self._cloud


    def getRadius(self):
        # Returns the radius of the cloud, ONLY IF ONE HAS BEEN DEFINED.
        return self._R


    def getMethod(self):
        # Returns the string that corresponds to the
        return self._method

    def getPoint(self,idx):
        # Returns the k-th element of the cloud.
        return self._cloud[idx]


    def setRadius(self,R):
        # Sets the radius of the cloud.
        self._R = R


    def setMethod(self,theMethod):
        # Sets the method for the generation of the points. Note that the method
        # MANUAL means that points will not be generated, but should be added
        # to the cloud manually.
        self._method = theMethod


    def setPoint(self,vector,idx):
        # Sets the idx-th point of self to vector
        if self._dimension == len(vector):
            self._cloud[idx] = vector
            return True
        else:
            return False



    # PRIVATE METHODS
    def _pntNorm(self,vector):
        # This function returns the regular norm of the vector.
        return sqrt(sum([i**2 for i in vector]))


    # PUBLIC METHODS
    def addList(self,theList):
        # This adds elements from theList to the cloud.
        for P in theList:
            self.addPoint(P)


    def addPoint(self,vector):
        # This method adds a point to the cloud.
        if len(vector) == self._dimension:
            self._cloud.append(vector)
            self._numOfPts = self._numOfPts + 1
            return True
        else:
            return False


    def removePoint(self, vector):
        # This method removes the vector from the cloud IF it is already in the
        # cloud.
        if vector in self._cloud:
            self._cloud.remove(vector)
            self._numOfPts = self._numOfPts - 1
            return True
        else:
            return False


    def removePosition(self,idx):
        # This method removes the idx-th point in cloud, where it starts in the
        # 0th position.
        if idx < self._numOfPts:
            del self._cloud[idx]
            self._numOfPts = self._numOfPts - 1
            return True
        else:
            return False


    def generateCloud(self, N):
        # This function generates N random points, according to the different
        # methods, and according to the other parameters.
        dim = self._dimension
        R   = self._R
        if R == 0:
            return "Radius equals zero. No cloud points are generated."
        elif self._method == "CUBE":
            # "CUBE" generates
            for n in range(N):
                self._cloud[n] = [2*R*random()-R for k in range(dim)]
            return "Success."
        elif self._method == "SPHERE":
            for n in range(N):
                flag = True
                while flag:
                    P = [2*R*random()-R for k in range(dim)]
                    if self._pntNorm(P) < R:
                        self._cloud[n] = P
                        flag = False
            return "Success."
        elif self._method == "GAUSS":
            for n in range(N):
                self_cloud[n] = [gauss(0,R) for k in range(dim)]
            return "Success."


    def getMeanPoint(self):
        # This method returns the center of gravity of the cloud.
        N = self._numOfPts
        C = self._cloud
        X = zip(*C)
        return [sum(x)/N for x in X]


    def getRandomSampleWithIndices(self,N):
        # This method returns a different cloud that contains a random sample of
        # the cloud self. It also returns the indices of the samples from the
        # original.
        sampleCloud = PointCloud(self._dimension)
        sampleCloud.setRadius(self._R)
        sampleCloud.setMethod(self._method)
        sampleIndices = sample(range(self._numOfPts),N)
        for k in sampleIndices:
            sampleCloud.addPoint(self._cloud[k])
        return sampleCloud,sampleIndices


    def getRandomSample(self,N):
        sampleCloud,sampleIndices = self.getRandomSampleWithIndices(N)
        return sampleCloud


    def addNoise(self,epsilon):
        for n in range(self._numOfPts):
            flag = True
            while flag:
                P = [2*epsilon*random()-epsilon for k in range(self._dimension)]
                if self._pntNorm(P) < epsilon:
                    self._cloud[n] = [sum(x) for x in zip(P,self._cloud[n])]
                    flag = False



    def translateCloud(self,vec):
        # This translates the cloud by vector.
        if self._dimension == len(vec):
            for n in range(self._numOfPts):
                P = self._cloud[n]
                self._cloud[n] = [sum(x) for x in zip(P,vec)]
            return True
        else:
            return False



# End of file
