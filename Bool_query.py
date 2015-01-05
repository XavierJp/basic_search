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
        curr_w = ''
        for pos, word in enumerate(wordsBuffer):
            word = word.lower()
            if word in ['||', '<>','&&'] and pos > 0 and pos < len(wordsBuffer)-1:
                L_w.append(curr_w)
                L_w.append(word)
                curr_w = ''
            elif not self.compare(word):
                if len(curr_w) == 0:
                    curr_w = word
                else:
                    return []
        L_w.append(curr_w)
        return L_w

    def execute_query(self):
        query_list = self.indexed_query
        if len(query_list) < 3:
            return {}
        else:
            results_temp = self.get_results(query_list[0])
            for pos, l in enumerate(query_list):
                if l in ['||', '<>','&&']:
                    results_temp = self.compare_lists(results_temp, query_list[pos+1], l)
            result_dict = defaultdict(int)
            for r in results_temp:
                result_dict[r] += 1
            return result_dict
                

    def compare_lists(self, doc_list_a, word_b, logic):
        doc_list_b = self.get_results(word_b)
        if logic == '&&':
            return list(set(doc_list_a).intersection(doc_list_b))
        elif logic == '<>':
            return list(set(doc_list_a).difference(doc_list_b))
        elif logic == '||':
            return list(set(doc_list_a).union(doc_list_b))

    def get_results(self, word):
        if word in self.my_index.reversed_index.keys():
            return self.my_index.reversed_index[str(word)].keys()
        else:
            return []

    def compare(self, element):
        if element in self.config.words:
            return True
        return False
