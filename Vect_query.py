from Config import Config
from Query import Query
from collections import defaultdict
from math import sqrt
import re

# Class
# ------------------------------

class Vect_query(Query):
    """
    Vectorial Query

    """

    def indexize(self, query):
        query_index = defaultdict(int)
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+",query)
        for word in wordsBuffer:
            word = word.lower()
            if not self.compare(word):
                query_index[word] +=1
        return query_index

    def compare(self, element):
        if element in self.config.words:
            return True
        return False

    #project query_vector over every doc_vector
    def execute_query(self):
        results_temp=defaultdict(float)
        for doc_id in self.my_index.raw_data.doc_word_index.keys():
            #cosinus(vecteur-requete,vecteur-document_courant)
            c = self.cosinus(self.indexed_query, doc_id)
            if c:
                results_temp[doc_id] = c
        return results_temp

    #calculates cosinus between two vectors of w_space
    def cosinus(self, indexed_query, doc_id):
        p = 0
        n = 0
        for w in indexed_query.keys():
            if w in self.my_index.raw_data.doc_word_index[doc_id]:
                p += float(indexed_query[w])*float(self.my_index.reversed_index[w][doc_id]['w'])
            n += int(indexed_query[w])*int(indexed_query[w])
        if p != 0:
            n = sqrt(n)
            return float(float(p)/(n*self.norm(doc_id)))
        else:
            return 0

    def norm(self, doc_id):
        n=0
        for w in self.my_index.raw_data.doc_word_index[doc_id]:
            n += int(self.my_index.reversed_index[w][doc_id]['w'])^2
        return sqrt(float(n))
