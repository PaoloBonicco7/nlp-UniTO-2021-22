import math
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pprint import pprint

from FrameContexts import FrameContexts # custom class we made to better utilize context sets

L = 3
MODE = 'graphic'
LEMMATIZER = WordNetLemmatizer()
DELETE_PUNCTUATION_TOKENIZER = RegexpTokenizer(r'\w+')

# TO-DO LIST:
# [] termini composti
# [] LU che sono stop words
def flatten(l):
    return [item for sublist in l for item in sublist]

def preprocess_word(word):
        word = word.lower()
        if not word in stopwords.words():
                no_punct_word = DELETE_PUNCTUATION_TOKENIZER.tokenize(word)
                if len(no_punct_word) > 0:
                    return LEMMATIZER.lemmatize(no_punct_word[0])

def find_max_sim_synset(term, fn_contexts):
    maxSim = 0
    maxSyns = {}
    # prendo i synset relativi a un termine
    synsets_of_term = list(wn.synsets(term))
    
    for syns in synsets_of_term:
        # costruisco il contesto di un synset
        syns_context = build_syns_context(syns)

        # calcolo sim(f,s)
        sim = similarity(term, fn_contexts, syns, syns_context) 
        # prendo l'argmax su s di tutti i sim(f,s)
        if (sim > maxSim):
            maxSim = sim
            maxSyns = syns
    return [maxSyns, maxSim]

def build_syns_context(syns):
    context = set()
    for word in syns.definition().split():
        prep_word = preprocess_word(word)
        if prep_word is not None:
            context.add(prep_word) 
    for word in syns.lemmas():
        prep_word = preprocess_word(word.name())
        if prep_word is not None:
            context.add(prep_word)
    context.add(syns.name())
    return context

def similarity(term, ctxf, syns, ctxs):
    sim = 0
    if (MODE == 'bag_of_words'):
        my_list = list(ctxs & ctxf.get_frame_context())
        sim = len(my_list) + 1
    elif (MODE == 'graphic'):
        sim = _graphic_similarity(term, ctxf, syns)
    #print("Normalized score: {}".format(sim))   
    return sim

def _graphic_similarity(term, ctxf, syns):
    score = compute_score(ctxf.get_frame_context(),syns)
    #print("Score: {}".format(score))
    return normalize_score(score, term, ctxf)

def compute_score(ctxf, s):
    score = 0
    for t in ctxf:
        synsets = wn.synsets(t)
        for s_prime in synsets:
            length = syn_distance(s, s_prime)
            if length is None or length > L:
                continue
            score += math.e**(-length+1)
    return score

def normalize_score(score, term, ctxf):
    normalization = 0
    for t in ctxf.get_term_contexts().keys():
        synsets = wn.synsets(term)
        for s_prime in synsets:
            normalization += compute_score(ctxf.get_term_context(t), s_prime)
    return score/normalization

def syn_distance(synset1, synset2):
    '''
    Args:
        synset1: first synset to calculate distance
        synset2: second synset to calculate
    Returns:
        distance between the two synset
    '''
    lcs = lowest_common_subsumer(synset1, synset2)
    if lcs is None:
        return None

    hypernym1 = synset1.hypernym_paths()
    hypernym2 = synset2.hypernym_paths()

    # paths from LCS to root
    hypernym_lcs = lcs.hypernym_paths()

    # create a set of unique items flattening the nested list
    #print(hypernym_lcs)
    set_lcs = set(flatten(hypernym_lcs))
    #print(set_lcs)

    # remove root
    set_lcs.remove(lcs)

    # path from synset to LCS
    hypernym1 = list(map(lambda x: [y for y in x if y not in set_lcs], hypernym1))
    hypernym2 = list(map(lambda x: [y for y in x if y not in set_lcs], hypernym2))

    # path containing LCS
    hypernym1 = list(filter(lambda x: lcs in x, hypernym1))
    hypernym2 = list(filter(lambda x: lcs in x, hypernym2))

    return min(list(map(lambda x: len(x), hypernym1))) + min(list(map(lambda x: len(x), hypernym2))) - 2


def lowest_common_subsumer(synset1, synset2): #? My function that simulate the WordNet function
    '''
    Args:
        synset1: first synset to take LCS from
        synset2: second synset to take LCS from
    Returns:
        the first common LCS
    '''
    if synset2 == synset1:
        return synset2

    commonsArr = []
    for hyper1 in synset1.hypernym_paths():
        for hyper2 in synset2.hypernym_paths():
            zipped = list(zip(hyper1, hyper2))  # merges 2 list in one list of tuples
            common = None
            for i in range(len(zipped)):
                if(zipped[i][0] != zipped[i][1]):
                    break
                common = (zipped[i][0], i)

            if common is not None and common not in commonsArr:
                commonsArr.append(common)

    if len(commonsArr) <= 0:
        return None

    commonsArr.sort(key=lambda x: x[1], reverse=True)
    return commonsArr[0][0]

frameSet = [{'id': 2664, 'name': 'Inhibit_motion_scenario'},
            {'id': 1460, 'name': 'Prominence'},
            {'id': 1933, 'name': 'Have_associated'},
            {'id': 370, 'name': 'Morality_evaluation'},
            {'id': 1771, 'name': 'Thriving'}]
frames_number = [1]

not_found_in_wn = []
similarities = []
for i in frames_number:
    frame = fn.frame( frameSet[i]['id'] )
    frame_name = frame.name
    contexts = FrameContexts(frame)
    #pprint(contexts.get_term_contexts())
    for term in contexts.get_frame_context():
        
        maxSyns, maxSim = find_max_sim_synset(term, contexts)
        
        if isinstance(maxSyns, dict) and len(maxSyns) == 0: 
            not_found_in_wn.append(term)
            continue

        # Memorizzazione dei risultati ottimi
        similarities.append([term, maxSyns, maxSim])
        print(term, maxSyns, maxSim)

        
print("Results are: ")
#pprint(similarities)
print("Numero di termini: {}".format(len(similarities)))
print("Termini non trovati in WN: {}".format(len(not_found_in_wn)))

