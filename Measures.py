# -*- coding: utf-8 -*-

# Imports
# -------
from Index import Index
import os
from Vect_query import Vect_query
from Query_set import Query_set
from Bool_query import Bool_query
from Probabilistic_query import Probabilistic_query
import matplotlib.pyplot as plt

# Class
# ------------------------------


class Measures:
    """
    Computes measures, mean, rappel and stuff

    """
    def __init__(self, index, query_set):
        self.set = query_set
        self.index = index
        self.measures_dict = self.aggregates_results()
        self.plot_rappel_precision(self.measures_dict)

    def __str__(self):
        return str(self.aggregates_results())

    def aggregates_results(self):
        """ aggregates rappel and precision over all dataset """
        # clean shell
        clear = lambda: os.system('clear')
        res = {}

        for pond in ['w', 'tf_idf', 'proba']:

            coordinates = []
            count = 0
            local_coords = []
            for q_id in xrange(1, 65):
                clear()
                print '|> processing query number '+str(q_id)+' out of 64'+' ['+pond+']'

                if len(self.set.results[str(q_id)]):
                    measures = self.compute_measures(str(q_id), pond)
                    local_coords = self.interpolate(measures)
                    count += 1

                    if len(coordinates) == 0:
                        coordinates = local_coords
                    else:
                        for j in xrange(0, len(coordinates)):
                            coordinates[j] += local_coords[j]
            # ponderation
            for j in xrange(0, 11):
                coordinates[j] = coordinates[j] / count

            res[pond] = coordinates

        return res

    def interpolate(self, coords):
        """ curve interpolation """
        interpolated_coords = []
        # 11 levels of recall
        for i_rec in xrange(0, 11):
            precision = 0

            for j in xrange(0, len(coords)):

                if coords[j][0] >= i_rec * 10 and coords[j][1] > precision:
                    precision = coords[j][1]

            if precision == 0 and i_rec > 0:
                precision = interpolated_coords[-1]

            # add i-eme level of recall, with highest precision
            interpolated_coords.append(precision)
        return interpolated_coords

    def compute_measures(self, q_id, pond):
        """ calculates rappel and precision for tf idf and simple vectoriel """
        # correct result
        q_set = self.set.results[str(q_id)]

        # query
        query = self.set.queries[q_id]

        # r_k results for simple vectorial and tf_idf
        if pond in ['tf_idf', 'w']:
            q = Vect_query(query, self.index, pond).results
        elif pond == 'proba':
            q = Probabilistic_query(query, self.index).results

        q = self.sorted_keys(q)

        r = []
        # computes recall-precision for both simmple vect and tf for all rank
        for i in xrange(1, len(q)):
            r.append(self.rappel_precision(q_set, q[:i], i))

        return r

    def sorted_keys(self, dict_to_order):
        return sorted(dict_to_order, key=dict_to_order.get, reverse=True)

    def tp(self, q_set, q_res):
        """ true pos. Nb of element of q_res that are in q_set """
        return len(set(q_set).intersection(q_res))

    def rappel_precision(self, q_set, q_res, r_k):
        """ Rappel : nb of relevant docs found compare to all relevant docs
            Precision : nb of relevant docs found compare to docs actually found
        """
        tp = self.tp(q_set, q_res)

        # recall & precision rank_k
        recall_K = 100 * tp / len(q_set)
        precision_K = 100 * tp / r_k

        return [recall_K, precision_K]

    def plot_rappel_precision(self, rappel_precision):
        """ plot with matpotlib """
        rappel_11 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        precision_w = self.measures_dict['w']
        precision_tf = self.measures_dict['tf_idf']
        precision_proba = self.measures_dict['proba']

        plt.plot(rappel_11, precision_w, label='Simple')
        plt.plot(rappel_11, precision_tf, label='tf-idf')
        plt.plot(rappel_11, precision_proba, label='Probabilistic')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
        plt.ylabel("Precision")
        plt.xlabel("Rappel")
        plt.axis([0, 100, 0, 65])
        plt.grid(True)
        plt.savefig('./resources/Precision-Rappel.png', format='png')
        print 'Curve has been saved in resources folder.'
        print '\n'+'Mean Average Precision'
        print '----------------------'
        print 'Simple vector model: '+"{:2.2f}".format(self.MAP(precision_w))
        print 'Tf-idf model: '+"{:2.2f}".format(self.MAP(precision_tf))
        print 'Probabilistic model: '+"{:2.2f}".format(self.MAP(precision_proba))

    def MAP(self, l):
        m = 0
        n = len(l)
        for i in l:
            m += i
        return float(m)/(100*n)

# Testing
# ------------------------------
if __name__ == "__main__":
    print 'hello'
