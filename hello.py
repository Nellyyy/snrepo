#math permet d'accéder aux fontions sin et sinh
from math import *
import numpy as np

#définitions des différents paramètres

U0=294  #température initiale en K
U1=304  #température à la limite T1
U2=314  #température à la limite T2

Lx=0.2  #longueur de la plaque selon x (en m)
Ly=0.1  #longueur de la plaque selon y (en m)
Px=5    #nombre de points du maillage selon x
Py=6    #nombre de points du maillage selon y

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
    Temp_i=np.ones((Px,Py))
    for i in range(1,Px):
        for j in range(1,Py):
            for k in range(0,n):
                somme += (1/(2*n+1))*sin(((2*n+1)*pi*i)/Lx)*(sinh((Ly-j)*(2*n*+1)*pi/Lx))/(sinh(((2*n*+1)*pi*Ly)/Lx))
            Temp_i[i,j]=U2+((4*(U1-U2))/pi)*somme
            print("i=",i," j=",j, "tabb= ",Temp_i[i,j])
    return Temp_i

solution_analytique(U1,U2,Lx,Ly,Px,Py)

