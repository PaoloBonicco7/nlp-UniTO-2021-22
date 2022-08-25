from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

'''
Questo file serve unicamente per costruire i contesti di FN che vengono usati nell'esercizio 3.
In particolare un oggetto FrameContexts ha due contesti diversi:
- frame_context: un set contenente tutte le parole (preproc.) di tutte le definizioni di frame, FE e LU
- term_context: un dizionario le cui chiavi sono nome del frame, nomi dei FE e nomi delle LU (non preproc.), ciascuna
delle quali ha come valore i termini preprocessati della corrispondente definizione
'''

LEMMATIZER = WordNetLemmatizer()
DELETE_PUNCTUATION_TOKENIZER = RegexpTokenizer(r'\w+')

class FrameContexts():
    def __init__(self, frame):
        self.name = frame.name
        self.lemmatizer = LEMMATIZER
        self.delete_punctuation_tokenizer = DELETE_PUNCTUATION_TOKENIZER
        self.frame_context = set()
        self.term_context = dict()
        self.build_name_context(frame)
        self.build_fes_context(frame)
        self.build_lu_context(frame)
        
    def get_term_context(self, term):
        return self.term_context[term]

    def get_term_contexts(self):
        return self.term_context

    def get_frame_context(self):
        return self.frame_context

    def build_name_context(self, frame):
        ctx = self._build_word_definition_context(frame)
        self.frame_context.add(frame.name)
        self.frame_context.update(ctx)
        self.term_context[self.name] = ctx

    def build_fes_context(self, frame):
        '''
        Use every Frame Element's definition and name in order 
        to build a context set for the frame itself. 
        Returns a list of lemmatized words with stopwords removal
        that comprised the context set.
        '''
        fn_fe_context = set()
        for fe_key in frame.FE.keys():
            fe = frame.FE[fe_key]
            name = self._preprocess_word(fe.name)
            context = set([name]) if name is not None else set()
            context.update(self._build_word_definition_context(fe))
            self.term_context[fe.name] = context
            fn_fe_context.update(context)
        self.frame_context.update(fn_fe_context)

    def build_lu_context(self, frame):
        fn_lu_context = set()
        for lu_key in frame.lexUnit.keys():
            lu = frame.lexUnit[lu_key]
            p = lu.name.find('.')
            name = self._preprocess_word(lu.name[:p])
            context = set([name]) if name is not None else set()
            context.update(self._build_word_definition_context(lu))
            self.term_context[lu.name] = context
            fn_lu_context.update(context)
        self.frame_context.update(fn_lu_context)

    def _build_word_definition_context(self, fn_word):
        context = set()
        for word in fn_word.definition.split():
            prep_word = self._preprocess_word(word)
            if prep_word is not None and prep_word not in ["cod", "fn", "fe"]:
                context.add(prep_word)
        return context

    def _preprocess_word(self, word):
        word = word.lower()
        if not word in stopwords.words():
                no_punct_word = self.delete_punctuation_tokenizer.tokenize(word)
                if len(no_punct_word) > 0:
                    return self.lemmatizer.lemmatize(no_punct_word[0])
