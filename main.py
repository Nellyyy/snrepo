import solution_numerique as sn
import saisie_param as sp
import hello as solana

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 
import sys

############################################################################
#affichage de la temp�rature sous forme d'isothermes
#le param�tre solution sert pour l'affichage du titre :
#   si solution=numerique, on souhaite afficher la solution num�rique
#   si solution=analytique, on souhaite afficher la solution analytique
#   si solution=difference, on souhaite afficher la diff�rence des 2 solutions

def affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,Temp_i,solution):
    mini=np.min([U0,U1,U2])
    maxi=np.max([U0,U1,U2])
    with open("temperature_finale_numerique.txt", "w") as filout:
        filout.write("{}\n".format(Temp_i))
        plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi)
        
        #titre du graphique en fonction du param�tre solution
        if solution=="numerique":
            plt.title("Profil de temp�rature avec solution num�rique pour Px="+str(Px)+", Py="+str(Py))
        elif solution=="analytique":
            plt.title("Profil de temp�rature avec solution analytique pour Px="+str(Px)+", Py="+str(Py)+", N=20")
        elif solution=="difference":
            plt.title("Diff�rence entre les profils de temp�rature obtenus de mani�re analytique et num�rique")
        plt.show()


############################################################################
#calcul de la diff�rence entre la temp�rature obtenue par solution analytique et 
#celle obtenue par solution num�rique

def difference_solution(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt):
    Temp_analytique=solana.solution_analytique(U1,U2,Lx,Ly,Px,Py)
    Temp_numerique=(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/1000000))[3]
    
    Temp_diff=Temp_analytique-Temp_numerique
    
    mini=np.min(Temp_diff)
    maxi=np.max(Temp_diff)
    
    plt.pcolormesh(Temp_diff, cmap=plt.cm.OrRd, vmin=mini, vmax=maxi)
    plt.show()
    
    return Temp_diff
    

############################################################################   
    
def main():
    #rappel des ss-programmes pour demander les parametres a l'utilisateur
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
    Lx = 1
    Ly = 1
    Px = 50
    Py = 50
    U0 = 294
    U1 = 304
    U2 = 314
    a = 0.000098
    Ttot = 1000
    Pt = 3000
    
    #affichage de la solution analytique
    #affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,solana.solution_analytique(U1,U2,Lx,Ly,Px,Py),"analytique")
    
    #affichage de la solution des différences finies
    #affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/100000))[3],"numerique")
    
    #affichage de la difference de temperature
    #difference_solution(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt)
    
    
    
main()


