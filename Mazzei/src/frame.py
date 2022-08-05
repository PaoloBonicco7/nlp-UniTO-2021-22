import random
from matcher import *

class Frame:
    
    def __init__(self, path):
        self.potions = {}
        self.student_ingredients = [] # memorizza le risposte corrette (ingredienti) dello studente
        self.student_name = ""
        self.add_potions(path)
        self.potion_name = pick_random(list(self.potions.keys())) # il nome della pozione oggetto dell'interrogazione
        self.mood = random.randint(0,2) # from 0 to 2 (0 = happy, 1 = neutral, 2 = angry)
        self.chances = len(self.potions[self.potion_name]) - self.mood

    def get_initial_chances(self):
        return len(self.potions[self.potion_name]) - self.mood

    def dec_chances(self):
        self.chances -= 1

    def get_potions_length(self):
        return len(self.potions)

    def get_chances(self):
        return self.chances

    def get_ingredients_number(self):
        return len(self.potions[self.potion_name])

    def get_potion_name(self):
        return self.potion_name

    def set_potion_name(self, potion_name):
        self.potion_name = potion_name
    
    def get_student_ingredients(self):
        return self.student_ingredients

    def get_student_name(self):
        return self.student_name

    def set_student_name(self, student_name):
        self.student_name = student_name
        if "potter" in self.student_name.lower():
            self.mood = 3
            self.chances = 1

    def get_mood(self):
        return self.mood

    def set_mood(self, mood):
        self.mood = mood
    
    # aggiungo la lista di pozioni al dizionario del frame leggendole da potions.txt
    def add_potions(self, path):
        file = open(path, "r")
        for line in file:
            p = list(line.strip("\n").split(','))
            p_name = p[0]
            p_ing = p[1:]
            self.potions[p_name] = p_ing
        file.close()
    
    def to_string(self):
        res = ""
        res = f"{res}Pozione scelta per l'interrogazione: {self.potion_name}\n" \
              f"Studente interrogato: {self.student_name}\n"\
              f"Elenco pozioni conosciute:\n"

        for p in self.potions.keys():
            res += f"{p}, ingredienti: {self.potions[p]} \n"
        return res

    # controllo che l'ingrediente sia corretto e se lo è lo aggiungo alle risposte corrette (se non è già stato detto)
    def check_response(self, ingredient):
        res = False
        for el in ingredient:
            for i in self.potions[self.potion_name]:
                if i.lower() == el.lower()  and (i not in self.student_ingredients):
                    self.student_ingredients.append(i)
                    res = True
        return res
        
    def full_frame(self):
        return self.get_ingredients_number() <= len(self.get_student_ingredients())

    def empty_frame(self):
        return True if len(self.student_ingredients) == 0 else False

    def remaining_ingredients(self):
        return self.get_ingredients_number() - len(self.get_student_ingredients())

