# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:51:07 2020

@author: camil
"""

#projet sciences numériques

import numpy as np

#définitions des différents paramètres
#(pourra être demandé à l'utilisateur plus tard)

Lx=0.2  #longueur de la plaque selon x (en m)
Ly=0.1  #longueur de la plaque selon y (en m)
Px=5    #nombre de points du maillage selon x
Py=6    #nombre de points du maillage selon y
a=98*(10**-6) #diffusivité thermique pour une plaque en silicium

Ttot=10 #temps total de l'expérience en seconde
Pt=100  #maillage temporel 

U0=294  #température initiale en K
U1=304  #température à la limite T1
U2=314  #température à la limite T2

############################################################################

#conditions aux limites
Cote0=np.ones((1,Py))*U2  #profil de température sur le côté tel que x=0
CoteLx=np.ones((1,Py))*U2 #profil de température sur le côté tel que x=Lx

#Profil de température à t=0
#on crée un tableau pour les températures intérieures, ie sans prendre en compte
#les côtés x=0 et x=Lx, calculés ci-dessus, qui seront ensuite rajoutés

Temp_inte_0=np.ones((Px-2,Py))*U0
for k in range(Px-2):
    Temp_inte_0[k,0]=U1     #conditions aux limites en y=0
    Temp_inte_0[k,Py-1]=U2  #conditions aux limites en y=Ly

#on combine Temp_inte_0 aux conditions aux limites x=0 et x=Lx
Temp_0=np.vstack((Cote0,Temp_inte_0,CoteLx))

#on fait pour les points (0,0) et (Lx,0) une moyenne entre U2 et U1 pour <<modéliser>>
#la continuité de la température aux bords
Temp_0[0,0]=Temp_0[Px-1,0]=(U1+U2)/2

############################################################################

#schémas aux différences finies
#déterminer le profil de température à l'instant i+1 en fonction de celui au temps i

Dt=Ttot/Pt
Dx=Lx/Px
Dy=Ly/Py

A=a*Dt/Dx**2
B=a*Dt/Dy**2

def differences_finies(Temp_i): #argument : profil de température au temps i
    #on note Temp_j la température au temps i+1
    #conditions aux limites de Temp_j avant de faire les calculs intérieurs
    Temp_j=np.vstack((Cote0,np.zeros((Px-2,Py)),CoteLx))
    Temp_j[0,0]=Temp_j[Px-1,0]=(U1+U2)/2
    
    for k in range(1, Px-1):
        Temp_j[k,0]=U1     #conditions aux limites en y=0
        Temp_j[k,Py-1]=U2  #conditions aux limites en y=Ly
        for h in range(1, Py-1):
            Temp_j[k,h]=(1-2*(A+B))*Temp_i[k,h]+A*(Temp_i[k+1,h]+Temp_i[k-1,h])+B*(Temp_i[k,h+1]+Temp_i[k,h-1]) 
   
    return Temp_j
    
#print(differences_finies(Temp_0))

############################################################################