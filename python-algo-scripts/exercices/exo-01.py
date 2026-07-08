from datetime import date    


firstname = "Alexandre"
name = "Conratte"
age = 29 


print ("Bonjour " + firstname + " " + name + ", vous avez " + str(age) + "ans!")

today = date.today()
print(today)   
birthdate = today.year - age
print("Vous êtes né en " + str(birthdate) + " !")
