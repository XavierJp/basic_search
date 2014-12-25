from Query import Query
from Index_generator import Index_generator
from math import log
from collections import defaultdict
import operator
# Class
# ------------------------------
class Index:
    """
    Represent an Index

    """

    def __init__(self):
        self.raw_data = Index_generator()
        self.w_max = self.w_max()
        self.reversed_index = self.reverse_index()

    def __str__(self):
        return str(self.reversed_index)

    def reverse_index(self):
        rev_index = defaultdict(str)
        for word in self.raw_data.word_doc_index.keys():
            rev_index[word] = defaultdict(str)
            for doc_id in self.raw_data.word_doc_index[word].keys():
                rev_index[word][doc_id] = defaultdict(str)
                w = self.raw_data.word_doc_index[word][doc_id]
                rev_index[word][doc_id]['w'] = w
                rev_index[word][doc_id]['w_n'] = float(w)/float(self.w_max[doc_id])
                rev_index[word][doc_id]['tf_idf'] = self.tf_idf(word, w)
                pass
        return rev_index

    def w_max(self):
        w_max_dict = defaultdict(int)
        for doc_id in self.raw_data.doc_word_index.keys():
            w_max = max(self.raw_data.doc_word_index[doc_id].values())
            w_max_dict[doc_id] = w_max
        return w_max_dict

    #tf_idf
    def tf_idf(self, word, frq):
        return self.tf(frq)*self.idf(len(self.raw_data.word_doc_index[word].keys()), self.raw_data.doc_number)

    #Log(inverse de la proportion de documents qui contiennent le terme)
    def idf(self, dt, N):
        return log(float(N)/float(dt))

    # Nb occurrences de ce terme dans le document
    def tf(self, frq):
        if frq >0: return 1 + log(frq)
        return 0
