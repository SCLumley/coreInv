import core
import numpy as np
import nuDat


class Solver:
    def __init__(self):
        self.invV = np.array([])
        self.atomMassV = np.array([])
        self.crossSecV = np.array([])
        self.decConstV = np.array([])
        self.neuYieldV = np.array([])
        self.fisYieldV = np.array([])
        self.absYieldM = np.array([])
        self.decYieldM = np.array([[]])
        self.ident = np.identity(1)

        self.flux = 0
        self.rho = 0
        self.beta = 0


        self.dataIsSet = False

    def setNudat(self,nudat:nuDat):
        self.invNames = nudat.invNames
        self.atomMassV = np.array(nudat.atomMass)
        self.crossSecV = np.array(nudat.crossSec) * 1E-28 * 6.0221409E+23
        self.decConstV = np.array(nudat.decConst)
        self.neuYieldV = np.array(nudat.neuYield)
        self.fisYieldV = np.array(nudat.fisYield)
        self.absYieldM = np.array(nudat.absYield)
        self.decYieldM = np.array(nudat.decYield)
        self.ident = np.identity(len(nudat.invNames))
        self.dataIsSet = True

    def dinvdt(self,invV, flux):
        transMat = (flux * np.diag(self.crossSecV)) @ (self.absYieldM - self.ident) + np.diag(self.decConstV) @ (self.decYieldM - self.ident)
        dinv_dt = transMat.transpose() @ invV
        return dinv_dt

    def dfluxdt(self,invV, flux, leak, source):
        absProd = flux * self.fisYieldV @ (self.crossSecV * invV)
        decProd = self.neuYieldV @ (self.decConstV * invV)
        absLoss = flux * (self.crossSecV @ invV)
        leakage = flux * leak
#        print(absProd,decProd,absLoss,leakage,flux)
        dflux_dt = source + absProd + decProd - absLoss - leakage
        self.rho = (dflux_dt - source)/flux
#        self.rho = (absProd - (absLoss + leakage)) / flux
        self.beta = decProd / (decProd + absProd)
        return dflux_dt

    def step(self,core:core,dt,batch=False):

        if batch is False:
            self.invV = ( (np.array(core.inv) * 1000 ) / self.atomMassV )  / core.coreVolume
            self.flux = core.flux

        # integrators
        # forward euler
        # invV =  invV + dinvdt(invV,flux) * dt
        # flux = flux + dfluxdt(invV,flux)[0] * dt

        # RK4
        invk1 = self.dinvdt(self.invV, self.flux)
        fluxk1 = self.dfluxdt(self.invV, self.flux, core.leak, core.source)

        invk2 = self.dinvdt(self.invV + invk1 * (dt / 2), self.flux + fluxk1 * (dt / 2))
        fluxk2 = self.dfluxdt(self.invV + invk1 * (dt / 2), self.flux + fluxk1 * (dt / 2), core.leak, core.source)

        invk3 = self.dinvdt(self.invV + invk2 * (dt / 2), self.flux + fluxk2 * (dt / 2))
        fluxk3 = self.dfluxdt(self.invV + invk2 * (dt / 2), self.flux + fluxk2 * (dt / 2), core.leak, core.source)

        invk4 = self.dinvdt(self.invV + invk3 * dt, self.flux + fluxk3 * dt)
        fluxk4 = self.dfluxdt(self.invV + invk3 * dt, self.flux + fluxk3 * dt, core.leak, core.source)

        self.invV = self.invV + 1 / 6 * dt * (invk1 + 2 * invk2 + 2 * invk3 + invk4)
        self.flux = self.flux + 1 / 6 * dt * (fluxk1 + 2 * fluxk2 + 2 * fluxk3 + fluxk4)

        if batch is False:
            core.inv = list(self.invV)
            core.flux = self.flux

    def solve(self,core:core,dt,tf,rr=0):
        self.invV = ((np.array(core.inv) * 1000) / self.atomMassV) / core.coreVolume
        self.flux = core.flux
        self.t = 0
        self.i = 0
        while self.t < tf :
            if rr > 0 and self.i % rr == 0:
                dataDict = {
                    "i" : self.i,
                    "t" : self.t,
                    "rho" : self.rho,
                    "beta" : self.beta,
                    "power" : self.flux * 1.9297067E+13 / 2.3 - core.source,
                    "flux" : self.flux
                }
                for name,amount in zip(self.invNames,list(self.invV)):
                    dataDict["s_"+ name] = amount

                core.writeHistory(dataDict)

#            print(self.i,self.t,self.flux)
            self.step(core,dt,True)
            self.t += dt
            self.i += 1

        core.inv = list(self.invV)
        core.flux = self.flux

