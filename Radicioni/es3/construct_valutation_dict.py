from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from pprint import pprint
from FrameContexts import FrameContexts
import spacy

'''
Questo file serve unicamente per costruire valutation_dict a mano, cioè il dizionario che verrà usato nella valutazione.
Il suo scopo è stampare i termini da mappare con relative definizioni e WN synset collegati, in modo da rendere più facile
il mapping da fare a mano.

PROBLEMI:
- nomi delle LU da modificare prima di cercare in WN
'''
def is_multiword(term):
    '''
    Returns whether the given term is a multiword or not.
    '''
    if term.find('_') >= 0:
        return True
    return False

def find_dependecy_root(term):
    '''
    This function expects the input term to be a multiword.
    It finds and returns the root of the dependency tree of the multiword.
    '''
    phrase = term.replace('_', ' ')
    phrase = term.replace('-', ' ')
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(phrase)

    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT":
                return token.text

def print_definition(term, frame):
    msg = term + ": "
    if term in frame.FE.keys():
        msg += frame.FE[term].definition
    elif term in frame.lexUnit.keys():
        msg += frame.lexUnit[term].definition
    elif term == frame.name:
        msg += frame.definition
    else: 
        return
    print(msg)

def check_term(term):
    p = term.find('.')
    # check if term is a lexUnit
    if p >= 0:
        term = term[:p] # remove dot and PoS
    # if term is a multiword, get the root of the dependency tree
    if len(wn.synsets(term)) == 0 and is_multiword(term):
        term = find_dependecy_root(term)
    return term

frameSet = [{'id': 2664, 'name': 'Inhibit_motion_scenario'},
                {'id': 1460, 'name': 'Prominence'},
                {'id': 1933, 'name': 'Have_associated'},
                {'id': 370, 'name': 'Morality_evaluation'},
                {'id': 1771, 'name': 'Thriving'},
                {'id': 278, 'name': 'Text_creation'},
                {'id': 2827, 'name': 'Catching_fire'},
                {'id': 1155, 'name': 'State_continue'},
                {'id': 2020, 'name': 'Alignment_image_schema'},
                {'id': 2481, 'name': 'Erasing'}]

frames_number = [1]

res = {}
for i in frames_number:
    frame = fn.frame( frameSet[i]['id'] )
    contexts = FrameContexts(frame)

    for term in contexts.get_term_contexts():
        
        print_definition(term, frame)
        term = check_term(term)
        synsets_of_term = list(wn.synsets(term))

        res[term] = []
        
        for syns in synsets_of_term:
            tmp = [syns.name()]
            examples = syns.examples()
            lemmas = syns.examples()
            if not len(examples) == 0:
                tmp.extend(examples)
            elif not len(lemmas) <= 1:
                tmp.extend(lemmas)
            else:
                tmp.extend(syns.hyponyms())

            res[term].append(tmp)

        pprint(res[term])
        print("\n")

valutation_dict = {
    'Inhibit_motion_scenario': {
        'Agent': 'agentive_role.n.01',
        'Cause': 'causal_agent.n.01',
        'Holding_location': 'placement.n.03',
        'Inhibit_motion_scenario': 'inhibit.v.04',
        'Theme': 'theme.v.01'
    },
    'Prominence': {
        'Attribute': 'attribute.n.02',
    }
}