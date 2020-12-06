import Sciences_numériques as sn
import saisie_param as sp
import hello as solana

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 
import sys

############################################################################
#affichage de la température : à mettre dans le "main" ensuite
#j'ai rajouté la température à afficher dans les paramètres de la fonction, 
#comme ça la fonction affichage est générale

def affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,Temp_i):
    mini=np.min([U0,U1,U2])
    maxi=np.max([U0,U1,U2])
    with open("temperature_finale_numerique.txt", "w") as filout:
        filout.write("{}\n".format(Temp_i))
        plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi) 
        plt.show()

def main():

#appel des ss-programmes pour demander les paramètres à l'utilisateur
	#Lx = float(sp.saisie_Lx())
	#Ly = float(sp.saisie_Ly())
	#Px = int(sp.saisie_Px())
	#Py = int(sp.saisie_Py())
	#U0 = float(sp.saisie_U0())
	#U1 = float(sp.saisie_U1())
	#U2 = float(sp.saisie_U2())
	#a = float(sp.saisie_a())
	#Ttot = int(sp.saisie_Ttot())
	#Pt = int(sp.saisie_Pt())

#saisie en dur pour tests
	Lx = 100
	Ly = 90
	Px = 10
	Py = 10
	U0 = 294
	U1 = 304
	U2 = 314
	a = 0.000098
	Ttot = 100
	Pt = 400

#affichage de la solution analytique
	#affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,solana.solution_analytique(U1,U2,Lx,Ly,Px,Py))

#affichage de la solution des différences finies
	#affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/100000)[3])


main()
