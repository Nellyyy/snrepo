#math permet d'accéder à la fontion exp
from math import *
import numpy as np

import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 

#paramètres en dur pour les tests

#U0=294  #température initiale en K
#U1=304  #température à la limite T1
#U2=314  #température à la limite T2

#Lx=200  #longueur de la plaque selon x (en cm)
#Ly=100  #longueur de la plaque selon y (en cm)
#Px=30   #nombre de points du maillage selon x
#Py=30   #nombre de points du maillage selon y


#saisie de la limite de la somme, n tend vers l'infini initalement
def saisie_n():
    n = input("saisir le paramètre n (grand) : ")
    print("valeur choisie: ", n)
    return int(n)

#profil de température selon la solution analytique

def solution_analytique(U1,U2,Lx,Ly,Px,Py):
    n = saisie_n()
    
    Dx=Lx/(Px)
    Dy=Ly/(Py)
    Temp_i=np.zeros((Py,Px))
        
    #remplissage de la matrice avec la solution analytique
    for j in range(0,Py):
        for i in range(0,Px):
            somme = 0
            for k in range(0,n):
                try:
                    somme += (1/(2*k+1))*sin(((2*k+1)*pi*Dx*i)/Lx)*((exp(-Dy*j*(2*k+1)*pi/Lx)-exp((-2*Ly+Dy*j)*(2*k+1)*pi/Lx))/(1-exp(-2*Ly*(2*k+1)*pi/Lx)))
                except OverflowError:
                    somme = float('inf')
            Temp_i[j,i]=U2+((4*(U1-U2))/pi)*somme
            print(" y=",j,"x=",i, "tab= ",Temp_i[j,i])
            
    #on fait pour les points (0,0) et (Lx,0) une moyenne entre les points adjacents pour assurer
    #la continuité de la température aux bords
    Temp_i[0,0]=(Temp_i[0,1]+Temp_i[1,0])/2
    Temp_i[0,Px-1]=(Temp_i[0,Px-2]+Temp_i[1,Px-1])/2
    return Temp_i


#affichage du profil de température

#def affichage_profil_solana(U0,U1,U2,Lx,Ly,Px,Py):
#    Temp_i = solution_analytique(U1,U2,Lx,Ly,Px,Py)
#    mini=np.min([U0,U1,U2])
#    maxi=np.max([U0,U1,U2])
#    with open("solana.txt", "w") as filout:
#        filout.write("{}\n".format(Temp_i))
#        plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi) 
#        plt.show() 
#    return Temp_i
    
#test
#affichage_profil(U1,U2,Lx,Ly,Px,Py)


