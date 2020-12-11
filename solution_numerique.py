# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 14:51:07 2020

@author: camil
"""

#projet sciences numériques

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm 
import sys


############################################################################

#Vérification de la stabilité du schéma numérique
#A PROUVER : ce schéma est stable ssi a*Dt/Dx**2 + a*Dt/Dy**2 <= 1/2

def stabilite_schema(a,Lx,Ly,Px,Py,Ttot,Pt):
    Dt=Ttot/Pt
    Dx=Lx/Px
    Dy=Ly/Py
    
    Fx=a*Dt/Dx**2
    Fy=a*Dt/Dy**2

    if (Fy+Fx)>=1/2:
        print("(Fy+Fx)>1/2, le schéma n'est pas cohérent : diminuer le delta t ou augmenter delta y ou delta x")
        return 0
    else:
        return 1


############################################################################

#conditions aux limites
def condition_limite_x(Px,U1,U2):
    Cote_0=np.ones((1,Px))*U1  #profil sur les côtés y=O
    Cote_Ly=np.ones((1,Px))*U2  #profil sur les côtés y=Ly
    return Cote_0,Cote_Ly

#Profil de température à t=0
#on créé un tableau pour les températures intérieures, ie sans prendre en compte
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


############################################################################

#schémas aux différences finies
#déterminer le profil de température à l'instant i+1 en fonction de celui au temps i

def differences_finies(Temp_i,Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt): #Temp_i : profil de température au temps i
    Dt=Ttot/Pt
    Dx=Lx/Px
    Dy=Ly/Py
    
    Fx=a*Dt/Dx**2
    Fy=a*Dt/Dy**2

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
            Temp_j[k,h]=(1-2*(Fx+Fy))*Temp_i[k,h]+Fy*(Temp_i[k+1,h]+Temp_i[k-1,h])+Fx*(Temp_i[k,h+1]+Temp_i[k,h-1]) 

    return Temp_j


############################################################################

#obtention du maillage de température à chaque instant
#les différents maillages sont conservés dans un fichier txt nommé maillage_temp

#on demande en entrée une grande epsilon : si max(T(t+1)[k,h]-T(t)[k,h]) est inférieure à epsilon
#on considère avoir atteint le régime permanent, et on arrête la fonction


def profil_temperature(Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt,epsilon):
    #on vérifie que les paramètres entrés sont conformes à la condition de stabilité
    if stabilite_schema(a,Lx,Ly,Px,Py,Ttot,Pt)==1:
        Temp_i=temperature_initiale(Px,Py,U0,U1,U2)
        temps_regime_permanent=0
        
        with open("temperature.txt", "w") as filout:
            filout.write("{}\n".format(Temp_i))

            print("Solution numérique : calcul en cours...")
            
            #on calcule pour chaque temps t le maillage, en utilisant la méthode des différences finies
            for t in range(Pt):
                Temp_j=differences_finies(Temp_i,Lx,Ly,Px,Py,a,U0,U1,U2,Ttot,Pt)
                
                #calcul de T(t+1)[k,h]-T(t)[k,h] : si c'est inférieur à epsilon, on arrête le programme
                difference=np.max(abs(Temp_i-Temp_j))
                temps_regime_permanent+=Ttot/Pt
                
                Temp_i=Temp_j
                filout.write("{}\n".format(Temp_i))
                
                if difference<=epsilon:
                    return "le programme a atteint le régime permanent. Le temps caractéristique est t=",temps_regime_permanent," et la température finale est ",Temp_i
                              
        return "le programme n'a pas atteint le régime permanent après t=",temps_regime_permanent,"et la température finale atteinte est", Temp_i         
       
    else:
        print("schéma non cohérent")
        sys.exit()
        
