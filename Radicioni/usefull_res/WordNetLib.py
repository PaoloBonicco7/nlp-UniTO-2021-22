from iteration_utilities import deepflatten
from nltk.corpus import wordnet as wn

class WordNetLib:
    
    def __init__(self):
        '''
        Constructor. Because computing the max depth of the graph is a very
        expensive task, it is computed here once for all the class.
        '''
        self.depth_max = 20
        # self.depth_max = self.__depth_max() #! For test purpose is disabled
    
    @staticmethod  
    def get_synsets(term):
        '''
        Retrurn the synsets of a term.
        '''
        if(len(wn.synsets(term)) > 0):
            return wn.synsets(term)
        return None

    @staticmethod
    def depth(syn):
        '''
        Return the distance between the WorNet root and a synset.
        '''
        if(syn is None):
            return 0
        if(type(syn) is list):
            if(len(syn) > 0):
                return syn[0].max_depth()
            return 0
        return syn.max_depth()

    @staticmethod
    def lch(syn1, syn2): #? WordNet function
        '''
        Return the lowest common hypernyms of two synsets.
        '''
        if(syn1 is None or syn2 is None):
            return None
        return syn1.lowest_common_hypernyms(syn2)

    @staticmethod
    def lowest_common_subsumer(synset1, synset2): #? My function taht simulate the WordNet function
        """
        Args:
            synset1: first synset to take LCS from
            synset2: second synset to take LCS from
        Returns:
            the first common LCS
        """
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

    @staticmethod
    def wu_pal_sim(syn1, syn2): #? WordNet function
        '''
        Return the Wu-Palmer similarity of two synsets.
        '''
        if(syn1 is None or syn2 is None):
            return 0
        return syn1.wup_similarity(syn2)

    def my_wu_pal_sim(self, syn1, syn2): #? My function that simulate the WordNet function
        if(syn1 is None or syn2 is None):
            return None
        else:
            if(self.depth(syn1) + self.depth(syn2) == 0):
                return 0
            return 2.0 * self.depth(self.lowest_common_subsumer(syn1, syn2)) / (self.depth(syn1) + self.depth(syn2))
       
    def max_similarity(self, syns1, syns2):
        sim_max = ("", "", 0)
        
        if(syns1 is not None and syns2 is not None):
            for syn1 in syns1:
                for syn2 in syns2:
                    if(syns1 is not None and syns2 is not None):
                        sim = self.my_wu_pal_sim(syn1, syn2)
                        if sim > sim_max[2]:
                            sim_max = (syn1, syn2, sim)      
                            
        return sim_max

    @staticmethod
    def depth_path(synset, lcs):
        """
        It measures the distance (depth) between the given Synset and the WordNet's root.
        Args:
            synset: synset to reach from the root
            lcs: Lowest Common Subsumer - the first common sense or most specific ancestor node
        Returns:
            the minimum path which contains LCS
        """
        paths = synset.hypernym_paths()
        paths = list(filter(lambda x: lcs in x, paths))  # all path containing LCS
        return min(len(path) for path in paths)
    
    def distance(self, synset1, synset2):
        """
        Args:
            synset1: first synset to calculate distance
            synset2: second synset to calculate
        Returns:
            distance between the two synset
        """
        lcs = self.lowest_common_subsumer(synset1, synset2)
        if lcs is None:
            return None

        hypernym1 = synset1.hypernym_paths()
        hypernym2 = synset2.hypernym_paths()

        # paths from LCS to root
        hypernym_lcs = lcs.hypernym_paths()

        # create a set of unique items flattening the nested list
        set_lcs = set(deepflatten(hypernym_lcs))

        # remove root
        set_lcs.remove(lcs)

        # path from synset to LCS
        hypernym1 = list(map(lambda x: [y for y in x if y not in set_lcs], hypernym1))
        hypernym2 = list(map(lambda x: [y for y in x if y not in set_lcs], hypernym2))

        # path containing LCS
        hypernym1 = list(filter(lambda x: lcs in x, hypernym1))
        hypernym2 = list(filter(lambda x: lcs in x, hypernym2))

        return min(list(map(lambda x: len(x), hypernym1))) + min(list(map(lambda x: len(x), hypernym2))) - 2

    
    @staticmethod
    def max_path():
        """
        Returns:
            The max depth of WordNet tree (20)
        """
        max_path = 0
        for synset in wn.all_synsets():
            if synset.max_depth() > max_path:
                max_path = synset.max_depth()
        return max_path

    @staticmethod
    def max_path_2(): #? Alternative of the method above
        return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())
