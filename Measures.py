# -*- coding: utf-8 -*-

# Imports
# -------
from Index import Index
from Vect_query import Vect_query
from Query_set import Query_set
from Bool_query import Bool_query

# Class
# ------------------------------


class Measures:
    """
    Computes measures, mean, rappel and stuff

    """
    def __init__(self, index, query_set):
        self.set = query_set
        self.index = index

    def __str__(self):
        return str(self.aggregates_results())

    def aggregates_results(self):
        """ aggregates rappel and precision over all dataset """
        compared_res = {}
        for q_id in self.set.queries.keys():
            compared_res[q_id] = self.computes_measures(q_id)
        return compared_res

    def computes_measures(self, q_id):
        """ calculates rappel and precision for tf idf and simple vectoriel """
        query = self.set.queries[q_id]
        q_tf = Vect_query(query, self.index, 'tf_idf').results.keys()
        q_w = Vect_query(query, self.index, 'w').results.keys()
        q_set = self.set.results[str(q_id)]
        return {'w': self.rappel_precision(q_set, q_w), 'tf_idf': self.rappel_precision(q_set, q_tf)}

    def fn(self, q_set, q_res):
        """ false neg. Nb of element in q_set and not in q_res """
        return len(set(q_set).difference(q_res))

    def fp(self, q_set, q_res):
        """ false pos. Nb of element in q_res and not in q_set """
        return len(set(q_res).difference(q_set))

    def tp(self, q_set, q_res):
        """ true pos. Nb of element of q_res that are in q_set """
        return len(set(q_set).intersection(q_res))

    def rappel_precision(self, q_set, q_res):
        """ nb of relevant docs found compare to all relevant docs"""
        tp = self.tp(q_set, q_res)
        fn = self.fn(q_set, q_res)
        fp = self.fp(q_set, q_res)
        return {"rappel": float(tp)/float((tp+fn)), "precision": float(tp)/float((tp+fn))}


# Testing
# ------------------------------
if __name__ == "__main__":
    print 'hello'
