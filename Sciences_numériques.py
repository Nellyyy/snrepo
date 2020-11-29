# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:51:07 2020

@author: camil
"""

#projet sciences numériques

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 

#définitions des différents paramètres
#(pourra être demandé à l'utilisateur plus tard)

Lx=1  #longueur de la plaque selon x (en m)
Ly=1  #longueur de la plaque selon y (en m)
Px=80    #nombre de points du maillage selon x
Py=100    #nombre de points du maillage selon y
a=98*(10**-6) #diffusivité thermique pour une plaque en silicium

Ttot=1000 #temps total de l'expérience en seconde
Pt=5000  #maillage temporel 

U0=294  #température initiale en K
U1=304  #température à la limite T1
U2=314  #température à la limite T2

############################################################################

#Vérification de la stabilité du schéma numérique
#A PROUVER : ce schéma est stable ssi a*Dt/Dx**2 < 1/2 et a*Dt/Dy**2 < 1/2

def stabilite_schema(a,Lx,Ly,Px,Py,Ttot,Pt):
    Dt=Ttot/Pt
    Dx=Lx/Px
    Dy=Ly/Py
    
    A=a*Dt/Dx**2
    B=a*Dt/Dy**2
    
    if B>=1/2:
        print("B>1/2, le schéma n'est pas cohérent : diminuer le delta t ou augmenter delta x")
        return 0
    elif A>=1/2:
        print("A>1/2, le schéma n'est pas cohérent : diminuer le delta t ou augmenter delta y")
        return 0
    else:
        return 1

#test
#print(stabilite_schema(a,Lx,Ly,Px,Py,Ttot,Pt))

############################################################################

#conditions aux limites
def condition_limite_x(Px,U1,U2):
    Cote_0=np.ones((1,Px))*U1  #profil sur les côtés y=O
    Cote_Ly=np.ones((1,Px))*U2  #profil sur les côtés y=Ly
    return Cote_0,Cote_Ly

#Profil de température à t=0
#on crée un tableau pour les températures intérieures, ie sans prendre en compte
#les côtés x=0 et x=Lx, calculés ci-dessus, qui seront ensuite rajoutés

def temperature_initiale(Px,Py,U0,U1,U2):
    Temp_inte_0=np.ones((Py-2,Px))*U0
    for k in range(Py-2):
        Temp_inte_0[k,0]=U2     #conditions aux limites en x=0
        Temp_inte_0[k,Px-1]=U2  #conditions aux limites en x=Lx
    #on combine Temp_inte_0 aux conditions aux limites y=0 et y=Ly
    Cote_0=condition_limite_x(Px,U1,U2)[0]
    Cote_Ly=condition_limite_x(Px,U1,U2)[1]
    Temp_0=np.vstack((Cote_0,Temp_inte_0,Cote_Ly))
    #on fait pour les points (0,0) et (Lx,0) une moyenne entre U2 et U1 pour <<modéliser>>
    #la continuité de la température aux bords
    Temp_0[0,0]=Temp_0[0,Px-1]=(U1+U2)/2
    return Temp_0

#test
#print(temperature_initiale(Px,Py,U0,U1,U2))

############################################################################

#schémas aux différences finies
#déterminer le profil de température à l'instant i+1 en fonction de celui au temps i

def differences_finies(Temp_i,Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt): #Temp_i : profil de température au temps i
    Dt=Ttot/Pt
    Dx=Lx/Px
    Dy=Ly/Py
    
    A=a*Dt/Dx**2
    B=a*Dt/Dy**2
    
    Cote_0=condition_limite_x(Px,U1,U2)[0]
    Cote_Lx=condition_limite_x(Px,U1,U2)[1]

    #on note Temp_j la température au temps i+1
    #conditions aux limites de Temp_j avant de faire les calculs intérieurs
    Temp_j=np.vstack((Cote_0,np.zeros((Py-2,Px)),Cote_Lx))
    Temp_j[0,0]=Temp_j[0,Px-1]=(U1+U2)/2
    
    for k in range(1, Py-1):
        Temp_j[k,0]=U2     #conditions aux limites en x=0
        Temp_j[k,Px-1]=U2  #conditions aux limites en x=Lx
        for h in range(1, Px-1):
            Temp_j[k,h]=(1-2*(A+B))*Temp_i[k,h]+B*(Temp_i[k+1,h]+Temp_i[k-1,h])+A*(Temp_i[k,h+1]+Temp_i[k,h-1]) 
   
    return Temp_j

#test
#print(differences_finies(temperature_initiale(Px,Py,U0,U1,U2),Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt))

############################################################################

#obtention du maillage de température à chaque instant
#les différents maillages sont conservés dans un fichier txt nommé maillage_temp
#on affiche le maillage de température à la fin de l'expérience par des nuances oranges

def profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt):
    if stabilite_schema(a,Lx,Ly,Px,Py,Ttot,Pt)==1:
        Temp_i=temperature_initiale(Px,Py,U0,U1,U2)
        mini=np.min([U0,U1,U2])
        maxi=np.max([U0,U1,U2])
        with open("temperature.txt", "w") as filout:
            for t in range(Pt):
                filout.write("{}\n".format(Temp_i))
                Temp_i=differences_finies(Temp_i,Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt)
            plt.pcolormesh(Temp_i, cmap=plt.cm.Oranges, vmin=mini, vmax=maxi) 
            plt.show()
            return Temp_i
    else:
        print("schéma non cohérent")
    

#test    
print(profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt))

############################################################################
