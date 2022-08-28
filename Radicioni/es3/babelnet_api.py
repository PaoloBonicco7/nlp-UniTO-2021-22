import requests
from pprint import pprint

def terms_list(path):
    terms = []

    with open (path, 'r') as f:
        for line in f:
            terms.extend([word.replace('\n','') for word in line.split('\t')])
    
    return terms

def synset_list(term_list, path):
    res = {}
    with open(path, 'r') as file:
        lines = file.readlines()
        init_terms = find_terms(lines, term_list)
        print(init_terms)
        for i in range(len(init_terms)):
            start = init_terms[i]
            for term in term_list:
                res[term] = {}
                res[term]['ids'] = []
                if i+1<len(init_terms):
                    end = init_terms[i+1] 
                    for line in lines[start+1:end-1]:
                        line = line.replace('\n', '')
                        #res[term]['ids'].append(line)
                else:
                    for line in lines[start:]:
                        line = line.replace('\n', '')
                        #res[term]['ids'].append(line)
    return res

def find_terms(lines, term_list):
    res = []
    for i in range(len(lines)):
        if lines[i].find('#') == 0 and lines[i][1:-1] in term_list:
            res.append(i)
    return res

def find_missing_term(lines, term_list, init_terms):
    res = []
    terms = [lines[i][1:-1] for i in init_terms]
    term_list.sort()
    terms.sort()
    for i in range(len(term_list)):
        print(term_list[i], terms[i])

terms = terms_list('term_list.txt')
print(len(terms))
#res = synset_list(terms, '../data/es3_res/SemEval17_IT_senses2synsets.txt')
#pprint(len(res))

with open('../data/es3_res/SemEval17_IT_senses2synsets.txt', 'r') as file:
    lines = file.readlines()
    init_terms = find_terms(lines, terms)
    print(len(init_terms))
    missing = find_missing_term(lines, terms, init_terms)
    #print(missing)
'''
key = '8be6bdbd-78ee-4efb-91a2-3854f79a97e0'
for id in ids:
    
    url = 'https://babelnet.io/v7/getSynset?id={}&key={}&targetLang=IT'.format(id,key)

    x = requests.get(url)
    senses = x.json()['senses']

    for sense in senses:
        pprint(sense['properties']['fullLemma'])
'''