import random

vie =int(input("Combien de vie souhaitez-vous : ") )
gobelets = [1,2,3,4,5]

emplacement_balle = random.choice(gobelets)


while vie > 0 : 
    choix = int(input("Choisis un gobelet numéroté de 1 à 5 : "))

    if choix == emplacement_balle : 
        print("Bravo tu as gagné")
        break
    else :
        vie  -= 1
        if vie == 0:
            print ("Perdu ! Tu n'as plus de vies")
            break
        select = input(f"Perdu, il te reste {vie} vie ,  try again ? (y/n) ")
        if select.lower() == "y" : 
            emplacement_balle = random.choice(gobelets)
        else :
            print ("Dommage!")
            break
          
       

       


  


