# Proyecto Cruces Mendelianos de PF 5026 Paradigmas de Computacion
# Este archivo contiene la parte logica del proyecto programado.
# 
# Grupo:
#    Mario Bogantes
#    David Jimenez
#    Denis Jimenez
#    Jeffry Ortiz
#

__DOMINANT  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
__RECESSIVE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z']

def allPhenotypes(n,dom,rec):
  # This function returns all the possible combinations of phenotypes given
  # a number of characteristics n.
  # j is the total number of phenotypes that one can find.
  k = 3**n
  # Start all the phenotypes as empty strings
  phenList = ['' for phen in range(k)]
  for j in range(n):
    # The phenotype for the j-th characteristic.
    homDom = dom[j]+dom[j]
    homRec = rec[j]+rec[j]
    hetCyg = dom[j]+rec[j]
    
    for i in range(k):
      # We traverse all the partial phenotypes, and index indicate the 
      # phenotype of the current characteristic that has to be computed.
      index = (i//(3**(n-j-1)))%3
      if index == 0:
        phenList[i] = phenList[i] + homDom 
      elif index == 1:
        phenList[i] = phenList[i] + hetCyg 
      else:
        phenList[i] = phenList[i] + homRec 
  return phenList




def allPhenDec(dadPhen, momPhen):
  # This function returns all the possible phenotypes of decendents. It assumes
  # that both strings are of the same size, such size is even, and it is 
  # correctly formated. 
  n = len(dadPhen) // 2
  # The lists dadDomRec and momDomRec correspond to the list, on each characteristic, 
  # of whether or not it is heterocygot (1), homocygot dominant (1), or homocygot
  # recessive (2)
  dadDomRec = [-1 for i in range(n)]
  momDomRec = [-1 for i in range(n)]
  dom = ['' for i in range(n)]
  rec = ['' for i in range(n)]
  for i in range(n):
    # We go over the sequences and check for homocygocity, dominant 
    # heterocigocity or recessive heterocygocity, and the character of each
    # characteristic.
    
    # First dad
    allele1 = dadPhen[2*i]
    allele2 = dadPhen[2*i+1]
    dom[i] = allele1.upper()
    rec[i] = allele1.lower()
    if allele1 == allele2:
      if allele1 == allele1.upper():
        dadDomRec[i] = 0
      else:
        dadDomRec[i] = 2
    else:
      dadDomRec[i] = 1
      
    # Now mom
    allele1 = momPhen[2*i]
    allele2 = momPhen[2*i+1]
    if allele1 == allele2:
      if allele1 == allele1.upper():
        momDomRec[i] = 0
      else:
        momDomRec[i] = 2
    else:
      momDomRec[i] = 1
      
  probabilities = [1]
  phenotypes = ['']
  
  # Now generate all the possible phenotypes of decendants
  for i in range(n-1,-1,-1):
    # If mom is homocygot dominant
    if momDomRec[i] == 0:
      
      # If dad is homocygot dominant
      if dadDomRec[i] == 0:
        homDom = dom[i] + dom[i]
        phenotypes = [homDom+s for s in phenotypes]
      
      # If dad is heterocygot
      elif dadDomRec[i] == 1:
        
        homDom = dom[i] + dom[i]        
        hetCyg = dom[i] + rec[i]
        
        homDomProb = [x*0.5 for x in probabilities]
        hetCygProb = [x*0.5 for x in probabilities]
        
        homDomPhen = [homDom+s for s in phenotypes]
        hetCygPhen = [hetCyg+s for s in phenotypes]
        
        probabilities = homDomProb + hetCygProb
        phenotypes    = homDomPhen + hetCygPhen
        
      # If dad is homocygot recessive
      else:
        hetCyg = dom[i] + rec[i]
        phenotypes = [hetCyg+s for s in phenotypes]
        
    # If mom is heterocygot
    elif momDomRec [i] == 1:
      # If dad is homocygot dominant
      if dadDomRec[i] == 0:
        
        homDom = dom[i] + dom[i]        
        hetCyg = dom[i] + rec[i]
        
        homDomProb = [x*0.5 for x in probabilities]
        hetCygProb = [x*0.5 for x in probabilities]        
        
        homDomPhen = [homDom+s for s in phenotypes]
        hetCygPhen = [hetCyg+s for s in phenotypes]
        
        probabilities = homDomProb + hetCygProb
        phenotypes    = homDomPhen + hetCygPhen
      
      # If dad is heterocygot
      elif dadDomRec[i] == 1:
        
        homDom = dom[i] + dom[i]        
        hetCyg = dom[i] + rec[i]
        homRec = rec[i] + rec[i]  
        
        homDomProb = [x*0.25 for x in probabilities]
        hetCygProb = [x*0.50 for x in probabilities]
        homRecProb = [x*0.25 for x in probabilities]
        
        homDomPhen = [homDom+s for s in phenotypes]
        hetCygPhen = [hetCyg+s for s in phenotypes]
        homRecPhen = [homRec+s for s in phenotypes]

        probabilities = homDomProb + hetCygProb + homRecProb
        phenotypes    = homDomPhen + hetCygPhen + homRecPhen


        # If dad is homocygot recessive
      else:
        
        hetCyg = dom[i] + rec[i]
        homRec = rec[i] + rec[i]        
        
        hetCygProb = [x*0.5 for x in probabilities]
        homRecProb = [x*0.5 for x in probabilities]
        
        hetCygPhen = [hetCyg+s for s in phenotypes]
        homRecPhen = [homRec+s for s in phenotypes]
        
        probabilities = hetCygProb + homRecProb
        phenotypes    = hetCygPhen + homRecPhen
        
    # If mom is homocygot recessive
    else:
      
      # If dad is homocygot dominant
      if dadDomRec[i] == 0:
        
        hetCyg = dom[i] + rec[i]
        phenotypes = [hetCyg+s for s in phenotypes]
        
      # If dad is heterocygot
      elif dadDomRec[i] == 1:
        
        hetCyg = dom[i] + rec[i]
        homRec = rec[i] + rec[i]        
        
        hetCygProb = [x*0.5 for x in probabilities]
        homRecProb = [x*0.5 for x in probabilities]
        
        hetCygPhen = [hetCyg+s for s in phenotypes]
        homRecPhen = [homRec+s for s in phenotypes]
        
        probabilities = hetCygProb + homRecProb
        phenotypes    = hetCygPhen + homRecPhen
        
      # if dad is homocygot recessive
      else:
        homRec = rec[i] + rec[i]
        phenotypes = [homRec+s for s in phenotypes]
        
  # After so many cases, returns probabilities and phenotypes
  return phenotypes,probabilities
  