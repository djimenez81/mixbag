# Proyecto Mapas genicos de PF 5026 Paradigmas de Computacion
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
TOL = 0.01

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
def xmlSave(info, filename):
    # This saves the information passed by the graphical interface to an xml
    # file. The variable infor is a list of three elements:
    #
    #  - first: list of sublists, each sublist has three strings, gen name,
    #           description and color.
    #  - second: Boolean. "Has matrix been entered?"
    #  - third: empty if second is false, the matrix if second is true.
    #
    root = ET.Element("GeneAnalyzer")
    if info[1]:
        matrixEntered = ET.SubElement(root,"HasMatrix", {"value":"True"})
    else:
        matrixEntered = ET.SubElement(root,"HasMatrix", {"value":"False"})
    geneList = ET.SubElement(root,"GeneList")
    for genL in info[0]:
        gene = ET.SubElement(geneList,"Gene",
                {"name":genL[0],"color":genL[2],"description":genL[1]})
    if info[1]:
        matrix = ET.SubElement(root,"Matrix")
        K = len(info[2])
        for i in range(K-1):
            for j in range(i+1,K):
                if info[2][i][j] != "":
                    entry = ET.SubElement(matrix,"Entry",
                            {"i":str(i),"j":str(j),"distance":info[2][i][j]})
    rough    = ET.tostring(root)
    reparsed = minidom.parseString(rough)
    pretty   = reparsed.toprettyxml(indent="  ")
    root     = ET.fromstring(pretty)
    tree = ET.ElementTree(root)
    tree.write(filename)


############
# XML READ #
############
def xmlRead(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    N = 0 # Number of genes
    info = [[],False,[]]
    for child in root:
        if child.tag ==  "HasMatrix":
            if child.attrib["value"] == "True":
                info[1] = True
        if child.tag == "GeneList":
            geneList = []
            for grandchild in child:
                gene = []
                gene.append(grandchild.attrib["name"])
                gene.append(grandchild.attrib["description"])
                gene.append(grandchild.attrib["color"])
                geneList.append(gene)
            info[0] = geneList
            N = len(geneList)
        if child.tag == "Matrix":
            matrix = [[""]*N for i in range(N)]
            for i in range(N):
                matrix[i][i] = "0.0"
            for grandchild in child:
                i = int(grandchild.attrib["i"])
                j = int(grandchild.attrib["j"])
                matrix[i][j] = grandchild.attrib["distance"]
                matrix[j][i] = grandchild.attrib["distance"]
            info[2] = matrix
    return info


############
# ANALYZER #
############
def genAnalyzer(theMatrix):
    # This is a control flow function. This function takes theMatrix, and
    # generates sequentially the groups, the ordering of the groups, and the
    # spacing of the groups. It does it for all groups, even if it finds
    # inconsistencies. It returns a dictionary package that contains:
    #
    #  - success: Boolean, is True if no inconsistency was found at all.
    #  - messages: list of all the messages for inconsistencies (empty if
    #               success is True)
    #  - groups: list of the ordered groups
    #           [gen0,gen1,gen2], [gen3, gen4, gen5]
    #  - spacings: list of the spacing lists between the elements of each ordered
    #               group. Each spacing list might be empty if inconsistencies
    #               were found. If not, it always has a 0 at the end
    #               [dist gen0 -gen1, dist gen1 gen2, 0]
    #  - inferred: List all inferred distances. Note that each inferred distance
    #               is given as [i j d] that means, that the distance between
    #               gene i and gene j was determined to be d.
    #  - matrix: The matrix once all inferred values have been introduced.
    #
    stillSucess = True
    messages = []
    ordGrps  = []
    inferred = []
    spacings = []

    groups = genGrouping(theMatrix)
    for group in groups:
        groupPackage = groupOrdering(group, theMatrix)
        theMatrix = groupPackage["matrix"]
        inferred += groupPackage["inferred"]
        if groupPackage["success"]:
            spng = genSpacing(groupPackage["ordGrp"],theMatrix)
            ordGrps.append(groupPackage["ordGrp"])
            spacings.append(spng)
        else:
            stillSucess = False
            spacings.append([])
            ordGrps.append([])
            messages.append(groupPackage["message"])
    package = {}
    package.update({"success":stillSucess})
    package.update({"messages":messages})
    package.update({"groups":ordGrps})
    package.update({"spacings":spacings})
    package.update({"inferred":inferred})
    package.update({"matrix":theMatrix})
    return package


############
# GROUPING #
############
def genGrouping(theMatrix):
    # This method groups the genes into link groups.
    N = len(theMatrix)
    useflDist = []
    coordDist = []
    # Preparing information
    for i in range(N-1):
        for j in range(i+1,N):
            if not isnan(theMatrix[i][j]):
                useflDist.append(theMatrix[i][j])
                coordDist.append([i,j])
    # Ordering the coordinates and distances.
    ordDist = []
    ordCoor = []
    while len(useflDist) > 0:
        x = min(useflDist)
        idx = useflDist.index(x)
        ordDist.append(x)
        ordCoor.append(coordDist[idx])
        del useflDist[idx]
        del coordDist[idx]

    # Eliminating the stupid case of not having any linkage what so ever.
    if ordDist[0] > 0.5:
        genGroups = [[x] for x in range(N)]
        return genGroups

    # Now the grouping part
    genGroups = []
    listOfGenes = list(range(N))
    while len(ordDist) > 0:
        x = ordCoor[0][0]
        y = ordCoor[0][1]
        d = ordDist[0]
        # Long chain of if (elif)+ else to group x and y
        if x in listOfGenes and y in listOfGenes and d<=0.5:
            liX = whichGroups(x,genGroups,theMatrix) # Groups where x can be
            liY = whichGroups(y,genGroups,theMatrix) # Groups where y can be
            liT = list(set(liX+liY))
            liT.sort()
            liT.reverse()
            if len(liT) > 0:
                group = [x,y]
                for idx in liT:
                    group += genGroups[idx]
                    del genGroups[idx]
                group = list(set(group))
                group.sort()
                genGroups.append(group)
            else:
                genGroups.append([x,y])
        elif x in listOfGenes and y in listOfGenes: # They are far appart
            liX = whichGroups(x,genGroups,theMatrix) # Groups where x can be
            liY = whichGroups(y,genGroups,theMatrix) # Groups where y can be
            liXY = [a for a in liX if a in liY] # where x and y are together
            if len(liXY) > 0: # This is the case where both are in a same group.
                liT = list(set(liX+liY))
                liT.sort()
                liT.reverse()
                group = [x,y]
                for idx in liT:
                    group += genGroups[idx]
                    del genGroups[idx]
                group = list(set(group))
                group.sort()
                genGroups.append(group)
            elif len(liX) > 0 and len(liY) > 0: # If they do not play together
                liT = list(set(liX+liY))
                liT.sort()
                liT.reverse()
                groupX = [x]
                for idx in liX:
                    groupX += genGroups[idx]
                groupX = list(set(groupX))
                groupX.sort()
                groupY = [y]
                for idx in liY:
                    groupY += genGroups[idx]
                groupY = list(set(groupY))
                groupY.sort()
                for idx in liT:
                    del genGroups[idx]
                genGroups.append(groupX)
                genGroups.append(groupY)
            elif len(liX) > 0:
                liX.sort()
                liX.reverse()
                group = [x]
                for idx in liX:
                    group += genGroups[idx]
                    del genGroups[idx]
                group = list(set(group))
                group.sort()
                genGroups.append(group)
                genGroups.append([y])
            elif len(liY) > 0:
                liY.sort()
                liY.reverse()
                group = [y]
                for idx in liY:
                    group += genGroups[idx]
                    del genGroups[idx]
                group = list(set(group))
                group.sort()
                genGroups.append(group)
                genGroups.append([x])
            else:
                genGroups.append([x])
                genGroups.append([y])
        elif x in listOfGenes and d < 0.5:
            liX = whichGroups(x,genGroups,theMatrix) # Groups where x can be
            for i in range(len(genGroups)):
                if y in genGroups[i]:
                    liX.append(i)
            liX = list(set(liX))
            liX.sort()
            liX.reverse()
            group = [x,y]
            for idx in liX:
                group += genGroups[idx]
                del genGroups[idx]
            group = list(set(group))
            group.sort()
            genGroups.append(group)
        elif y in listOfGenes and d < 0.5:
            liY = whichGroups(y,genGroups,theMatrix) # Groups where y can be
            for i in range(len(genGroups)):
                if x in genGroups[i]:
                    liY.append(i)
            liY = list(set(liY))
            liY.sort()
            liY.reverse()
            group = [x,y]
            for idx in liY:
                group += genGroups[idx]
                del genGroups[idx]
            group = list(set(group))
            group.sort()
            genGroups.append(group)
        elif x in listOfGenes:
            liX = whichGroups(x,genGroups,theMatrix) # Groups where x can be
            liX.sort()
            liX.reverse()
            group = [x]
            for idx in liX:
                group += genGroups[idx]
                del genGroups[idx]
            group = list(set(group))
            group.sort()
            genGroups.append(group)
        elif y in listOfGenes:
            liY = whichGroups(y,genGroups,theMatrix) # Groups where x can be
            liY.sort()
            liY.reverse()
            group = [y]
            for idx in liY:
                group += genGroups[idx]
                del genGroups[idx]
            group = list(set(group))
            group.sort()
            genGroups.append(group)
        elif d < 0.5:
            idX = [i for i in range(len(genGroups)) if x in genGroups[i]]
            idY = [i for i in range(len(genGroups)) if y in genGroups[i]]
            if idX[0] != idY[0]:
                group = genGroups[idX[0]] + genGroups[idY[0]]
                if idX[0] < idY[0]:
                    del genGroups[idY[0]]
                    del genGroups[idX[0]]
                else:
                    del genGroups[idX[0]]
                    del genGroups[idY[0]]
                genGroups.append(group)
        # Now we have to errase the information from the ToDo list
        if x in listOfGenes:
            idx = listOfGenes.index(x)
            del listOfGenes[idx]
        if y in listOfGenes:
            idx = listOfGenes.index(y)
            del listOfGenes[idx]
        del ordCoor[0]
        del ordDist[0]

    # In case we have not yet grouped all the Genes
    while len(listOfGenes) > 0:
        x = listOfGenes[0]
        liX = whichGroups(x,genGroups,theMatrix)
        liX.sort()
        liX.reverse()
        group = [x]
        for idx in liX:
            group += genGroups[idx]
            del genGroups[idx]
        group = list(set(group))
        group.sort()
        genGroups.append(group)
        del listOfGenes[0]

    # Now, FINALLY, the return
    return genGroups


############
# ORDERING #
############

def groupOrdering(genGroup, theMatrix):
    # This method takes a group of genes 'genGroup' (nonempty subset of
    # range(len(theMatrix))) and a recombinant probability matrix theMatrix. It
    # returns a dictionary with several entries:
    #  - success: A boolean of whether or not the information is consistent.
    #  - ordGrp: The group ordered. Empty if success is False
    #  - message: A string specifying the first inconsisntency found, if any.
    #  - inferred: A list of elements [i,j,d], where the distance i,j has been
    #             inferred from the distances given as d.
    #  - matrix: The matrix with the inferred values inserted.
    #
    # We define a global variable TOL, that is a tolerance, and we consider
    # inconsistent, if x, y, z are the genes, and d_xy, d_yz and d_xz the
    # respective distances, (lets assume d_xy <= d_yz <= d_xz), then, we
    # consider inconsistent the distances if abs(1-(d_xy+d_yz)/d_xz) => TOL.
    #
    message = ""
    inferred = []
    N = len(genGroup)
    genGroup.sort()
    cGenGroup = [x for x in genGroup]
    first   = -1
    last    = -1
    maxdist = -1
    theI    = -1
    theJ    = -1
    changed = False # This is the flag to check that the variables have changed
    for i in range(N-1):
        for j in range(i+1,N):
            if theMatrix[genGroup[i]][genGroup[j]] > maxdist:
                maxdist = theMatrix[genGroup[i]][genGroup[j]]
                first = genGroup[i]
                last  = genGroup[j]
                theI  = i
                theJ  = j
                changed = True
    # Now we initialize our variables and delete from cGenGroup the genes that
    # have already been located.
    ordGrp = [first,last]
    del cGenGroup[theJ]
    del cGenGroup[theI]
    stillConsistent = True
    while len(cGenGroup) > 0 and stillConsistent:
        # We will make a search of a pair that is
        M = len(cGenGroup)
        K = len(ordGrp)
        allDistancesThere = []
        notResetYet = True
        insertIdx = -1
        k = 0
        while k < M and notResetYet:
            for j in range(K):
                x = theMatrix[cGenGroup[k]][ordGrp[j]]
                allDistancesThere.append(not isnan(x))
            if all(allDistancesThere):
                # Consistency Check
                i = 0
                while i < K-1 and stillConsistent:
                    j = i+1
                    while j < K and stillConsistent:
                        x = theMatrix[ordGrp[i]][ordGrp[j]]
                        y = theMatrix[cGenGroup[k]][ordGrp[i]]
                        z = theMatrix[ordGrp[j]][cGenGroup[k]]
                        a = max(x,y,z)
                        t = abs(1-(x+y+z-a)/a)
                        if t > TOL:
                            message  = "Inconsistencia detectada entre genes "
                            message += str(ordGrp[i]) + ", " + str(ordGrp[j])
                            message += " y " + str(cGenGroup[k]) + "."
                            stillConsistent = False
                            notResetYet     = False
                        elif x == a and j == i + 1:
                            # This should happen only once.
                            insertIdx = j
                        j += 1
                    i += 1
                if stillConsistent:
                    notResetYet = False
                    ordGrp.insert(insertIdx,cGenGroup[k])
                    del cGenGroup[0]
            else:
                k += 1
        if notResetYet and stillConsistent:
            allDistancesThere = []
            for j in range(K):
                x = theMatrix[cGenGroup[0]][ordGrp[j]]
                if not isnan(x):
                    allDistancesThere.append(not isnan(x))
            if sum(allDistancesThere) < 2:
                message  = "Inconsistencia detectada, gen " + str(cGenGroup[0])
                message += " no tiene suficientes distancias para ser incluido."
                stillConsistent = False
            else:
                # I need to include the guy in this case. Basically I have to
                # check consistency and insert it in the right place.
                nonZero = [i for i in range(len(allDistancesThere))
                                if allDistancesThere[i]]
                i = 0
                d = 1
                mark = -1 # 0: the new gene is in the middle of the two analized.
                          # 1: the new gene is before the first of the analized.
                          # 2: the new gene is after the last of the analized.
                theI = -1
                theJ = -1
                while i < len(nonZero) - 1  and stillConsistent:
                    j = i+1
                    while j < len(nonZero) and stillConsistent:
                        x = theMatrix[ordGrp[nonZero[i]]][ordGrp[nonZero[j]]]
                        y = theMatrix[cGenGroup[0]][ordGrp[i]]
                        z = theMatrix[ordGrp[j]][cGenGroup[0]]
                        a = max(x,y,z)
                        t = abs(1-(x+y+z-a)/a)
                        if t > TOL:
                            message  = "Inconsistencia detectada entre genes "
                            message += str(ordGrp[nonZero[i]]) + ", "
                            message += str(ordGrp[nonZero[j]]) + " y "
                            message += str(cGenGroup[0]) + "."
                            stillConsistent = False
                            notResetYet     = False
                        elif a == x and x < d:
                            d = x
                            theI = i
                            theJ = j
                            mark = 0
                        elif mark < 0:
                            theI = i
                            theJ = j
                            if a == x: # In the middle
                                d = x
                                mark = 0
                            else:
                                d = min(1,y+z)
                                if a == y: # After
                                    mark = 2
                                else:
                                    mark = 1
                if stillConsistent:
                    notLocated = True
                    idx1 = nonZero[theI] # Lower extreme
                    idx2 = nonZero[theJ] # Upper extreme
                    if mark == 0: # The new guy is in the middle of the other 2.
                        k = idx1 + 1
                        x = theMatrix[cGenGroup[0]][ordGrp[idx1]]
                        if k == idx2: # They are consecutive
                            ordGrp.insert(k,cGenGroup[0])
                            notLocated = False
                        else:
                            while k < idx2 and notLocated:
                                y = theMatrix[ordGrp[idx1]][ordGrp[k]]
                                if x < y:
                                    ordGrp.insert(k,cGenGroup[0])
                                    notLocated = False
                                else:
                                    k += 1
                            if notLocated:
                                ordGrp.insert(idx2,cGenGroup[0])
                                notLocated = False
                    elif mark == 1: # The new guy is before the other 2
                        k = 0
                        x = theMatrix[cGenGroup[0]][ordGrp[idx1]]
                        if k == idx1:
                            ordGrp.insert(k,cGenGroup[0])
                            notLocated = False
                        else:
                            while k < idx1 and notLocated:
                                y = theMatrix[ordGrp[idx1]][ordGrp[k]]
                                if x > y:
                                    ordGrp.insert(k,cGenGroup[0])
                                    notLocated = False
                                else:
                                    k += 1
                            if notLocated:
                                ordGrp.insert(idx1,cGenGroup[0])
                                notLocated = False
                    elif mark == 2: # The new guy is after the other 2
                        k = idx2+1
                        x = theMatrix[cGenGroup[0]][ordGrp[idx2]]
                        if k == K-1:
                            ordGrp.insert(K,cGenGroup[0])
                            notLocated = False
                        else:
                            while k < K and notLocated:
                                y = theMatrix[ordGrp[idx2]][ordGrp[k]]
                                if x < y:
                                    ordGrp.insert(k,cGenGroup[0])
                                    notLocated = False
                                else:
                                    k += 1
                            if notLocated:
                                ordGrp.insert(K,cGenGroup[0])
                                notLocated = False

                    if notLocated: # It should never get here, but just in case.
                        # This condition is added just to ensure termination.
                        message = "Error desconocido"
                        stillConsistent = False
                    else: # Inference and delition
                        K = len(ordGrp)
                        idx = ordGrp.index(cGenGroup[0])
                        pvt = -1
                        k = 0
                        while pvt < 0 and k < K: # We are searching for a pivot
                            if k == idx:
                                k += 1
                            elif isnan(theMatrix[ordGrp[k]][ordGrp[idx]]):
                                k += 1
                            else:
                                pvt = k
                        # Once pivot is found
                        pd = theMatrix[ordGrp[pvt]][ordGrp[idx]]
                        for k in range(K):
                            if isnan(theMatrix[ordGrp[k]][ordGrp[idx]]):
                                nd = theMatrix[ordGrp[pvt]][ordGrp[k]]
                                if max(abs(pvt-idx), abs(pvt-k)) < abs(idx-k):
                                    d = nd + pd
                                else:
                                    d = abs(pd - nd)
                                theMatrix[ordGrp[k]][ordGrp[idx]] = d
                                theMatrix[ordGrp[idx]][ordGrp[k]] = d
                                inferred.append([ordGrp[k],ordGrp[idx],d])
                                inferred.append(ordGrp[idx],[ordGrp[k],d])
    package = {}
    package.update({"success":stillConsistent})
    package.update({"ordGrp":ordGrp})
    package.update({"inferred":inferred})
    package.update({"matrix":theMatrix})
    package.update({"message":message})
    return package


###########
# SPACING #
###########
def genSpacing(ordGrp,theMatrix):
    # This method takes a linkage group and a distance matrix. It assumes the
    # group (it is a list of indices) is already ordered according to the method
    # genOrdering, and it assumes that theMatrix is given after all the values
    # that needed to be inferred already were added to this matrix. Returns:
    #
    #  - disVec: list of distances where disVec[i] is the distance between the
    #            gen ordGrp[i] and ordGrp[i+1]. This is, disVec length one less
    #            than ordGrp.
    #
    disVec = []
    if len(ordGrp) > 1:
        for k in range(len(ordGrp)-1):
            disVec.append(theMatrix[ordGrp[k]][ordGrp[k+1]])
    disVec.append(0)
    return disVec


#################
# OTHER METHODS #
#################
def whichGroups(idx,groups,matrix):
    # This method searches to find which groups in the array of groups have
    # elements with a recombinant probability of less than 0.5 with the element
    # given by idx by
    possibleGroups = []
    L = len(groups)
    if L > 0:
        for i in range(L):
            for idy in groups[i]:
                if matrix[idx][idy] <=0.5:
                    possibleGroups.append(i)
    return list(set(possibleGroups))
