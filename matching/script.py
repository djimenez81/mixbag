from matching import *
degrees, choices = generatePolyMatchingData(20,1,3,10,15)
matches = polyMatching(degrees,choices)
matches[0]
matches[1]
matches[2]






fo = generateOptions(10)
mo = generateOptions(10)
match = galeShapley(mo,fo)
match
