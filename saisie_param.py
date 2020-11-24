#saisie des différents paramètres


#saisie de la longueur de la plaque selon x en mètres
def saisie_Lx():
	Lx = input("Choisissez la longueur de la plaque selon x : ")
	return Lx

#saisie de la largeur de la plaque selon y en mètres
def saisie_Ly():
	Lx = input("Choisissez la largeur de la plaque selon y : ")
	return Ly

#saisie du nombre de points du maillage selon x
def saisie_Px():
	Px = input("Choisissez le nb de points du maillage selon x : ")
	return Px

#saisie du nombre de points du maillage selon y
def saisie_Py():
	Py = input("Choisissez le nb de points du maillage selon y : ")
	return Py

#saisie de la diffusivité thermique selon le matériau
def saisie_a():
	a = input("Diffusivité du matériau choisi : ")
	return a

#saisie du temps total de l'expérience en seconde
def saisie_Ttot():
	Ttot = input("Temps total de l'expérience : ")
	return Ttot

#saisie du maillage temporel 
def saisie_Pt():
	Pt = input("Choisissez le maillage temporel : ")
	return Pt

#saisie des températures
#température initiale en K
def saisie_U0():
	U0 = input("température initiale (K): ")
	return U0
#température à la limite T1
def saisie_U1():
	U1 = input("température à la limite T1 (y=0) : ")
	return U1
#température à la limite T2
def saisie_U2():
	U2 = input("température à la limite T2 (les trois autres faces): ")
	return U2

#appel des ss-programmes en fonction des besoins
print(saisie_U2())
