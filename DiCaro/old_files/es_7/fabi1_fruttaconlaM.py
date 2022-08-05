import string
import random
import sys
from nltk.corpus import wordnet as wn


help_dict = {"fruit": ["apple", "cranberry"], 
             "animal": ["horse", "shark"]}

#* Controllo se i nostri esempi di aiuto (help_dict[category]) appartengono agli iponomi del 
#* synset passato come parametro, se è così restituisco gli iponimi
def check_hypo(synset, category):
    for example in help_dict[category]:
        if wn.synsets(example)[0] in synset.hyponyms():
            return synset.hyponyms()
            
    return []

#* Data una lista di liste di synset, restituisco tutti quelli che iniziano con la lettera passata per parametro
def pick_hypo(synset, letter):
    result = []
    for list in synset:
        for element in list:
            name = element.lemma_names('eng')[0]
            if name[0].upper() == letter:
                result.append(name)
    return result

#* Cerco l'elemento da restituire e stampo il risultato
def find_element(asking_cat, asking_letter):
    category_synset = wn.synsets(asking_cat)[0]
    system_answer, results = [], []
    for hypo in category_synset.hyponyms():
        part_result = check_hypo(hypo, asking_cat)
        if part_result != []:
            results.append(check_hypo(hypo, asking_cat))
        
    if results != []:
        system_answer = pick_hypo(results, asking_letter)
    
    if system_answer != []:
        print(f"The {asking_cat} that starts with letter {asking_letter} is: {system_answer}")
    else:
        print(f"There is no {asking_cat} that starts with letter {asking_letter}")

CAT = ["fruit"]

asking_cat = random.choice(CAT)
asking_letter = random.choice(string.ascii_uppercase)
find_element(asking_cat, asking_letter)





'''
answer = input(f"Hello! Pick a {asking_cat} that starts with letter {asking_letter}: ")
answer = answer.replace(" ", "_")
print(wn.synsets("fruit")[0].closure(lambda s:s.hyponyms))

if wn.synsets(answer) != []:
    full_hypo = set([i for i in wn.synsets(asking_cat)[0].closure(lambda s:s.hyponyms())])
    
    if wn.synsets(answer)[0] in full_hypo:
        print("Good Answer")
    else:
        print("That is not a right answer")
else:
    print("What?")'''