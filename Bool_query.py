from Config import Config
from Query import Query
from collections import defaultdict
import re

# Class
# ------------------------------

class Bool_query(Query):
    """
    Represent a query

    """

    def indexize(self, query):
        query_index = {}
        wordsBuffer = re.findall(r"[a-zA-Z0-9&|<>]+",query)
        L_w = []
        curr_list = []
        for pos, word in enumerate(wordsBuffer):
            word = word.lower()
            if word in ['||', '<>','&&'] and pos > 0 and pos < len(wordsBuffer)-1:
                L_w.append(curr_list)
                L_w.append(word)
                curr_list = []
            elif not self.compare(word):
                curr_list.append(word)
        L_w.append(curr_list)
        return L_w

    def execute_query(self):
        query_list = self.indexed_query
        results_temp = [query_list[0]]
        for pos, l in enumerate(query_list):
            if l in ['||', '<>','&&']:
                results_temp = self.compare_list(results_temp[-1], query_list[pos+1], l)
        result_dict = defaultdict(int)
        for r in results_temp:
            result_dict[r] += 1
        return result_dict
                

    def compare_list(self, word_list_a, word_list_b, logic):
        A = self.get_results(word_list_a)
        B = self.get_results(word_list_b)
        if logic == '&&':
            return list(set(A).intersection(B))
        elif logic == '<>':
            return list(set(A).difference(B))
        elif logic == '||':
            return list(set(A).union(B))

    def get_results(self, A):
        results = []
        for w in A:
            results = list(set(results).union(self.get_docs(w)))
        return results

    def get_docs(self, word):
        return self.my_index.reversed_index[str(word)].keys()

    def compare(self, element):
        if element in self.config.words:
            return True
        return False
