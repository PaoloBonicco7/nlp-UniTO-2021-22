import requests
from pprint import pprint

key = '8be6bdbd-78ee-4efb-91a2-3854f79a97e0'
id = 'bn:00050409n'
url = 'https://babelnet.io/v7/getSynset?id={}&key={}&targetLang=IT'.format(id,key)

x = requests.get(url)
senses = x.json()['senses']
for sense in senses:
    pprint(sense['properties']['fullLemma'])

# Questo codice è equiparabile a wn.synset.lemmas()
