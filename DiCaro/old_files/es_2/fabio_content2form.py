from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import Counter
from nltk.wsd import lesk

def word_sense_disambiguation(list_words, word):
    right_synset = lesk(list_words, word)
    return right_synset

def remove_stop_words(row):
    stop_words = set(stopwords.words('english'))
    #punctuation = [',', '.', ';', '!', '?', "'", "''", '"', "’", "’’", "`","``"]
    filtered_sentence = [w for w in row if not w.lower() in stop_words and w not in punctuation]
    return filtered_sentence

def calculate_frequency(row):
    freq_dict = {}
    row = remove_stop_words(word_tokenize(row))
    for word in row[1:]:
        if word.lower() not in freq_dict:
            freq_dict[word.lower()] = 1
        else:
            freq_dict[word.lower()] += 1
    return freq_dict


with open ('def.csv', 'r') as f:
    for row in f:
        dict = calculate_frequency(row)
        k = Counter(dict)
        most_freq = k.most_common(3)
        
        for word in most_freq:
            print(f"- Word: {word} \n{wn.synsets(word[0])}")
        

#! Dobbiamo scegliere il synset per ognuna delle parole più frequenti.
#! Per ogni synset prendiamo tutti i figli e se ci sono sovrapposizioni, 
#! quelle possono essere i synset del concetto che vogliamo descrivere (Person, Brick, ...)
        print(f"Le parole più utilizzate sono: {most_freq}\n\n")
        