
#Nuclear Data
invNames=["Fuel","Precursors","Structure","Water","Xenon"]
atomMass=[235.0,117.5,178.49,18.0,135.0] 					#atomic mass of species in amu
crossSec=[99.0 + 583.0,0.0,50.2,0.40001,2.0E06]			#Microscopic cross section of absorption + fission (thermal) in barns
decConst=[0.0,0.4,0.0,0.0,2.10E-05]							#decay constant of species in s^(-1)
neuYield=[0.0,1.6,0.0,0.0,0.0]							#average neutron yield of decay 
fisYield=[2.3 * 0.85,0.0,0.0,0,0]						#average neutron yield of absorption event (normally fission)
absYield=[[0.0,0.01,0.0,0.0,0.0],						#yield matrix of [row] -> [column] species on absorption 
		  [0.0,0.0,0.0,0.0,0.0],
		  [0.0,0.0,1.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0,0.0]
		  ]
		  
decYield=[[0.0,0.0,0.0,0.0,0.0],						#yield matrix of [row] -> [column] species on decay
		  [0.0,0.0,0.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0,0.0],
		  [0.0,0.0,0.0,0.0,0.0]
		  ]

		  

#Core Constants
source=1.0E-12										#constant source term in mol s^(-1) (no directionality, so no area in units)
leak=0.2											#leakage fraction
coreVolume=2										#Core Volume in m^3

#Starting Values
inv=[90.6,0.0,700.0,1500.0,0.001]					#Initial core inventory in kg
flux=1.0E-13										#starting flux in mol s^(-1)         (no directionality, so no area in units)

#Simulation Properties
tf=300												#Simulation stopping time in s
dt=0.01												#Timestep in s
rr=100												#Record rate in cycles (i.e. record data for plot every [rr] cycles)
csv=True											#Write CSV	
plotter=True										#Plot output
