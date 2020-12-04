#math permet d'accéder aux fontions sin et sinh
from math import *
import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 

#définitions des différents paramètres

U0=294  #température initiale en K
U1=304  #température à la limite T1
U2=314  #température à la limite T2

Lx=200  #longueur de la plaque selon x (en cm)
Ly=100  #longueur de la plaque selon y (en cm)
Px=15   #nombre de points du maillage selon x
Py=16   #nombre de points du maillage selon y

somme=0 #on initialise la somme à 0 pour éviter les erreurs

#saisie de la limite de la somme, n tend vers l'infini initalement
def saisie_n():
    n = input("saisir le paramètre n (grand) : ")
    print("valeur choisie: ", n)
    return int(n)

#profil de température selon la solution analytique
def solution_analytique(U1,U2,Lx,Ly,Px,Py):
    n = saisie_n()
    
    global somme
    Dx=Lx/Px
    Dy=Ly/Py
    Temp_i=np.zeros((Py,Px))

    #conditions limites
    for i in range(0,Px):
        Temp_i[0,i]=U2
        Temp_i[Py-1,i]=U2
    for j in range(0,Py):
        Temp_i[j,0]=U1
        Temp_i[j,Px-1]=U2
        
    #remplissage de la matrice avec la solution analytique
    for j in range(1,Py-1):
        for i in range(1,Px-1):
            for k in range(1,n):
                try:
                    somme += (1/(2*k+1))*sin(((2*k+1)*pi*Dx*i)/Lx)*((exp(-Dy*j*(2*k+1)*pi/Lx)-exp((-2*Ly+Dy*j)*(2*k+1)*pi/Lx))/(1-exp(-2*Ly*(2*k+1)*pi/Lx)))
                except OverflowError:
                    somme = float('inf')
            Temp_i[j,i]=U2+((4*(U1-U2))/pi)*somme
            print(" y=",j,"x=",i, "tab= ",Temp_i[j,i])
    return Temp_i


#affichage du profil de température
#ajouter le ss programme de Camille sur la stabilité en fct de comment on organise les modules
def affichage_profil(U1,U2,Lx,Ly,Px,Py):
    #si stabilité
    Temp_i = solution_analytique(U1,U2,Lx,Ly,Px,Py)
    mini=np.min([U0,U1,U2])
    maxi=np.max([U0,U1,U2])
    with open("solana.txt", "w") as filout:
        filout.write("{}\n".format(Temp_i))
        plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi) 
        plt.show() 
    return Temp_i

affichage_profil(U1,U2,Lx,Ly,Px,Py)


