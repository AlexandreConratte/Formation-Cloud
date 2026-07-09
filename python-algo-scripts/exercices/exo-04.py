import statistics

notes = []
action = -1

while action != 0 : 
    print ("=== PROGRAMME NOTES ===" +
    " 1. Entrer une nouvelle note" +
    " 2. Consulter l'ensemble des notes" +
    " 3. Connaître la plus petite note" + 
    " 4. Connaître la plus grande note" +
    " 5. Connaître la moyenne des notes" +
    " 0. Quitter") 

    action = int(input("Quelle action souhaitez-vous faire : "))
    
    
    if action == 1 :
        note=int(input("Note à ajouter : "))
        notes.append(note)   
    elif action == 2 : 
        print("L'ensemble des notes sont :", notes)   
    elif action == 3 : 
        note_mini = min(notes) 
        print( "La note la plus basse est :",  note_mini)
    elif action == 4 : 
        note_maxi = max(notes)
        print("La note la plus élevée est :",  note_maxi)
    elif action == 5 : 
        moyenne = statistics.mean(notes)
        print("La moyenne de classe est :",  moyenne)
    elif action == 0 : 
        print("Vous quittez notre menu")
print("Adios Amigos")     