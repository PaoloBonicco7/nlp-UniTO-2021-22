import json
import os

'''
File che serve per valutare i rusltati ottenuti nel mapping di framenet su wordnet.
Per la valutazione si usa valutation_dict, un dizionario scritto a mano (grazie al file construct_valutation_dict.py)
che contiene per ogni elemento da mappare di ogni frame il nome del synset mappato a mano.
La valutazione vera e propria si effettua contando gli elementi mappati correttamente dall'algoritmo confrontandoli con
valutation_dict, e dividendo il numero così ottenuto per il num totale di elementi mappati.
'''

L = 3
#MODE = 'graphic'
MODE = 'bag_of_words'

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
frames_number = [0]
res = {}
valutation_dict = {
    'Inhibit_motion_scenario': {
        'Agent': 'agentive_role.n.01',
        'Cause': 'causal_agent.n.01',
        'Holding_location': 'placement.n.03',
        'Inhibit_motion_scenario': 'inhibit.v.04',
        'Theme': 'theme.v.01'
    }
}

file_path = 'results/result_{}_{}.json'.format(MODE,L)
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        json_dict = json.load(f)
        for i in frames_number:
            if i in json_dict['mapped_frames']:
                name = frameSet[i]['name']
                print("Loading frame {}.".format(name))
                res[name] = json_dict[name]
count = 0
total = 0
correct = []
for frame in res.keys():
    for [term, syns, sim] in res[frame]['similarities']:
        total += 1
        if syns == valutation_dict[frame][term]:
            count+=1
            correct.append(term)

print("Correct: ", count, "\nTotal: ", total, "\nAccuracy: ", count/total)
print(correct)

'''
res = {'Inhibit_motion_scenario': {'similarities': [...], 'not_found_in_wn': [...] },
           'frame1': {'similarities': [...], 'not_found_in_wn': [...] },
           'mapped_frames': [0,1] }
'''