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
from Bool_query import Bool_query
import operator

def execute_query(cacm_index, query_w):
    print('------------------------')
    r = raw_input("your query: ")
    tps_int2 = time.clock()
    if query_w == '3':
        result = Bool_query(r, cacm_index)
    elif query_w == '4':
        result = Vect_query(r, cacm_index)
    tps_fin = time.clock()
    
    print '------------------------'
    print "query executed in "+str((tps_fin - tps_int2))+" sec."
    print str(len(result.results))+" result(s) found. Only first ten are displayed."
    print '------------------------'

    n = 0
    for doc in reversed(sorted(result.results.items (), key = operator.itemgetter (1) )):
        if n < 10:
            n += 1
            print " - "+doc[0]+" : "+cacm_index.get_title_by_doc_id(doc[0],['.T'])
    tps_int1 = time.clock()


def main_loop():
    tps_debut = time.clock()
    #loading raw_file and creating index
    cacm_index = Index()


    tps_int1 = time.clock()
    print "cacm file loaded in "+str((tps_int1 - tps_debut))+" sec."
    print 'index size: ' + str(sys.getsizeof(str(cacm_index.reversed_index))/1000000) +' Mo'
    print '------------------------'
    print '\n'
    input_var = 'ini'
    while input_var != '0':
        input_var = raw_input('What do you want to do ? '+'\n'
            '\n'+'1: Search a document by docID'
            '\n'+'2: Look for documents a word belongs to'
            '\n'+'3: Execute a boolean query'
            '\n'+'4: Execute a Vectorial query Tf-idf'
            '\n'+'5: Execute a Vectorial query xxxx'
            '\n'+'6: Predefined query'
            '\n'+'0: Quitter'
            '\n'+'------------------------'+'\n'
            )

        if input_var == '1':
            input_doc_id = raw_input('Document ID you are looking for : ')
            print cacm_index.search_a_doc_id(input_doc_id)
        elif input_var == '2':
            input_word = raw_input('Word you are looking for : ')
            print cacm_index.search_a_word(input_word)
        elif input_var in ['2','6']:
            print 'coming soon...'
        elif input_var in ['3', '4']:
            execute_query(cacm_index, input_var)

main_loop()
