#import des différentes librairies
from math import *
import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm
import math 
from numba import jit

############################################################################
#profil de température selon la solution analytique
@jit(nopython=True)
def solution_analytique(U1,U2,Lx,Ly,Px,Py,n):
    Dx=Lx/(Px-1)   #On met Px-1 car pour Px point, il y a Px-1 intervalle
    Dy=Ly/(Py-1)   #idem
    Temp_i=np.zeros((Py,Px)) #on initialise la matrice de température
        
    #calcul du profil de température avec la solution analytique
    print("Solution analytique : calcul en cours")
    #on parcourt la matrice de température
    #les boucles en i et j ont été inversées pour des questions d'affichage
    for j in range(0,Py):
        for i in range(0,Px):
            #on initialise la somme à 0
            somme = 0
            #calcul de la somme
            #ne pouvant simuler l'infini, on arrête la somme à n (supposé grand)
            for k in range(0,n):
                somme += (1/(2*k+1))*sin(((2*k+1)*pi*Dx*i)/Lx)*((exp(-Dy*j*(2*k+1)*pi/Lx)-exp((-2*Ly+Dy*j)*(2*k+1)*pi/Lx))/(1-exp(-2*Ly*(2*k+1)*pi/Lx)))
            #calcul de la température au noeud (j,i)
            Temp_i[j,i]=U2+((4*(U1-U2))/pi)*somme     
    #Pour les points (0,0) et (Lx,0), on fait une moyenne entre les points adjacents pour assurer
    #la continuité de la température aux bords
    Temp_i[0,0]=(Temp_i[0,1]+Temp_i[1,0])/2
    Temp_i[0,Px-1]=(Temp_i[0,Px-2]+Temp_i[1,Px-1])/2
    return Temp_i



