import solution_numerique as sn
import saisie_param as sp
import solution_analytique as solana

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 
from scipy import stats
import sys

############################################################################
#calcul de l'erreur pour un maillage donné

def calcul_erreur(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,n):
    Temp_analytique=solana.solution_analytique(U1,U2,Lx,Ly,Px,Py,n)
    Temp_numerique=(sn.profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,1/1000000))[3]
    
    Temp_diff=Temp_analytique-Temp_numerique
    
    somme=0
    for j in range(0,Py):
        for i in range(0,Px):
            somme+=(Temp_diff[j,i])**2
    
    Dx=Lx/Px
    Dy=Ly/Py
    erreur=(somme*(Dx*Dy))**(1/2) #A VERIFIER DH=DX*DY
        
    return erreur

############################################################################
#calcul de l'erreur pour des maillages spatiaux de plus en plus raffinés
#affichage de l'erreur en fonction du maillage

def affichage_erreur(Lx,Ly,a,U0,U1,U2,Ttot,n):
    nbr_point_maillage_spatial=[200]
    
    #on détermine un maillage de temps respectant la stabilité
    nbr_point_maillage_temporel=[]
    
    for i in range(len(nbr_point_maillage_spatial)):
        Dx=Lx/nbr_point_maillage_spatial[i]
        Dy=Lx/nbr_point_maillage_spatial[i]

        nbr_stab=a/Dx**2+a/Dy**2

        nbr_Fourier=0.45
        Pt=int(Ttot/(nbr_Fourier/nbr_stab))
        
        nbr_point_maillage_temporel.append(Pt)
    
    #calcul de l'erreur pour chaque maillage spatial
    liste_erreur=[]
    
    for i in range(len(nbr_point_maillage_spatial)):
        Px=Py=nbr_point_maillage_spatial[i]
        Pt=nbr_point_maillage_temporel[i]
        liste_erreur.append(calcul_erreur(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,n))
    
    return liste_erreur
   
    
############################################################################
#régression linéaire 

maillage=np.array([10,50,100,200])
erreur=np.array([20,16,4,2])

def regression_lineaire(maillage,erreur):
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(maillage, erreur)
    print("slope: %f    intercept: %f" % (slope, intercept))
    print("R-squared: %f" % r_value**2)

    plt.plot(maillage, erreur, 'o', label='original data')
    plt.plot(maillage, intercept + slope*maillage, 'r', label='fitted line')
    plt.legend()
    plt.show()
    
regression_lineaire(maillage,erreur)