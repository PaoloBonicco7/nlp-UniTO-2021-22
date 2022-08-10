import math
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pprint import pprint
import json
import os

from FrameContexts import FrameContexts # custom class we made to better utilize context sets

L = 3
MODE = 'graphic'
#MODE = 'bag_of_words'
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
        sim = len(ctxs & ctxf.get_frame_context())
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
            length = syn_distance(s, s_prime)
            if length is None or length > L:
                continue
            score += math.e**(-length+1)
    return score

def normalize_score(score, term, ctxf):
    '''
    Function that normalize the given score using
    the words in the given context.
    '''
    normalization = 0
    for t in ctxf.get_term_contexts().keys():
        # Here 't' will be one of the following:
        # a frame name, a FE name or a LU name

        # We retrieve the synsets linked to 'term'
        synsets = wn.synsets(term)
        for s_prime in synsets:
            # We now sum the scores of (Ctx(t), s') pairs
            normalization += compute_score(ctxf.get_term_context(t), s_prime)
    # Return the normalized score
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
frames_number = [0,1,2,3,4] # position in frameSet of frames to map


res = {} # This dict will have a key for every frame of frameSet, where each frame will have as
# value another dictionary, this time with two keys: similarities and not_found_in_wn.
# The values will be the corresponding lists.
# Additionally, res will have a key 'mapped_frames' which will contain all frames that will have been mapped
# res = {'frame0': {'similarities': [...], 'not_found_in_wn': [...] },
#       'frame1': {'similarities': [...], 'not_found_in_wn': [...] },
#       'mapped_frames': [0,1] }
not_found_in_wn = [] # This list will contain all the terms of a frame that were not found in wordnet
similarities = [] # List of triplettes of the form '[term, syns, sim]' where
# - 'term' is a FN term from the frame,
# - 'syns' is the WN synset mapped to that term,
# - 'sim' is the similarity score that was calcuted with either a bag-of-words approach or a graphic approach

# First we check if a file exists in which the parameters are the same as this run
file_path = 'results/result_{}_{}.json'.format(MODE,L)
if os.path.exists(file_path):
    mapped_frames = []
    with open(file_path, 'r') as f:
        # For every frame we have already mapped, load the results
        json_dict = json.load(f)
        res['mapped_frames'] = json_dict['mapped_frames']
        all_frames_mapped = True
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
    # Get one of the frames
    frame = fn.frame( frameSet[i]['id'] )
    res[frame.name] = {'similarities': [], 'not_found_in_wn': []}

    # Build context sets of frame. See FrameContexts.py for more details
    contexts = FrameContexts(frame)
    #pprint(contexts.get_frame_context())
    #pprint(contexts.get_term_contexts())

    for term in contexts.get_frame_context():
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
    res[frame.name]['similarities'] = similarities
    res[frame.name]['not_found_in_wn'] = not_found_in_wn

# Once every term has been mapped, save the results in a JSON file
with open(file_path, 'w') as f:
    json.dump(res,f, indent=4)

print("Program ended. Mapped frames: {}".format(res.keys()))

