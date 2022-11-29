import argparse
import os
import core
import nuDat
import solver


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Core Inventory solver')
    parser.add_argument(
        'input',
        help='Filepath to a  settings input file written in python. This must always be entered.',
        type=str
    )

    args = parser.parse_args()

    basedir = os.path.dirname(os.path.realpath(__file__))
    input = open(args.input, "r")
    jobdir = os.path.dirname(os.path.realpath(args.input))
    vars = input.read()


    # Define Inventory Properties
    invNames = [""]
    atomMass = [0]
    crossSec = [0.0]
    decConst = [0.0]
    neuYield = [0.0]
    fisYield = [0.0]
    absYield = [[0.0]]
    decYield = [[0.0]]

    # Core Constants
    source = 0.0
    leak = 0.0
    coreVolume = 1

    # Starting Values
    inv = [0.0]
    flux = 0.0

    # Simulation Properties
    tf = 1
    dt = 0.001
    rr = 1
    plotter = False
    csv = False
    outputFile = "out.csv"

    exec(vars)



    #set objects
    nuclearData = nuDat.NuDat()
    nuclearData.setData(invNames,atomMass,crossSec,decConst,neuYield,fisYield,absYield,decYield)

    theCore = core.Core()
    theCore.setVariables(inv,flux)
    theCore.setProperties(source,leak,coreVolume)

    model = solver.Solver()
    model.setNudat(nuclearData)

    #run model
    model.solve(theCore,dt,tf,rr)

    #generate output
    if csv:
#        print(theCore.history[-1])
        theCore.csvFromHistory(outputFile)

    if plotter:
        theCore.visualiseHistory()
