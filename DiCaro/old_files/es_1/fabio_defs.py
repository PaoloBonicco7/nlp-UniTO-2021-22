from collections import Counter
from nltk.stem import WordNetLemmatizer

STOP_WORDS = ['on','of','a', 'most', 'be', 'did', "mightn't", 'or', 'the', 'does', "it's", 'ourselves', 'if', 'few', 'above', 've', 'ours', 
'your', 'some', 'own', 't', 'yours', 'couldn', "you'll", 'both', "wouldn't", 'once', 'off', 'doesn', 'through', 'their', 
'themselves', 'until', 'isn', 'do', "hadn't", 'have', 'from', 'needn', 'hers', 'has', 'between', 'not', 'ain', 'they', 'after', 'out', 
'then', 'while', "shouldn't", 'mightn', 'against', "should've", "couldn't", 'she', 'but', 'as', 'below', 'over', 'each', 'hadn', 'when', 
'of', 'there', 'hasn', 'before', 'aren', 'only', 'them', 'is', 'will', 'yourself', 'so', 're', 'very', "you'd", 'all', 'nor', 'o', 'haven', 
'had', 'that', 'doing', 'just', 'no', 'and', "needn't", 'was', "didn't", 'a', 'weren', 'why', 'an', "mustn't", "isn't", 'wouldn', 'whom', 
'too', "that'll", 'should', 'himself', 'about', 'which', 'under', "don't", 'y', "hasn't", 'been', 'his', 'here', 'further', "doesn't", 
'same', 'how', 'we', 'than', 'ma', 'who', 'herself', 'theirs', 'were', 'any', 'wasn', "haven't", 'having', 'it', 'yourselves', 'more', 
'won', 'those', 'by', 'now', 'd', 'where', 'me', 'him', 'again', 's', 'are', 'shouldn', "weren't", "wasn't", 'for', 'what', "she's", 'll', 
"won't", 'this', 'because', 'm', 'you', 'shan', 'up', 'can', 'her', 'itself', 'i', "you're", 'in', 'myself', 'its', 'mustn', 'don', 'these', 
'such', 'down', 'our', 'into', "shan't", 'didn', 'am', 'he', 'to', 'my', "aren't", 'other', "you've", 'at', 'during', 'with', 'someone']

def remove_stop_words(text):
    result = []
    for word in text:
        if word.lower() not in STOP_WORDS:
            result.append(word.lower())
    return result

def lemmatize_words(text):
    result = []
    lemmatizer = WordNetLemmatizer()
    for word in text:
        result.append(lemmatizer.lemmatize(word))
    return result

list = open("def.csv").readlines()
data = []
for l in list:
    data.append(l.strip("\n").split(","))

for l in data:
    main_concept = l[0]
    counter_concept = Counter()
    for definition in l[1:]:
        statement = remove_stop_words(definition.split())
        statement = lemmatize_words(statement)
        counter_concept.update(statement)

    first,second,third = counter_concept.most_common(3)

    #print(f"Parole più frequenti per {main_concept}: {counter_concept.most_common(3)}")

    results = {first[0]:0, second[0]:0, third[0]:0}
    n_statement = 0

    for definition in l[1:]:
        if first[0] in definition.split():
            results[first[0]] += 1
        if second[0] in definition.split():
            results[second[0]] += 1
        if third[0] in definition.split():
            results[third[0]] += 1
        n_statement += 1
    
  
    #* EVALUATION
    mean = 0.0
    for element in results.keys():
        mean += results[element]/n_statement
    print(f"Punteggio finale per {main_concept}: {round(mean/3, 2)}")

