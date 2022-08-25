from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from pprint import pprint
from FrameContexts import FrameContexts
import spacy

'''
Questo file serve unicamente per costruire valutation_dict a mano, cioè il dizionario che verrà usato nella valutazione.
Il suo scopo è stampare i termini da mappare con relative definizioni e WN synset collegati, in modo da rendere più facile
il mapping da fare a mano.
'''
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
            {'id': 2585, 'name': 'Revolution'},
            {'id': 1771, 'name': 'Thriving'},
            {'id': 278, 'name': 'Text_creation'},
            {'id': 2827, 'name': 'Catching_fire'},
            {'id': 1155, 'name': 'State_continue'},
            {'id': 793, 'name': 'Being_born'},
            {'id': 2481, 'name': 'Erasing'}]

frames_number = [9]

res = {}

# Print all things
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

        print(term)
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
        'Prominence': 'prominence.n.01',
        'Entity' : 'entity.n.01',
        'Attribute': 'property.n.04',
        'Degree': 'degree.n.01',
        'Time': 'time.n.03',
        'Circumstances': 'circumstances.n.02',
        'Place': 'place.n.04',
        'salient.a': 'outstanding.s.02',
        'prominent.a': 'outstanding.s.02',
        'conspicuous.a': 'conspicuous.a.01',
        'eye-catching.a': 'attention-getting.s.01',
        'flashy.a': 'brassy.s.02',
        'blatant.a': 'blatant.s.01',
        'quiet.a': 'quiet.a.01'
    },
    'Have_associated': {
        'Have_associated': 'associate.v.01',
        'Entity': 'entity.n.01',
        'Time': 'time.n.03',
        'Duration': 'duration.n.03',
        'Explanation': 'explanation.n.01',
        'Place': 'place.n.04',
        'Circumstances': 'circumstances.n.02',
        'Viewpoint': 'point_of_view.n.01',
        'Concessive': 'concessive.a.01',
        'Topical_entity': 'entity.n.01',
        'Depictive': 'delineative.s.01',
        'Period_of_iterations': 'time_period.n.01',
        'have.v': 'have.v.07',
        'have got.v': 'have.v.07',
        'with.v': None
    },
    'Revolution': {
        'Revolution': 'revolution.n.01',
        'Agent': 'agentive_role.n.01',
        'Current_leadership': 'leadership.n.02',
        'Current_order': 'order.n.03',
        'Place': 'topographic_point.n.01',
        'Time:': 'time.n.03',
        'Means': 'means.n.01',
        'Degree': 'degree.n.01',
        'Manner': 'manner.n.01',
        'revolutionary.n': 'revolutionist.n.01',
    },
    'Thriving': {
        'Thriving': 'booming.s.01',
        'Entity': 'entity.n.01',
        'Circumstances': 'context.n.02',
        'Time': 'time.n.03',
        'Place': 'place.n.04',
        'Frequency': 'frequency.n.01',
        'Role': 'role.n.04',
        'Particular_iteration': 'iteration.n.01',
        'Duration': 'duration.n.03',
        'Explanation': 'explanation.n.01',
        'Desirability': 'desirability.n.01',
        'thrive.v': 'boom.v.05',
        'flourish.v': 'boom.v.05',
        'prosper.v': 'thrive.v.02',
        'languish.v': 'languish.v.03',
        'slump.n': 'slump.n.01',
        'do.v': 'do.v.04',
        'fare.v': 'fare.v.02',
        'prosperity.n': 'prosperity.n.01',
        'live.v': 'populate.v.01'
    },
    'Text_creation': {
        'Text_creation': 'creation.n.01',
        'Author': 'writer.n.01',
        'Components': 'component.n.01',
        'Text': 'text.n.01',
        'Depictive': 'delineative.s.01',
        'Instrument': 'instrument.n.02',
        'Place': 'place.n.03',
        'Manner': 'manner.n.01',
        'Means': 'means.n.01',
        'Purpose': 'purpose.n.01',
        'Time': 'time.n.03',
        'Beneficiary': 'beneficiary.n.01',
        'Form': 'form.n.10',
        'Explanation': 'explanation.n.01',
        'Medium': 'medium.n.01',
        'pen.v': 'write.v.01',
        'author.v': 'author.v.01',
        'write.v': 'write.v.01',
        'compose.v': 'write.v.01',
        'draft.v': 'draft.v.01',
        'jot down.v': None,
        'jot.v': 'jot_down.v.01',
        'speak.v': 'talk.v.02',
        'say.v': 'read.v.02',
        'utter.v': 'utter.v.02',
        'write up.v': None,
        'write down.v': None,
        'write in.v': None,
        'write out.v': None,
        'print.v': 'print.v.04',
        'type.v': 'type.v.01',
        'type out.v': None,
        'type up.v': None,
        'type in.v': None,
        'print out.v': None,
        'print up.v': None,
        'get down.v': None,
        'chronicle.v': 'chronicle.v.01',
        'sign.v': 'sign.v.01',
        'dash off.v': None,
        'ist.v': 'list.v.01'
    },
    'Catching_fire': {
        'Catching_fire': 'burn.v.01',
        'Place': 'place.n.03',
        'Time': 'time.n.03',
        'Fire': 'fire.n.01',
        'Fuel': 'fuel.n.01',
        'Manner': 'manner.n.01',
        'Explanation': 'explanation.n.03',
        'break out.v': None,
        'catch.v': 'catch.v.12',
        'catch fire.v': None,
        'start.v': 'originate.v.02',
        'combust.v': 'burn.v.05'
    },
    'State_continue': {
        'State_continue': 'continue.v.01',
        'Entity': 'entity.n.01',
        'State': 'state.n.02',
        'Time': 'time.n.03',
        'Place': 'place.n.04',
        'Explanation': 'explanation.n.03',
        'Duration': 'duration.n.01',
        'Circumstances': 'circumstances.n.02',
        'Depictive': 'delineative.s.01',
        'remain.v': 'stay.v.01',
        'stay.v': 'stay.v.01',
        'rest.v': 'stay.v.01'
    },
    'Being_born': {
        'Being_born': 'born.n.01',
        'Child': 'child.n.01',
        'Time': 'time.n.03',
        'Place': 'topographic_point.n.01',
        'Relatives': 'relative.n.01',
        'Depictive': 'delineative.s.01',
        'Means': 'means.n.01',
        'come into the world.v': None,
        'born.v': 'give_birth.v.01',
    },
    'Erasing': {
        'Erasing': 'erase.v.02',
        'Agent': 'agent.n.02',
        'Information': 'information.n.03',
        'Cause': 'cause.n.01',
        'Document': 'document.n.01',
        'Manner': 'manner.n.01',
        'Time': 'time.n.03',
        'Place': 'place.n.04',
        'Means': 'means.n.01',
        'strike.v': 'strike.v.14',
        'delete.v': 'erase.v.03',
        'erase.v': 'erase.v.03',
        'expunge.v': 'strike.v.14',
        'kill.v': 'kill.v.12'
    }
}