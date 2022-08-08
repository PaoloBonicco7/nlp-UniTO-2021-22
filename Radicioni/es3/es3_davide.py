import nltk
import math
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pprint import pprint

# TO-DO LIST:
# [] termini composti
# [] LU che sono stop words

def print_sep():
    print('------------------------------------------------------------------------')

def preprocess_word(word):
    word = word.lower()
    if not word in stopwords.words():
            no_punct_word = delete_punctuation_tokenizer.tokenize(word)
            if len(no_punct_word) > 0:
                return lemmatizer.lemmatize(no_punct_word[0])

def build_name_context(frame):
    context = set()
    for word in frame.definition.split():
        prep_word = preprocess_word(word)
        if prep_word is not None:
            context.add(prep_word) 
    return context

def build_fes_context(frame):
    '''
    Use every Frame Element's definition and name in order 
    to build a context set for the frame itself. 
    Returns a list of lemmatized words with stopwords removal
    that comprised the context set.
    '''
    fn_fe_context = set()
    for fe_key in frame.FE.keys():
        fe = frame.FE[fe_key]
        name = preprocess_word(fe.name)
        context = set([name]) if name is not None else set()
        for word in fe['definition'].split():
            prep_word = preprocess_word(word)
            if prep_word is not None:
                context.add(prep_word)
        fn_fe_context.update(context)
    return fn_fe_context

def build_lu_context(frame):
    fn_lu_context = set()
    for lu_key in frame.lexUnit.keys():
        lu = frame.lexUnit[lu_key]
        p = lu.name.find('.')
        name = preprocess_word(lu.name[:p])
        if name is not None:
            fn_lu_context.add(name)
    return fn_lu_context

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

def similarity(ctxf, ctxs, syns1, mode='bag_of_words'):
    sim = 0
    if (mode == 'bag_of_words'):
        my_list = list(set(ctxs) & set(ctxf))
        sim = len(my_list) + 1
    elif (mode == 'graphic'):
        sim = _graphic_similarity(ctxf, syns1)   
    return sim

def _graphic_similarity(ctxf):
    sim = 0
    max = []
    for term in ctxf:
        synsets = wn.synsets(term)
        for s in synsets:
            score = compute_score(term,s)
            prob = normalize_score(score)
            if (prob > max[0]):
                max = [prob, s]
        
    return sim

def normalize_score(score):
    pass

def compute_score(term, s):
    synsets = wn.synsets(term)
    score = 0
    for s_prime in synsets:
        length = compute_path_length(s, s_prime)
        score += math.e**(-length+1)

def compute_path_length(syns1, syns2):
    pass

def find_max_sim_synset(term, term_context):
    maxSim = 0
    maxSyns = {}
    # prendo i synset relativi a un termine
    synsets_of_term = list(wn.synsets(term))
    
    for syns in synsets_of_term:
        # costruisco il contesto di un synset
        synset_context = build_syns_context(syns)

        # calcolo sim(f,s)
        mode = 'bag_of_words'
        sim = similarity(term_context, synset_context, mode) 
        # prendo l'argmax su s di tutti i sim(f,s)
        if (sim > maxSim):
            maxSim = sim
            maxSyns = syns
    return [maxSyns, maxSim]

frameSet = [{'id': 2664, 'name': 'Inhibit_motion_scenario'},
            {'id': 1460, 'name': 'Prominence'},
            {'id': 1933, 'name': 'Have_associated'},
            {'id': 370, 'name': 'Morality_evaluation'},
            {'id': 1771, 'name': 'Thriving'}]
lemmatizer = WordNetLemmatizer()
delete_punctuation_tokenizer = RegexpTokenizer(r'\w+')
frames_number = range(5)

frameDict = {} # dizionario che avrà {nome_frame1: contesto_frame1, nome_frame2: contesto_frame2, ...}

for i in frames_number:
    frame = fn.frame( frameSet[i]['id'] )
    ctx = build_name_context(frame) # ctx is a set
    ctx.update(build_fes_context(frame))
    ctx.update(build_lu_context(frame))
    frameDict[frame.name] = ctx

not_found_in_wn = []
similarities = []
for frame_name in frameDict.keys():
    for term in frameDict[frame_name]:

        maxSyns, maxSim = find_max_sim_synset(term, frameDict[frame_name])
        
        if isinstance(maxSyns, dict) and len(maxSyns) == 0: 
            not_found_in_wn.append(term)
            continue

        # Memorizzazione dei risultati ottimi
        similarities.append([term, maxSyns, maxSim])

        
print("Results are: ")
#pprint(similarities)
print("Numero di termini: {}".format(len(similarities)))
print("Termini non trovati in WN: {}".format(len(not_found_in_wn)))
