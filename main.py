import re
import time
from Config import Config
from Index import Index
from Vect_query import Vect_query
from Bool_query import Bool_query
import operator

def execute_query(cacm_index, query_w):
    print('------------------------')
    r = raw_input("your query: ")
    tps_int2 = time.clock()
    if query_w == 'B':
        result = Bool_query(r, cacm_index)
    elif query_w == 'V':
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
            print " - "+doc[0]+" : "+cacm_index.raw_data.search_by_doc_id(doc[0],['.T'])
    tps_int1 = time.clock()


def main_loop():
    tps_debut = time.clock()
    #loading raw_file and creating index
    cacm_index = Index()

    tps_int1 = time.clock()
    print "cacm file loaded in "+str((tps_int1 - tps_debut))+" sec."

    stop = False
    while not stop:
        query_w = raw_input("Do you want to execute a Boolean or a Vectorial query? (V/B): ")
        if query_w in ['V', 'B']:
            execute_query(cacm_index, query_w)
        else: 
            print ('Mmmmh you have to type B or V...')

        stop_word = raw_input("Do you want to look for another document? (Y/N): ")

        if stop_word == 'Y':
            stop = False
        else:
            stop = True

main_loop()
