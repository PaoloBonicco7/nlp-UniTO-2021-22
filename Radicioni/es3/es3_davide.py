import nltk
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus.reader.framenet import PrettyList, PrettyDict

# TO-DO LIST:
# [] costruzione contesto dei synset
# [] 

def print_sep():
    print('------------------------------------------------------------------------')

def preprocess_word(word):
    word = word.lower()
    if not word in stopwords.words():
            no_punct_word = delete_punctuation_tokenizer.tokenize(word)
            if len(no_punct_word) > 0:
                return lemmatizer.lemmatize(no_punct_word[0])

def build_fes_context(frame):
    '''
    Build a context set for every Frame Entity in the given frame. 
    Returns an array of n objects of the form
        {fe_name : fe_context}
    where 
    - n is the number of frame entities in the given frame, 
    - fe_name is the name of a frame entity,
    - fe_context is the context set of that frame entity
    '''
    fn_fe_context = []
    for fe_key in frame.FE.keys():
        fe = frame.FE[fe_key]
        context = []
        for word in fe['definition'].split():
            prep_word = preprocess_word(word)
            if prep_word is not None:
                context.append(prep_word)
        name = preprocess_word(fe.name)
        fn_fe_context.append({name: context})
    return fn_fe_context

def build_name_context(frame):
    context = []
    for word in frame.definition.split():
        prep_word = preprocess_word(word)
        if prep_word is not None:
            context.append(prep_word) 
    name = preprocess_word(frame.name)
    return [{name: context}]

def build_lu_context(frame):
    fn_lu_context = []
    for lu_key in frame.lexUnit.keys():
        lu = frame.lexUnit[lu_key]
        context = []
        for word in lu['definition'].split():
            prep_word = preprocess_word(word)
            if prep_word is not None and prep_word != "COD":
                context.append(prep_word)
        p = lu.name.find('.')
        name = preprocess_word(lu.name[:p])
        fn_lu_context.append({name: context})
    return fn_lu_context

def build_syns_context(syns):
    context = []
    for word in syns.definition().split():
        prep_word = preprocess_word(word)
        if prep_word is not None:
            context.append(prep_word) 
    for word in syns.lemmas():
        prep_word = preprocess_word(word.name())
        if prep_word is not None:
            context.append(prep_word)
    name = syns.name()
    return {name: context}


def similarity(ctxf, ctxs, mode='bag_of_words'):
    sim = 0
    if(mode == 'bag_of_words'):
        #print(set(ctxs))
        #print(set(ctxf))
        my_list = list(set(ctxs) & set(ctxf))
        sim = len(my_list) + 1
    return sim

frameSet = [{'id': 2664, 'name': 'Inhibit_motion_scenario'},
            {'id': 1460, 'name': 'Prominence'},
            {'id': 1933, 'name': 'Have_associated'},
            {'id': 370, 'name': 'Morality_evaluation'},
            {'id': 1771, 'name': 'Thriving'}]
lemmatizer = WordNetLemmatizer()
delete_punctuation_tokenizer = RegexpTokenizer(r'\w+')
frames_number = [1]

frameTerms = [] # lista di dizionari {nome: contesto}

for i in frames_number:
    frame = fn.frame( frameSet[i]['id'] )
    frameTerms.extend(build_name_context(frame))
    frameTerms.extend(build_fes_context(frame))
    frameTerms.extend(build_lu_context(frame))

similarities = []
for termDict in frameTerms:
    # prendo i synset relativi a un termine
    for term in termDict.keys():
        print("Term is:\n " + term)
        print("Context of term is: ")
        print(termDict[term])
        maxSim = 0
        maxSyns = {}
        synsets_of_term = list(wn.synsets(term))
        #print("Synsets:")
        #print([x.name() for x in synsets_of_term])
        for syns in synsets_of_term:
            # costruisco il contesto di un synset
            synsets_context = build_syns_context(syns)

            # calcolo sim(f,s) con Bag of words
            sim = similarity(termDict[term], synsets_context[syns.name()]) 
            if (sim > maxSim):
                maxSim = sim
                maxSyns = syns
                maxContext = synsets_context[syns.name()]
        print("Results are: ")
        print(maxSim, maxContext)
        similarities.append((term,syns,sim))
        # FINE FOR

# prendo l'argmax su s di tutti i sim(f,s) finora calcolati.