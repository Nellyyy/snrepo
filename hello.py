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



#profil de température selon la solution analytique

def solution_analytique(U1,U2,Lx,Ly,Px,Py,n):
    print("a1")
    Dx=Lx/(Px-1)   #On met Px-1 car pour Px point, il y a Px-1 intervalle
    Dy=Ly/(Py-1)   #idem
    Temp_i=np.zeros((Py,Px))
        
    #remplissage de la matrice avec la solution analytique
    print("calcul en cours")
    for j in range(0,Py):
        for i in range(0,Px):
            somme = 0
            print("a2")
            for k in range(0,n):
                try:
                    somme += (1/(2*k+1))*sin(((2*k+1)*pi*Dx*i)/Lx)*((exp(-Dy*j*(2*k+1)*pi/Lx)-exp((-2*Ly+Dy*j)*(2*k+1)*pi/Lx))/(1-exp(-2*Ly*(2*k+1)*pi/Lx)))
                except OverflowError:
                    somme = float('inf')
            Temp_i[j,i]=U2+((4*(U1-U2))/pi)*somme
            
            #affichage de la température point par point
            #print(" y=",j,"x=",i, "temp = ",Temp_i[j,i])
    print("a3")        
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


