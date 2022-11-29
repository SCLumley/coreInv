class NuDat:
    def __init__(self):
        self.invNames = [""]            #Names of all species in the core
        self.atomMass = [0]             #Atomic mass of species in amu
        self.crossSec = [0.0]           #Microscopic cross section of absorption + fission (thermal) in barns
        self.decConst = [0.0]           #decay constant of species in s^(-1)
        self.neuYield = [0.0]           #average neutron yield of decay
        self.fisYield = [0.0]           #average neutron yield of absorption event (normally fission)
        self.absYield = [[0.0]]         #yield matrix of [row] -> [column] species on absorption
        self.decYield = [[0.0]]         #yield matrix of [row] -> [column] species on decay

    def setData(self,invNames,atomMass,crossSec,decConst,neuYield,fisYield,absYield,decYield):
        self.invNames = invNames
        self.atomMass = atomMass
        self.crossSec = crossSec
        self.decConst = decConst
        self.neuYield = neuYield
        self.fisYield = fisYield
        self.absYield = absYield
        self.decYield = decYield