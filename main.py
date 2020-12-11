#import des différentes librairies
import solution_numerique as sn
import saisie_param as sp
import solution_analytique as solana
import affiche_erreur as ae

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
        #dégradé de couleur
        plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi)
        
        #titre du graphique en fonction du paramètre solution
        if solution=="numerique":
            plt.title("Profil de température avec solution numérique pour Px="+str(Px)+", Py="+str(Py))
        elif solution=="analytique":
            plt.title("Profil de température avec solution analytique pour Px="+str(Px)+", Py="+str(Py)+", N=1000")   

        #légende pour le dégradé de couleur
        plt.colorbar()
        #affichage du profil de température
        plt.show()


############################################################################
#calcul de la différence entre la température obtenue par solution analytique et 
#celle obtenue par solution numérique

def difference_solution(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,n):
    #on trouve les profils de température pour chaque solution (lorsqu'on a atteint le régime permanent)
    Temp_analytique=solana.solution_analytique(U1,U2,Lx,Ly,Px,Py,n)
    Temp_numerique=(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/1000000))[3]
    #on calcule la différence des solutions pour chaque noeud
    Temp_diff=Temp_analytique-Temp_numerique
    
    mini=np.min(Temp_diff)
    maxi=np.max(Temp_diff)
    #dégradé de couleur de la différence obtenue
    plt.pcolormesh(Temp_diff, cmap=plt.cm.OrRd, vmin=mini, vmax=maxi)
    plt.title("Différence entre les profils de température obtenus de manière analytique et numérique")
    #légende pour le dégradé de couleur
    plt.colorbar()
    #affichage du profil de température
    plt.show()
    
    return Temp_diff


############################################################################   
    
def main():
    #appel des ss-programmes pour demander les parametres à l'utilisateur
    #à décommenter si besoin pour une saisie utilisateur
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
    n=1000
    
    
    #affichage de la solution analytique
    #affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,solana.solution_analytique(U1,U2,Lx,Ly,Px,Py,n),"analytique")
    
    #affichage de la solution des différences finies
    #affichage_profil(U1,U2,U0,Lx,Ly,Px,Py,(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/100000))[3],"numerique")
    
    #affichage de la difference de temperature
    #difference_solution(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,n)
    
    #print(ae.calcul_erreur(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,n))
    print(ae.affichage_erreur(Lx,Ly,a,U0,U1,U2,Ttot,n))
    
    
main()


