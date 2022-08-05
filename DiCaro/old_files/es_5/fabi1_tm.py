from gensim.test.utils import simple_preprocess
from gensim.corpora.dictionary import Dictionary
from gensim import models
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def get_text_from_file(path):
    file = []
    stop_words = set(stopwords.words('english'))
    with open (path, 'r') as f:
        for row in f:
            filtered_s = [w for w in word_tokenize(row) if not w.lower() in stop_words]
            file.append(simple_preprocess(str(filtered_s), deacc=True))
    f.close()
    return file

text = get_text_from_file('topics.txt')
common_dictionary = Dictionary(text)
common_corpus = [common_dictionary.doc2bow(line) for line in text]

lsi_model = models.LsiModel(common_corpus, id2word = common_dictionary, num_topics=3)
pprint(lsi_model.print_topics(3))