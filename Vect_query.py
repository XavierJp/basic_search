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
        """ trnasform the query from a string to a word index """
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

    def execute_query(self, ponderation):
        """ execute the query search and return results """
        res_temp = defaultdict(int)

        # computes a ponderated vector for query
        query_vect = defaultdict(dict)
        for w in self.indexed_query:
            if w in self.my_index.reversed_index:
                max_tf = max(self.indexed_query.iteritems(), key=operator.itemgetter(1))[1]
                df = self.my_index.reversed_index[w]['df']
                tf = self.indexed_query[w]
                query_vect[w] = self.ponderation(tf, df, max_tf, ponderation)

        # computes a ponderated vector and computes cosinus
        doc_vect = defaultdict(dict)
        for word in self.indexed_query:
            if word in self.my_index.reversed_index:
                for doc_id in self.my_index.reversed_index[word]:
                    if doc_id != 'df':
                        max_tf = self.max_tf(doc_id)
                        df = self.my_index.reversed_index[word]['df']
                        tf = self.my_index.reversed_index[word][doc_id]
                        doc_vect[doc_id][word] = self.ponderation(tf, df, max_tf, ponderation)
        for doc_id in doc_vect:
            cos = self.cosinus(query_vect, doc_vect[doc_id], doc_id, ponderation)
            res_temp[doc_id] = int(100*cos)
        return res_temp

    def max_tf(self, doc_id):
        """ computes the max tf amongst words in doc_id """
        return max(self.my_index.index[doc_id].iteritems(), key=operator.itemgetter(1))[1]

    def ponderation(self, tf, df, max_tf, pond_type):
        """ 
            returns ponderation calculation
            either 'w' or 'tf-idf'
        """
        if pond_type == 'tf_idf':
            return self.tf_log(tf)*self.idf(df)
        elif pond_type == 'w':
            return float(tf)/float(max_tf)

    def cosinus(self, indexed_query, indexed_doc, doc_id, pond_type):
        """ computes cosinus calculation """
        p = 0
        norm_query = 0
        for w, w_freq in indexed_query.iteritems():
            if w in indexed_doc.keys():
                p += float(w_freq)*float(indexed_doc[w])
            norm_query += pow(w_freq, 2)
        if p != 0:
            norm_query = sqrt(norm_query)
            return float(float(p)/(norm_query*self.norm_doc_vect(doc_id, pond_type)))
        else:
            return 0

    def norm_doc_vect(self, doc_id, pond_type):
        """ computes norm """
        n = 0
        for w, freq in self.my_index.index[doc_id].iteritems():
            if pond_type == 'tf_idf':
                df = self.my_index.reversed_index[w]['df']
                tf = freq
                tf_idf = self.tf_log(tf)*self.idf(df)
                n += pow(tf_idf, 2)
            elif pond_type == 'w':
                w = freq/self.max_tf(doc_id)
                n += pow(w, 2)
        return sqrt(float(n))

    def tf_log(self, tf):
        if tf > 0:
            return 1+log10(tf)
        else:
            return 0

    def idf(self, df):
        return log10(float(int(self.my_index.N))/float(df))
