# -*- coding: utf-8 -*-

# Imports
# -------
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
        """ transform the query from a string to a word index """
        query_index = defaultdict(int)
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+", query)
        for word in wordsBuffer:
            word = word.lower()
            if not self.compare(word):
                query_index[word] += 1
        return query_index

    def compare(self, element):
        """ compare a word to the list of meaningless word """
        if element in self.config.words:
            return True
        return False

    def execute_query(self, pond_type):
        """ execute the query search and return results """
        res_temp = defaultdict(int)

        # computes a ponderated vector for query
        query_vect = self.indexed_query
        for w in query_vect:
            if pond_type == 'tf_idf':
                if w in self.my_index.reversed_index:
                    tf = float(query_vect[w])
                    df = len(self.my_index.reversed_index[w])
                    N = float(self.my_index.N)
                    query_vect[w] = (1+log10(df))*log10((N)/df)
            elif w not in self.my_index.reversed_index:
                query_vect[w] = 0

        # computes a ponderated vector and computes cosinus
        doc_vect = defaultdict(dict)
        for word in self.indexed_query:
            if word in self.my_index.reversed_index:
                for doc_id in self.my_index.reversed_index[word]:
                    doc_vect[doc_id][word] = self.ponderation(word, doc_id, pond_type)
        for doc_id in doc_vect:
            cos = self.cosinus(query_vect, doc_vect[doc_id], doc_id, pond_type)
            res_temp[doc_id] = cos
        return res_temp

    def ponderation(self, word, doc_id, pond_type):
        """ 
            returns ponderation calculation
            either 'w' or 'tf-idf'
        """
        if pond_type == 'tf_idf':
            return float(self.tf_idf(word, doc_id))/float(self.max_tf_idf(doc_id))
        elif pond_type == 'w':
            tf = self.my_index.reversed_index[word][doc_id]
            max_tf = self.my_index.index[doc_id]["w_max"]
            return float(tf)/float(max_tf)

    def tf_idf(self, word, doc_id):
        df = len(self.my_index.reversed_index[word])
        tf = self.my_index.reversed_index[word][doc_id]
        return self.tf_log(tf)*self.idf(df)

    def max_tf_idf(self, doc_id):
        if 'max_tf_idf' in self.my_index.index[doc_id]:
            return self.my_index.index[doc_id]['max_tf_idf']
        else:
            max_tf_idf = 0
            for word in self.my_index.index[doc_id]:
                if word != 'w_max':
                    tf_idf = self.tf_idf(word, doc_id)
                    if tf_idf > max_tf_idf:
                        max_tf_idf = tf_idf
            self.my_index.index[doc_id]['max_tf_idf'] = max_tf_idf
            return max_tf_idf

    def cosinus(self, indexed_query, indexed_doc, doc_id, pond_type):
        """ computes cosinus calculation """
        p = 0
        norm_query = 0
        norm_doc = 0
        for w, w_freq in indexed_query.iteritems():
            if w in indexed_doc.keys():
                p += float(w_freq)*float(indexed_doc[w])
                norm_doc += pow(indexed_doc[w], 2)
            norm_query += pow(w_freq, 2)
        if p != 0:
            norm_query = sqrt(norm_query)
            norm_doc = sqrt(norm_doc)
            return float(float(p)/(norm_query*self.norm(indexed_doc, doc_id, pond_type)))
        else:
            return 0

    def norm(self, indexed_doc, doc_id, pond_type):
        if doc_id in self.my_index.norms[pond_type]:
            return self.my_index.norms[pond_type][doc_id]
        else:
            n = 0
            for w in self.my_index.reversed_index.keys():
                if w in indexed_doc.keys():
                    freq = self.ponderation(w, doc_id, pond_type)
                    n += pow(freq, 2)
            norm = sqrt(n)
            self.my_index.norms[pond_type][doc_id] = norm
            return norm

    def tf_log(self, tf):
        if tf > 0:
            return 1+log10(tf)
        else:
            return 0

    def idf(self, df):
        return log10(float(self.my_index.N)/float(df))
