import random

def lancer_de_Dé(n):
    d = random.randint(1,n)
    return d

def lancer_De_Des(nbDes,nbFaces=6):
    listeDesDes = []    
    for i in range(nbDes):
        d = lancer_de_Dé(nbFaces) 
        listeDesDes.append(d)     
    return listeDesDes

def somme_des_Des(nbDes,nbFaces):
    S = 0    #somme des dés, pour l'instant nulle
    for i in range(nbDes):
        d = lancer_de_Dé(nbFaces) #on lance un dé
        S=S+d     #on ajoute ce dé à la somme
    return S


class personnage : 
    race : str
    pv : int
    reduc_dmg : int
    bonus_dmg : int

def __init__(self, race : str,  pv : int, reduc_dmg : int, bonus_dmg : int) : 
    self.race = race
    self.pv = pv 
    self.reduc_dmg = reduc_dmg
    self.bonus_dmg = bonus_dmg

class creature : 
    race : str
    pv : int
    reduc_dmg : int
    bonus_dmg : int

def __init__(self, race : str,  pv : int, reduc_dmg : int, bonus_dmg : int) : 
    self.race = race
    self.pv = pv 
    self.reduc_dmg = reduc_dmg
    self.bonus_dmg = bonus_dmg

joueur = personnage( 
    race = "humain ",
    pv = 30,
    reduc_dmg = 2,
    bonus_dmg = 3,

)

ennemi = creature(
    race = "gobelin",
    pv = 20,
    reduc_dmg = 1,
    bonus_dmg = 1
)


while joueur.pv > 0 and ennemi.pv > 0 : 
    input("\n Appuie sur entrée pour attaquer ...")

    dmg_joueur = somme_des_Des(2,6) + joueur.bonus_dmg - ennemi.reduc_dmg

    print(f"Tu infliges {dmg_joueur} au {ennemi.race}")
    
    ennemi.pv -= dmg_joueur

    print(f"{ennemi.race} pv : {ennemi.pv}")

    if ennemi.pv <= 0 : 
        print(f"Tu as vaincu {ennemi.race}")

