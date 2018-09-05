# Proyecto Alineamiento de Secuencias de PF 5026 Paradigmas de Computacion
# Este archivo contiene la parte logica del proyecto programado.
#
# Grupo:
#    Mario Bogantes
#    David Jimenez
#    Denis Jimenez
#    Jeffry Ortiz
#

#############
#############
##         ##
## IMPORTS ##
##         ##
#############
#############
from math import isnan
import pdb
import xml.etree.ElementTree as ET
from xml.dom import minidom

######################
######################
##                  ##
## GLOBAL VARIABLES ##
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


############
# XML SAVE #
############


############
# XML READ #
############


########################### 
# GENERAL NEEDLEMAN WUNCH # 
########################### 
def generalNW(sequence1, sequence2, matchScore, mismatchScore, gapPenalty):
    # This method is basically the Needleman-Wunsch, where the user can specify
    # the match score, the mismatch score, and the gap penalty.
    # 
    # Parameters:
    #   - sequence1:     An array. Can be also strings, but then, each character
    #                   is a symbols. The contents have to be comparable with
    #                   '='.
    #   - sequence2: Same requirements as sequence1
    #   - matchScore:    A number. Self explanatory.
    #   - mismatchScore: A number. Self explanatory.
    #   - gapPenalty:    A number. Self explanatory.
    #
    # Returns:
    #   - aligned: An array of two arrays of the same length, representing the 
    #              sequences already aligned.
    # 
    
    
    # CONSTANTS
    UP       = 1 
    LEFT     = 2
    DIAG     = 3
    UPLEFT   = 4
    UPDIAG   = 5
    LEFTDIAG = 6
    ALLDIR   = 7

    # DEFINITION OF VARIABLES
    n = len(sequence1)
    m = len(sequence2)
    scores = [[0 for i in range(m+1)] for j in range(n+1)]
    arrows = [[0 for i in range(m+1)] for j in range(n+1)]
    
    # Initialize matrices
    for i in range(1,n+1):
        scores[i][0] = i * gapPenalty
        arrows[i][0] = UP
    for i in range(1,m+1):
        scores[0][i] = i * gapPenalty
        arrows[0][i] = LEFT
    
    # Filling the matrices
    for i in range(1,n+1):
        for j in range(1,m+1):
            m = 0
            if sequence1[i-1] == sequence2[j-1]:
                m = matchScore
            else:
                m = mismatchScore
            x = scores[i-1][j-1] + m         # DIAG
            y = scores[i-1][j] + gapPenalty  # UP
            z = scores[i][j-1] + gapPenalty  # LEFT
            
            v = max(x,y,z)
            scores[i][j] = v
            
            if v == x and v == y and v == z:
                arrows[i][j] = ALLDIR
            elif v == x and v == y:
                arrows[i][j] = UPDIAG
            elif v == x and v == z:
                arrows[i][j] = LEFTDIAG
            elif v == y and v == z:
                arrows[i][j] = UPLEFT
            elif v == x:
                arrows[i][j] = DIAG
            elif v == y:
                arrows[i][j] = UP
            elif v == z: 
                arrows[i][j] = LEFT
            
            
    return [scores,arrows]
    
    



#################
# OTHER METHODS #
#################
