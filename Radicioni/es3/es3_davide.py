import nltk
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.corpus.reader.framenet import PrettyList, PrettyDict

# TO-DO LIST:
# [] inserire in frameSet gli altri frame
# [] finire set di contesto LU
# [] preprocessing su WordNet
# [] 

def print_sep():
    print('------------------------------------------------------------------------')

def preprocess_word(word):
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
        tmp = {fe.name: context}
        fn_fe_context.append(tmp)
    return fn_fe_context

def build_name_context(frame):
    context = []
    for word in frame.definition.split():
        prep_word = preprocess_word(word)
        if prep_word is not None:
            context.append(prep_word) 
    return {frame.name: context}

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
        tmp = {lu.name[:p]: context}
        fn_lu_context.append(tmp)
    return fn_lu_context




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
    #fn_name_context = build_name_context(frame)
    #fn_fe_context = build_fes_context(frame)
    #fn_lu_context = build_lu_context(frame)
    frameTerms.append(build_fes_context(frame))
    #frameTerms.append(...build_name_context(frame))
    #frameTerms.append(...build_lu_context(frame))

    
