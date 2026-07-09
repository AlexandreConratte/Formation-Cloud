import random

vie =int(input("Combien de vie souhaitez-vous :") )
gobelets = [1,2,3,4,5]

emplacement_balle = random.sample(gobelets,1)

while vie > 0 : 
    choix = int(input("Choisis un gobelet numéroté de 1 à 5 : "))

    if choix == emplacement_balle : 
        print("Bravo tu as gagné")
    else :
        select = input(f"Perdu; try again ? (y/n) ")
        if select.lower() == "y" : 
            emplacement_balle = random.sample(gobelets,1)
            vie = vie-1
       

       


  


