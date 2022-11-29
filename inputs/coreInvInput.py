
#Nuclear Data Properties
invNames=["Fuel","Precursors","Absorber","Water"]
atomMass=[235.0,117.5,178.49,18.0] 					#atomic mass of species in amu
crossSec=[99.0 + 583.0,0.0,104.2,0.40001]			#Microscopic cross section of absorption + fission (thermal) in barns
decConst=[0.0,4,0.0,0]							#decay constant of species in s^(-1)
neuYield=[0.0,1.6,0.0,0]							#average neutron yield of decay 
fisYield=[2.3 * 0.85,0.0,0.0,0]						#average neutron yield of absorption event (normally fission)
absYield=[[0.0,0.01,0.0,0.0],						#yield matrix of [row] -> [column] species on absorption 
		  [0.0,0.0,0.0,0.0],
		  [0.0,0.0,1.0,0.0],
		  [0.0,0.0,0.0,0.0]
		  ]
		  
decYield=[[0.0,0.0,0.0,0.0],						#yield matrix of [row] -> [column] species on decay
		  [0.0,0.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0]
		  ]

		  

#Core Constants
#source=1e-14											#constant source term in mol s^(-1) (no directionality, so no area in units)
leak=0.2											#leakage fraction
coreVolume=2										#Core Volume in m^3

#Starting Values
inv=[100.0,1e-14,395.194133,2000]							#Initial core inventory in kg
#critical for starting values is about 395.194133 kg of absorber
flux=7.39315759621551E-13										#starting flux in mol s^(-1)         (no directionality, so no area in units)

#Simulation Properties
tf=200												#Simulation stopping time
dt=0.05												#Timestep in s
rr=10											#Record rate in cycles (i.e. record data for plot every [rr] cycles)
csv=True
plotter=True
outputFile = "input1.csv"
