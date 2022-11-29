import numpy
from typing import List
import pandas
import csv


class Core:
    def __init__(self):

        # Core Constants
        self.source = 0.0               #constant source term in mol s^(-1) (no directionality, so no area in units)
        self.leak = 0.0                 #leakage fraction
        self.coreVolume = 1             #Core Volume in m^3

        # Starting Values
        self.inv = [0.0]                #Initial core inventory in kg
        self.flux = 0.0                 #starting flux in mol s^(-1)         (no directionality, so no area in units)

        self.variables = False
        self.properties = False

        self.history = []


    def setVariables(self,inv,flux):
        self.inv=inv
        self.flux=flux
        self.variables = True

    def setProperties(self,source,leak,coreVolume):
        self.source = source
        self.leak = leak
        self.coreVolume = coreVolume
        self.properties = True

    def writeHistory(self,data:dict):
        self.history.append(data)


    def visualiseHistory(self):
        from mpl_toolkits.axes_grid1 import host_subplot
        import mpl_toolkits.axisartist as AA
        import matplotlib.pyplot as plt

        timeOut = [data["t"] for data in self.history]
        powerOut = [data["power"] for data in self.history]
        rhoOut = [data["rho"] for data in self.history]
        invOut = []
        invNames = []


        filteredHistory =[{k: v for k, v in stepData.items() if k.startswith('s_')} for stepData in self.history]
        invNames = [name.replace('s_','') for name in sorted(filteredHistory[0].keys())]
        for inv in filteredHistory:
            invOut.append([i for k,i in sorted(inv.items())])




        host = host_subplot(111, axes_class=AA.Axes)
        plt.subplots_adjust(right=0.75)

        par1 = host.twinx()
        par2 = host.twinx()

        offset = 65
        new_fixed_axis = par2.get_grid_helper().new_fixed_axis
        par2.axis["right"] = new_fixed_axis(loc="right", axes=par2, offset=(offset, 0))

        par2.axis["right"].toggle(all=True)
        par1.axis["right"].toggle(all=True)

        host.set_xlim(0, max(timeOut))
        host.set_ylim(1E-12, 1E4)
        host.set_yscale('log')

        host.set_xlabel("Time ($s$)")
        host.set_ylabel("Inventory ($kg/m^3$)")
        par1.set_ylabel("Flux ($W$, Fission power equivalent)")
        par1.set_yscale('log')
        par2.set_ylabel("Reactivity ($ΔK / K$)")

        h1 = host.plot(timeOut, invOut, label="Inventory")
        p1 = par1.plot(timeOut, powerOut, color='c', label="flux")
        # p1 = par1.plot(timeOut,  fluxOut, color='c', label="flux")
        p2 = par2.plot(timeOut, rhoOut, color='m', label="rho")

        # par2.set_ylim(-0.1, 0.1)
        host.legend(invNames)
        host.axis["left"].label.set_color(h1[0].get_color())
        par1.axis["right"].label.set_color(p1[0].get_color())
        par2.axis["right"].label.set_color(p2[0].get_color())

        plt.draw()
        plt.show()


    def csvFromHistory(self,handle='out.csv'):
        keys = self.history[0].keys()
        with open(handle, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file,fieldnames=keys)
            fc.writeheader()
            fc.writerows(self.history)
