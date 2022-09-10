import math
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import spacy
from pprint import pprint
import json
import os
from FrameContexts import FrameContexts # custom class we made to better utilize context sets

L = 3
MODE = 'graphic'
#MODE = 'bag_of_words'
LEMMATIZER = WordNetLemmatizer()
DELETE_PUNCTUATION_TOKENIZER = RegexpTokenizer(r'\w+')

def flatten(l):
    return [item for sublist in l for item in sublist]

def preprocess_word(word):
        word = word.lower()
        if not word in stopwords.words():
            no_punct_word = DELETE_PUNCTUATION_TOKENIZER.tokenize(word)
            if len(no_punct_word) > 0:
                return LEMMATIZER.lemmatize(no_punct_word[0])

def is_multiword(term):
    '''
    Returns whether the given term is a multiword or not.
    '''
    if term.find('_') >= 0 or term.find('-') >= 0 or term.find(' '):
        return True
    return False

def find_dependecy_root(term):
    '''
    This function expects the input term to be a multiword.
    It finds and returns the root of the dependency tree of the multiword.
    '''
    p = term.find('_')
    while p >= 0:
        term = term[:p] + ' ' + term[p+1:]
        p = term.find('_')

    p = term.find('-')
    while p >= 0:
        term = term[:p] + ' ' + term[p+1:]
        p = term.find('-')

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(term)

    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT":
                return token.text

def find_max_sim_synset(term, fn_contexts):
    '''
    Given a term and its context, return the WN synset
    that maximize the similarity score chosen between
    bag-of-words and graphic approach.
    '''
    maxSim = 0
    maxSyns = {}
    term = check_term(term)
    # retrieve synset linked to term
    synsets_of_term = list(wn.synsets(term))

    for syns in synsets_of_term:
        # build synset context
        syns_context = build_syns_context(syns)

        # compute sim(f,s)
        sim = similarity(term, fn_contexts, syns, syns_context) 

        # argmax implementation
        if (sim > maxSim):
            maxSim = sim
            maxSyns = syns
    return [maxSyns, maxSim]

def check_term(term):
    p = term.find('.')
    # check if term is a lexUnit
    if p >= 0:
        term = term[:p] # remove dot and PoS
    # if term is a multiword, get the root of the dependency tree
    if len(wn.synsets(term)) == 0 and is_multiword(term):
        term = find_dependecy_root(term)
    return term

def build_syns_context(syns):
    '''
    Build the context of a synset given in input.
    Return a set that contains the preprocessed words found either
    in the the definition of the synset or in its lemmas.
    The name of the synset is also il the context set.
    '''
    context = set()
    for word in syns.definition().split():
        prep_word = preprocess_word(word)
        if prep_word is not None:
            context.add(prep_word) 
    for word in syns.lemmas():
        prep_word = preprocess_word(word.name())
        if prep_word is not None:
            context.add(prep_word)
    for ex in syns.examples():
        for word in ex:
            prep_word = preprocess_word(word)
            if prep_word is not None:
                context.add(prep_word)
    context.add(syns.name())
    return context

def similarity(term, ctxf, syns, ctxs):
    '''
    Function that computes the similarity of a term and a synset.
    It also chooses between bag-of-words or graphic approach
    based on the 'MODE' parameter. Inputs: term and synset and their contexts.
    'ctxf' is supposed to be a FrameContexts object.
    Returns a number that is the similarity of the given term and synset.
    '''
    sim = 0
    if (MODE == 'bag_of_words'):
        sim = len(ctxs & ctxf.get_frame_context()) + 1
    elif (MODE == 'graphic'):
        sim = _graphic_similarity(term, ctxf, syns)
    #print("Normalized score: {}".format(sim))   
    return sim

def _graphic_similarity(term, ctxf, syns):
    '''
    Function that computes the similarity of a term
    and a synset using the graphic approach.
    Inputs: the term and the synset, plus the FrameContext
    object that is supposed to be 'ctxf'.
    Returns the similarity of the given elements.
    '''
    score = compute_score(ctxf.get_frame_context(),syns)
    return normalize_score(score, term, ctxf)

def compute_score(ctxf, s):
    '''
    Function that computes the score of a synset given a FN context set.
    The score is based on the length of the paths between the synsets linked
    to words in the context 'ctxf' and the given synset 's'. Only length lower
    than the paramter L are considered, while others are ignored.
    '''
    score = 0
    for t in ctxf:
        synsets = wn.synsets(t)
        for s_prime in synsets:
            lengths = syn_distance(s, s_prime)
            if lengths is not None:
                for length in lengths:
                    score += math.e**(-length+1)
    return score

def normalize_score(score, term, ctxf):
    '''
    Function that normalize the given score using
    the words in the given context.
    '''
    normalization = 0
    # We retrieve the synsets linked to 'term'
    synsets = wn.synsets(term)
    for s_prime in synsets:
        for t in ctxf.get_term_contexts().keys():
            # Here 't' will be one of the following:
            # a frame name, a FE name or a LU name
            # We now sum the scores of (Ctx(t), s') pairs
            normalization += compute_score(ctxf.get_term_context(t), s_prime)
    # Return the normalized score
    if normalization == 0:
        normalization = 1
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

    #print(synset1, synset2)
    hypernym1 = synset1.hypernym_paths()
    #print("Hypernym1: {}".format(hypernym1))
    hypernym2 = synset2.hypernym_paths()
    #print("Hypernym2: {}".format(hypernym2))
    common_hyps = synset1.common_hypernyms(synset2)

    lengths_list = list()
    for common_hypernym in common_hyps:
        #print(common_hypernym)
        # remove paths without common_hypernym
        tmp1 = list(filter(lambda x: common_hypernym in x, hypernym1))
        tmp2 = list(filter(lambda x: common_hypernym in x, hypernym2))

        # get positions of common_hypernym in every path of hypernym1 and hypernym2
        positions1 = list(map(lambda x: len(x) - x.index(common_hypernym), tmp1)) # len - index = position from the end
        positions2 = list(map(lambda x: len(x) - x.index(common_hypernym), tmp2))

        #print(positions1)
        # sum
        for pos1 in positions1:
            for pos2 in positions2:
                sum = pos1 + pos2
                if sum <= L:
                    lengths_list.append(sum)

    #print(lengths_list)
    return lengths_list

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
            {'id': 2585, 'name': 'Revolution'}, # changed from Morality_Evaluation
            {'id': 1771, 'name': 'Thriving'},
            {'id': 278, 'name': 'Text_creation'},
            {'id': 2827, 'name': 'Catching_fire'},
            {'id': 1155, 'name': 'State_continue'},
            {'id': 793, 'name': 'Being_born'}, # changed from Alignment_image_schema
            {'id': 2481, 'name': 'Erasing'}]

frames_number = [0,1,2,3,4,5,6,7,8,9] # position in frameSet of frames to map


res = {'mapped_frames': []} # This dict will have a key for every frame of frameSet, where each frame will have as
# value another dictionary, this time with two keys: similarities and not_found_in_wn.
# The values will be the corresponding lists.
# Additionally, res will have a key 'mapped_frames' which will contain all frames that will have been mapped
# res = {'frame0': {'similarities': [...], 'not_found_in_wn': [...] },
#       'frame1': {'similarities': [...], 'not_found_in_wn': [...] },
#       'mapped_frames': [0,1] }

# First we check if a file exists in which the parameters are the same as this run
file_path = 'results/result_{}_{}.json'.format(MODE,L)
if os.path.exists(file_path):
    mapped_frames = []
    with open(file_path, 'r') as f:
        # For every frame we have already mapped, load the results
        json_dict = json.load(f)
        res['mapped_frames'] = json_dict['mapped_frames']
        for i in frames_number:
            if i in res['mapped_frames']:
                name = frameSet[i]['name']
                print("Results already calculated with these parameters. Loading frame {}.".format(name))
                res[name] = json_dict[name]
                mapped_frames.append(i)
        
        # Remove the already mapped frames from frames_number
        frames_number = list(set(frames_number) - set(mapped_frames))

# Compute the results for every frame left
for i in frames_number:
    not_found_in_wn = [] # This list will contain all the terms of a frame that were not found in wordnet
    similarities = [] # List of triplettes of the form '[term, syns, sim]' where
    # - 'term' is a FN term from the frame,
    # - 'syns' is the WN synset mapped to that term,
    # - 'sim' is the similarity score that was calcuted with either a bag-of-words approach or a graphic approach

    # Get one of the frames
    frame = fn.frame( frameSet[i]['id'] )
    res[frame.name] = {'similarities': [], 'not_found_in_wn': []}

    # Build context sets of frame. See FrameContexts.py for more details
    contexts = FrameContexts(frame)
    #pprint(contexts.get_frame_context())
    #pprint(contexts.get_term_contexts())

    #print(contexts.get_term_context('Prominence'))
    
    for term in contexts.get_term_contexts().keys():
        # Find the WN synset that maximizes a similarity measure.
        maxSyns, maxSim = find_max_sim_synset(term, contexts)
        
        # Check to see if the term has not been found in WN
        if isinstance(maxSyns, dict) and len(maxSyns) == 0:
            not_found_in_wn.append(term)
            continue

        # Save the results as a triple '[term, syns, sim]'
        similarities.append([term, maxSyns.name(), maxSim])
        print(term, maxSyns, maxSim)

    res['mapped_frames'].append(i)
    res[frame.name]['similarities'] = similarities.copy()
    res[frame.name]['not_found_in_wn'] = not_found_in_wn.copy()
    
# Once every term has been mapped, save the results in a JSON file
with open(file_path, 'w') as f:
    json.dump(res,f, indent=4)
    

print("Program ended. Mapped frames: {}".format(res.keys()))

