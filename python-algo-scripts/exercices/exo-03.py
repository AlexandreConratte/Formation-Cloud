import random 


# number_to_guess = str()
# number_to_guess = int(input("Player 1 : Entrez un nombre entre 0 et 100 : "))
# if number_to_guess < 0 or number_to_guess > 100:
#     print("Le nombre doit être compris entre 0 et 100")
#     number_to_guess = int(input("Player 1 : Entrez un nombre entre 0 et 100 : "))

min_value = 0
max_value = 100
number_to_guess = random.randint(min_value, max_value)

number_to_entered = input("Player 2 : Entrez un nombre entre " + str(min_value) + " et " + str(max_value) + " : ")

if type(number_to_entered) != int:
    print("Le nombre doit être un entier")
    number_to_entered = int(input("Player 2 : Entrez un nombre entre " + str(min_value) + " et " + str(max_value) + " : "))

# while number_to_entered != number_to_guess:
#     if number_to_entered > number_to_guess: 
#         print("Trop haut") 
#         max_value = number_to_entered
#         number_to_entered = input("Player 2 : Entrez à nouveau un nombre entre " + str(min_value) + " et " + str(max_value) + " : ")
#         if type(number_to_entered) != int:
#             print("Le nombre doit être un entier")
#             number_to_entered = int(input("Player 2 : Entrez un nombre entre " + str(min_value) + " et " + str(max_value) + " : "))
#     elif number_to_entered < number_to_guess:
#         print("Trop bas") 
#         min_value = number_to_entered
#         number_to_entered = input("Player 2 : Entrez à nouveau un nombre entre " + str(min_value) + " et " + str(max_value) + " : ")
#         if type(number_to_entered) != int:
#             print("Le nombre doit être un entier")
#             number_to_entered = int(input("Player 2 : Entrez un nombre entre " + str(min_value) + " et " + str(max_value) + " : "))

while number_to_entered != number_to_guess:
     if number_to_entered > number_to_guess: 
         print("Trop haut") 
         max_value = number_to_entered
         
     elif number_to_entered < number_to_guess:
         print("Trop bas") 
         min_value = number_to_entered
         
         while True:
             number_to_entered = int(input("Player 2 : Entrez à nouveau un nombre entre " + str(min_value) + " et " + str(max_value) + " : "))
             if type(number_to_entered) == int:
                 break
             else:
                 print("Le nombre doit être un entier")
                 continue

    

print("Félicitations")


