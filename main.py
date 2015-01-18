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

def execute_query(cacm_index, input_var):
    print('------------------------')
    r = raw_input("your query: ")
    tps_int2 = time.clock()

    if input_var == '1':
        input_doc_id = raw_input('Document ID you are looking for : ')
        print cacm_index.search_a_doc_id(input_doc_id)
    elif input_var == '2':
        input_word = raw_input('Word you are looking for : ')
        print cacm_index.search_a_word(input_word)
    elif input_var == '3':
        result = Bool_query(r, cacm_index)
    elif input_var == '4':
        result = Vect_query(r, cacm_index, 'tf_idf')
    elif input_var == '5':      
        result = Vect_query(r, cacm_index, 'w')
    elif input_var in ['6']:
        print 'coming soon...'
    tps_fin = time.clock()
    elif input_var == '0':
        return '0'
    
    if result:
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

    return '8'

def main_loop():
    tps_debut = time.clock()
    #loading raw_file and creating index
    cacm_index = Index()


    tps_int1 = time.clock()
    print "cacm file loaded in "+str((tps_int1 - tps_debut))+" sec."
    print 'index size: ' + str(sys.getsizeof(str(cacm_index.reversed_index))/1000000) +' Mo'
    print '------------------------'
    print '\n'
    loop = 'ini'
    while loop != '0':
        input_var = raw_input('What do you want to do ? '+'\n'
            '\n'+'1: Search a document by docID'
            '\n'+'2: Look for documents a word belongs to'
            '\n'+'3: Execute a boolean query'
            '\n'+'4: Execute a Vectorial query (Tf-idf)'
            '\n'+'5: Execute a Vectorial query (w)'
            '\n'+'6: Predefined query'
            '\n'+'0: Quitter'
            '\n'+'------------------------'+'\n'
            )
        loop = execute_query(cacm_index, input_var)



# _____ MAIN LOOP _____        
main_loop()
