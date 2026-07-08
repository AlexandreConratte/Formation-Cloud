
number_to_guess = str()
number_to_guess = int(input("Player 1 : Entrez un nombre entre 0 et 100 : "))
if number_to_guess < 0 or number_to_guess > 100:
    print("Le nombre doit être compris entre 0 et 100")
    number_to_guess = int(input("Player 1 : Entrez un nombre entre 0 et 100 : "))

number_to_entered = int(input("Player 2 : Entrez un nombre entre 0 et 100 : "))

while number_to_entered != number_to_guess:
    if number_to_entered > number_to_guess: 
        print("Trop haut") 
        number_to_entered = int(input("Player 2 : Entrez un nombre entre 0 et 100 : "))
    elif number_to_entered < number_to_guess:
        print("Trop bas") 
        number_to_entered = int(input("Player 2 : Entrez un nombre entre 0 et 100 : "))
    else : 
        print("Félicitations")


