import random
 
MOTS = ["hunter",
"fatezero",
"fullmetal",
"bleach",
"parasyte",
"",
"",
"",
"",]

def select_world() : 
    """Selectionne un mot."""
    return random.choice(MOTS)

def creation_affichage 