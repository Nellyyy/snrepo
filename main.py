import solution_numerique as sn
import saisie_param as sp
import hello as solana

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 
import sys

############################################################################
#affichage de la température sous forme d'isothermes
#le paramètre solution sert pour l'affichage du titre :
#   si solution=numerique, on souhaite afficher la solution numérique
#   si solution=analytique, on souhaite afficher la solution analytique

def affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,Temp_i,solution):
    mini=np.min([U0,U1,U2])
    maxi=np.max([U0,U1,U2])
    with open("temperature_finale_numerique.txt", "w") as filout:
        filout.write("{}\n".format(Temp_i))
        plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi)
        
        #titre du graphique en fonction du paramètre solution
        if solution=="numerique":
            plt.title("Profil de température avec solution numérique pour Px="+str(Px)+", Py="+str(Py))
        elif solution=="analytique":
            plt.title("Profil de température avec solution analytique pour Px="+str(Px)+", Py="+str(Py)+", N=1000")   

        #légende pour le dégradé de couleur
        plt.colorbar()

        plt.show()


############################################################################
#calcul de la différence entre la température obtenue par solution analytique et 
#celle obtenue par solution numérique

def difference_solution(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt):
    Temp_analytique=solana.solution_analytique(U1,U2,Lx,Ly,Px,Py)
    Temp_numerique=(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/1000000))[3]
    
    Temp_diff=Temp_analytique-Temp_numerique
    
    mini=np.min(Temp_diff)
    maxi=np.max(Temp_diff)
    
    plt.pcolormesh(Temp_diff, cmap=plt.cm.OrRd, vmin=mini, vmax=maxi)
    plt.title("Différence entre les profils de température obtenus de manière analytique et numérique")
    #légende pour le dégradé de couleur
    plt.colorbar()
    plt.show()
    
    return Temp_diff

############################################################################ 
#affichage de l'erreur en fonction du maillage 
def calcul_erreur(Lx,Ly,a,U0,U1,U2,Ttot):
    maillage_spatial=[500] #point pour faire une régression linéaire
    
    #on détermine un maillage de temps respectant la stabilité
    maillage_temporel=[]
    Fx=[]
    Fy=[]
    for i in range(len(maillage_spatial)):
        Dx=Lx/maillage_spatial[i]
        Dy=Lx/maillage_spatial[i]

        nbr_stab=a/Dx**2+a/Dy**2

        nbr_Fourier=0.45
        Pt=int(Ttot/(nbr_Fourier/nbr_stab))
        
        maillage_temporel.append(Pt)
        
    #on calcule l'erreur pour différent maillage spatial 
    erreur=[]
    for i in range(len(maillage_spatial)):
        Px=Py=maillage_spatial[i]
        Pt=maillage_temporel[i]
        
        Temp_analytique=solana.solution_analytique(U1,U2,Lx,Ly,Px,Py)
        Temp_numerique=(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/100000))[3]
    
        Temp_diff=Temp_analytique-Temp_numerique
        
        erreur.append(np.max(Temp_diff))
    
    return Temp_diff, np.max(Temp_diff), erreur

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
    #n = int(sp.saisie_n())
    
    #saisie en dur pour tests
    Lx = 1
    Ly = 1
    Px = 15
    Py = 15
    U0 = 200
    U1 = 304
    U2 = 400
    a = 0.000098
    Ttot = 1000
    Pt = 10000
    
    #affichage de la solution analytique
    #affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,solana.solution_analytique(U1,U2,Lx,Ly,Px,Py),"analytique")
    
    #affichage de la solution des différences finies
    #affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/100000))[3],"numerique")
    
    #affichage de la difference de temperature
    #difference_solution(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt)
    
    print(calcul_erreur(Lx,Ly,a,U0,U1,U2,Ttot))
    
    
main()


