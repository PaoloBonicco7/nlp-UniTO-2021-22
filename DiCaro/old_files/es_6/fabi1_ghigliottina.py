import urllib.parse as up
import urllib.request as ur
import json
import gzip
from collections import Counter
from io import BytesIO


WORDS_1 = ['pneumatico', 'volante', 'freno a mano']

def get_indexes_by_word(word):
    service_url = 'https://babelnet.io/v6/getSynsetIds'

    lemma = word
    lang = 'IT'
    key  = '5da132f9-c606-4832-9a4f-3c2e3f739cf7'

    params = {
            'lemma' : lemma,
            'searchLang' : lang,
            'key'  : key
    }

    url = service_url + '?' + up.urlencode(params)
    request = ur.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = ur.urlopen(request)
    list_indexs = []
    if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = json.loads(f.read())
            for result in data:
                    list_indexs.append(result['id'])
            return list_indexs

def get_synset_by_id(id):
    service_url = 'https://babelnet.io/v6/getSynset'

    key  = '5da132f9-c606-4832-9a4f-3c2e3f739cf7'

    params = {
        'id' : id,
        'key'  : key,
        'targetLang' : 'IT'
    }

    url = service_url + '?' + up.urlencode(params)

    request = ur.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = ur.urlopen(request)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())

        # retrieving BabelGloss data
        glosses = data['glosses']
        res = []
        for result in glosses:
            gloss = result.get('gloss')
            language = result.get('language')
            if language != None:
                res.append(str(gloss.encode('utf-8')))
            
        return res

def count(final_description):
    counter = Counter()
    for l in final_description:
        
        print(list(l))
        counter.update(l)
    print(counter.most_common(3))

'''final_description = []
for word in WORDS_1:
    list_indexs = get_indexes_by_word(word)

    if list_indexs != []:
        for index in list_indexs:
            final_description.append(get_synset_by_id(index))
'''
abb = [['b"Pertinente o relativo all\'aria o ad altri gas."'], [], ['b"La pneumatica dal greco \\xcf\\x80\\xce\\xbd\\xce\\xb5\\xcf\\x85\\xce\\xbc\\xce\\xb1\\xcf\\x84\\xce\\xb9\\xce\\xba\\xcf\\x8c\\xcf\\x82 \\xc3\\xa8 una branca della fisica e della tecnologia che studia il trasferimento di forze mediante l\'utilizzo di gas in pressione, molto spesso aria compressa."', "b'Ramo della meccanica che si occupa delle propriet\\xc3\\xa0 meccaniche dei gas.'"], ['b"Involucro di gomma che avvolge la camera d\'aria dei pneumatici di un veicolo"', 'b"Lo pneumatico, \\xc3\\xa8 l\'elemento che viene montato sulle ruote di un veicolo e che permette l\'aderenza del veicolo stesso sulla strada, fermo o durante il moto, determinando assieme al peso complessivo del veicolo e al tipo di fondo stradale il suo attrito sul suolo."', 'b"Elemento che montato sulle ruote ne permette l\'aderenza del veicolo sulla strada."', "b'Anello di gomma spessa posto sopra il cerchio di una ruota di un veicolo stradale per fornire trazione e ridurre gli impatti dovuti alle imperfezioni delle strade.'"], ['b"Movimento di uccelli, aerei o veicoli nell\'atmosfera"', 'b"Il volo \\xc3\\xa8 il processo tale per cui un animale o un oggetto si sposta nell\'aria attraverso l\'uso di una forza diretta verso l\'alto detta portanza."', "b'Processo fisico'"], ['b"Organo che fa parte dell\'apparato di sterzo di un autoveicolo"'], ['b"La squadra volante della Polizia di Stato \\xc3\\xa8 una sezione dell\'Ufficio Prevenzione Generale e Soccorso Pubblico della Polizia di Stato italiana, che assicura il pronto intervento 24 ore su 24."'], ["b'Gli attributi araldici di azione sono quelli che definiscono la posizione assunta, per effetto di una specifica azione, da una figura che compare in uno stemma.'"], ["b'Il volante \\xc3\\xa8 un organo meccanico di forma circolare che serve per controllare la direzione di un veicolo.'", "b'Organo meccanico di forma circolare che serve per imprimere manualmente ad un asse un movimento rotatorio'", "b'Organo meccanico di forma circolare che serve per controllare la direzione di un veicolo'", "b'Oggetto circolare usato per guidare determinati tipi di veicoli (ad es. le automobili).'"], ["b'Reparto di polizia.'"], [], [], ["b'Il freno di stazionamento \\xc3\\xa8 il freno presente sugli autoveicoli che permette di bloccare il veicolo durante le soste o quando si effettuano partenze in salita.'", "b'Freno di bloccaggio utilizzato per mantenere la vettura ferma.'"]]

bba = [["Ciao come va"], ["Io tutto bene"]]
count(abb)
