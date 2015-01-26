# -*- coding: utf-8 -*-

# Imports
# -------
import re
import sys
import time
import os
from Config import Config
from Index import Index
from Vect_query import Vect_query
from Measures import Measures
from Query_set import Query_set
from Bool_query import Bool_query
from Probabilistic_query import Probabilistic_query
import operator


BOOL = "Please type your query like this : OR(A,AND(C,NOT(B))) :"
VECT = "Please type your query  :"

# clean shell
clear = lambda: os.system('clear')

def print_results(result, cacm_index, pos0):
    """ when called, print ten results """
    curr_pos = pos0 + 10
    for pos, doc in enumerate(reversed(sorted(result.results.items(), key=operator.itemgetter(1)))):
        if pos >= pos0 and pos < curr_pos:
            print " - "+doc[0]+" : "+cacm_index.get_title_by_doc_id(doc[0], ['.T'])
    return(- 1 if (curr_pos > len(result.results)) else curr_pos)


def query_input(string):
    print('------------------------')
    return raw_input(string)


def execute_query(cacm_index, q_set, input_var):
    """ when called, fetches and prints the results """

    tps_q_0 = time.clock()

    result = False

    if input_var == '1':
        input_doc_id = raw_input('Document ID you are looking for : ')
        print cacm_index.search_a_doc_id(input_doc_id)
    elif input_var == '2':
        input_word = raw_input('Word you are looking for : ')
        print cacm_index.search_a_word(input_word)
    elif input_var == '3':
        result = Bool_query(query_input(BOOL), cacm_index)
    elif input_var == '4':
        result = Vect_query(query_input(VECT), cacm_index, 'tf_idf')
    elif input_var == '5':
        result = Vect_query(query_input(VECT), cacm_index, 'w')
    elif input_var == '6':
        result = Probabilistic_query(query_input(VECT), cacm_index)
    elif input_var == '7':
        input_q_id = raw_input('Which query_id are you looking for? : ')
        print q_set.queries[input_q_id]
        result = Vect_query(q_set.queries[input_q_id], cacm_index, 'tf_idf')
    elif input_var == '8':
        input_q_id = raw_input('Which query_id are you looking for? : ')
        print q_set.queries[input_q_id]
        result = Vect_query(q_set.queries[input_q_id], cacm_index, 'w')
    elif input_var == '9':
        input_q_id = raw_input('Which query_id are you looking for? : ')
        print q_set.queries[input_q_id]
        result = Probabilistic_query(q_set.queries[input_q_id], cacm_index)
    elif input_var == '0':
        clear()
        Measures(cacm_index, q_set)
        tps_chart_fin = time.clock()
        print "Chart computed in "+"{:2.2f}".format(tps_chart_fin - tps_q_0)+" sec."

    tps_q_fin = time.clock()

    if result:
        clear()
        print '------------------------'
        print "query executed in "+"{:2.2f}".format(tps_q_fin - tps_q_0)+" sec."
        print str(len(result.results))+" result(s) found."
        if len(result.results) > 10:
            print "Only first ten results are being displayed."
        print '------------------------'

        curr_print_pos = 0
        keep_going = 'Y'
        while keep_going == 'Y':
            curr_print_pos = print_results(result, cacm_index, curr_print_pos)
            if curr_print_pos != -1:
                keep_going = raw_input('Would you like to diplay ten more? (Y/N): ')
                print '----------------------------------------'
            else:
                break

def main_loop():
    """ creates a basic user interface """
    tps_0 = time.clock()
    # loading raw_file and creating index & inversed index
    # ----------------------------------------------------
    print 'loading data...'
    cacm_index = Index()
    q_set = Query_set()

    # returning relevant infos : index size, loading time...
    # ------------------------------------------------------
    tps_index = time.clock()
    clear()
    print "cacm file loaded and analyzed in "+"{:2.3f}".format(tps_index - tps_0)+" sec."
    print 'reverted index size: ' + "{:2.2f}".format(float(sys.getsizeof(str(cacm_index.reversed_index)))/1000000)+ ' Mo'
    print 'index size: ' + "{:2.2f}".format(float(sys.getsizeof(str(cacm_index.index)))/1000000) + ' Mo'
    print '-----------------------------'
    print '\n'

    # choices
    # -------
    input_var = '0'
    while input_var in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        input_var = raw_input('What do you want to do now ? ' + '\n'
            '\n' + '1: Search a document by docID'
            '\n' + '2: Search for document where a word occurs'
            '\n' + '3: Execute a boolean query'
            '\n' + '4: Execute a Vectorial query (Tf-idf)'
            '\n' + '5: Execute a Vectorial query (simple vectorial model)'
            '\n' + '6: Execute a Probabilistic query (Binary Independence Retrieval)'
            '\n' + '7: Predefined query (Tf-idf)'
            '\n' + '8: Predefined query (simple vectorial model)'
            '\n' + '9: Predefined query (Binary Independence Retrieval)'
            '\n' + '0: Plot Rappel-precision chart'
            '\n' + 'ENTER: Stop'
            '\n' + '------------------------'+'\n'
            '|> ')
        if input_var in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            execute_query(cacm_index, q_set, input_var)
        else:
            break


# _____ MAIN LOOP _____
main_loop()
