import re
import time
from Config import Config
from Index import Index
from Vect_query import Vect_query
import operator

tps_debut = time.clock()

cacm_index = Index()

tps_int1 = time.clock()
print "cacm file loaded in "+str((tps_int1 - tps_debut))+" sec."

r = raw_input("your query: ")
tps_int2 = time.clock()
result = Vect_query("walk on the wild side", cacm_index)
tps_fin = time.clock()

print '------------------------'
print "query executed in "+str((tps_fin - tps_int2))+" sec."
print str(len(result.results))+" result(s) found."
print '------------------------'
for doc in reversed(sorted(result.results.items (), key = operator.itemgetter (1) )):
    print " - "+doc[0]+" : "+cacm_index.raw_data.search_by_doc_id(doc[0],['.T'])
tps_int1 = time.clock()
