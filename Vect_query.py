# -*- coding: utf-8 -*-

# Imports
# -------
from Config import Config
from Query import Query
from collections import defaultdict
from math import sqrt
from math import log10
import re
import operator

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
        doc_list = defaultdict(dict)
        for word in self.indexed_query:
            if word in self.my_index.reversed_index:
                for doc in self.my_index.reversed_index[word]:
                    if doc != 'df':
                        df = self.my_index.reversed_index[word]['df']
                        tf = self.my_index.reversed_index[word][doc]
                        doc_list[doc][word] = self.ponderation(tf, df, 'w')
        for doc in doc_list:
            doc_list[doc]['cos'] = self.cosinus(self.indexed_query, doc_list[doc], doc, 'tf_idf') 
        return doc_list

    def ponderation(self, tf, df ,pond_type):
        if pond_type=='tf_idf':
            return self.tf_log(tf)*self.idf(df)
        elif pond_type=='w':
            max_w = max(self.my_index.index.iteritems(), key=operator.itemgetter(1))[0]
            return float(tf)/float(max_w)


    #calculates cosinus between two vectors of w_space
    def cosinus(self, indexed_query, indexed_doc, doc_id, pond_type):
        p = 0
        norm_q = 0
        for w, w_freq in indexed_query.iteritems():
            if w in indexed_doc.keys():
                p += float(w_freq)*float(indexed_doc[w])
            norm_q += int(w_freq)^2
        if p != 0:
            norm_q = sqrt(norm_q)
            return float(float(p)/(norm_q*self.norm(doc_id, pond_type)))
        else:
            return 0

    def norm(self, doc_id, pond_type):
        n=0
        for w , freq in self.my_index.index[doc_id].iteritems():
            if pond_type == 'tf_idf':
                n+= freq^2
            elif pond_type == 'w':
                n+= freq^2
        return sqrt(float(n))

    def tf_log(self, tf):
        if tf>0:
            return 1+log10(tf)
        else:
            return 0

    def idf(self, df):
        return log10(float(int(self.my_index.N)/float(df)))

