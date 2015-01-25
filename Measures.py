# -*- coding: utf-8 -*-

# Imports
# -------
from Index import Index
import os
from Vect_query import Vect_query
from Query_set import Query_set
from Bool_query import Bool_query
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
        coordinates_w = []
        coordinates_tf = []
        count = 0
        local_coords = []
        for q_id in xrange(1, 65):
            clear()
            print '|> processing query number '+str(q_id)+' out of 64'

            if len(self.set.results[str(q_id)]):
                measures = self.compute_measures(str(q_id))
                local_coords_w = self.interpolate(measures['w'])
                local_coords_tf = self.interpolate(measures['tf_idf'])
                count += 1

                if len(coordinates_w) == 0:
                    coordinates_w = local_coords_w
                else:
                    for j in xrange(0, len(coordinates_w)):
                        coordinates_w[j] += local_coords_w[j]

                if len(coordinates_tf) == 0:
                    coordinates_tf = local_coords_tf
                else:
                    for j in xrange(0, len(coordinates_tf)):
                        coordinates_tf[j] += local_coords_tf[j]

        # ponderation
        for j in xrange(0, 11):
            coordinates_w[j] = coordinates_w[j] / count
            coordinates_tf[j] = coordinates_tf[j] / count
        return {"w": coordinates_w, "tf_idf": coordinates_tf}

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

    def compute_measures(self, q_id):
        """ calculates rappel and precision for tf idf and simple vectoriel """
        # correct result
        q_set = self.set.results[str(q_id)]

        # query
        query = self.set.queries[q_id]

        # r_k results for simple vectorial and tf_idf
        q_tf = Vect_query(query, self.index, 'tf_idf').results
        q_tf = self.sorted_keys(q_tf)
        q_w = Vect_query(query, self.index, 'w').results
        q_w = self.sorted_keys(q_w)

        r_p_w = []
        r_p_tf_idf = []
        # computes recall-precision for both simmple vect and tf for all rank
        for i in xrange(1, len(q_w)):
            r_p_w.append(self.rappel_precision(q_set, q_w[:i], i))

        for j in xrange(1, len(q_tf)):
            r_p_tf_idf.append(self.rappel_precision(q_set, q_tf[:j], j))

        return {'w': r_p_w, 'tf_idf': r_p_tf_idf}

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

        plt.plot(rappel_11, precision_w, label='Simple vectorial ponderation')
        plt.plot(rappel_11, precision_tf, label='tf-idf ponderation')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
        plt.ylabel("Rappel")
        plt.xlabel("Precision")
        plt.axis([0, 100, 0, 100])
        plt.grid(True)
        plt.savefig('./resources/Precision-Rappel.png', format='png')
        print 'Curve has been saved in resources folder.'

# Testing
# ------------------------------
if __name__ == "__main__":
    print 'hello'
