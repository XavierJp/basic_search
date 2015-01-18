# -*- coding: utf-8 -*-

# Imports
# -------
from Config import Config
from Query import Query
from collections import defaultdict
import re
import ast

# Class
# ------------------------------

class Bool_query(Query):
    """
    Represent a query

    """

    def indexize(self, query):
        """ tokenize query and turn it into an index or a tree """
        return query

    def execute_query(self):
        res_temp = self.reccur_analysis(self.indexed_query)
        results = {}
        for r in res_temp:
            results[r] = 1
        return results
        
    def reccur_analysis(self, q_str):
        if q_str[:3]=='AND':
            if '(' in q_str[3:]:
                q = self.split_str(q_str[3:])
                return self.call_compare_lists(q[0], q[1], 0)
            else: 
                q = q_str[3:].split(',')
                return self.call_compare_lists(q[0], q[1], 0)
        elif q_str[:2]=='OR':
            if '(' in q_str[2:]:
                q = self.split_str(q_str[2:])
                return self.call_compare_lists(q[0], q[1], 1)
            else: 
                q = q_str[2:].split(',')
                return self.call_compare_lists(q[0], q[1], 1)
        elif q_str[:3]=='NOT':
            if '(' in q_str[3:]:
                res = self.reccur_analysis(q_str[3:])
            else: 
                q_str = q_str.lower()
                res = self.get_results(q_str)
            res.append('!')
            return res                
        else:
            q_str = q_str.lower()
            return self.get_results(q_str)

    def call_compare_lists(self, elmnt1, elmnt2, k):
        return self.compare_lists(self.reccur_analysis(elmnt1), self.reccur_analysis(elmnt2), k)

    def split_str(self, entire_str):
        entire_str = entire_str[1:len(entire_str)-1]
        parenthesis = []
        for pos in xrange(0,len(entire_str)):
            if entire_str[pos] in ['(', ')', ',']:
                parenthesis.append([entire_str[pos],pos])
        pos = self.analize_structure(parenthesis)
        return [entire_str[:pos], entire_str[pos+1:]]

    def analize_structure(self, struct_list):
        temp_list = struct_list
        pos = len(struct_list)-1
        while pos !=0:
            if struct_list[pos][0] == ')':
                if struct_list[pos-1][0] == '(':
                    del temp_list[pos-1:pos+1]
                    pos = len(temp_list)-1
                elif struct_list[pos-2][0] == '(' and struct_list[pos-1][0] == ',':
                    del temp_list[pos-2:pos+1]
                    pos = len(temp_list)-1
                else:
                    pos = pos -1
            else:
                pos = pos -1
        return temp_list[0][1]

    def compare_lists(self, doc_list_a, doc_list_b, logic):
        if logic == 0:
            if doc_list_b[-1]=='!' and len(doc_list_b) > 0:
                temp_res = list(set(doc_list_a).difference(doc_list_b[-1:]))
            elif doc_list_a[-1]=='!' and len(doc_list_a) > 0:
                temp_res = list(set(doc_list_b).difference(doc_list_a[-1:]))
            else:
                temp_res = list(set(doc_list_a).intersection(doc_list_b))
        else:
            if doc_list_b[-1]=='!' and len(doc_list_b) > 0:
                temp_res = doc_list_a
            elif doc_list_a[-1]=='!' and len(doc_list_a) > 0:
                temp_res = doc_list_b
            else:
                temp_res = list(set(doc_list_b).union(doc_list_a))
        return temp_res

        

    def get_results(self, word):
        if word in self.my_index.reversed_index.keys():
            res = self.my_index.reversed_index[str(word)].keys()
            if 'df' in res:
                res.remove('df')
            return res
        else:
            return []

