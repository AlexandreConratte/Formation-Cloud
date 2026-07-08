produits = ["coca", "fanta", "sprite", "orangina", "ice tea", "pomme", "poire"]
price = [1.5, 1.4, 2.0, 1.6, 1.7, 0.3, 0.5]
somme_totale = 20
list_courses = []

for i in range(len(produits)):
    print(f"{produits[i]} : {price[i]}€")

#for i in range(len(produits)):
 #   select = input(f"Voulez-vous acheter le produit suivant :{produits[i]} ? (oui/non) ")
  #  if select.lower() == "oui":
   #    somme_totale -= price[i]
    #   print(somme_totale)

for i in range(len(produits)):
    select = input(f"Voulez-vous acheter le produit suivant :{produits[i]} ? (oui/non) ")
    if select.lower() == "oui":
     somme_totale -= price[i] 
     list_courses.append(produits[i])
    print(somme_totale)

somme_dépensée = 20 - somme_totale

select = input("Voulez-vous bien acheter les produits suivants : " + str(list_courses) + " pour " + str(somme_dépensée) + "€ ? (oui/non) ")
 
if select.lower() == "oui":
    print(f"Vous avez acheté {', '.join(list_courses)} pour {somme_dépensée}€ et il vous reste {somme_totale}€")
else:
    print("Vous n'avez rien acheté !")


 



