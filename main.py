import re
import time
from Config import Config
from Index_generator import Index_generator
from Query import Query
import operator

tps_debut = time.clock()

cacm = Index_generator()

tps_int1 = time.clock()
print "cacm file loaded: "+str((tps_int1 - tps_debut))+" sec."

r = raw_input("your query: ")
tps_int2 = time.clock()
result = cacm.index.new_query(r)
tps_fin = time.clock()

print '------------------------'
print "query executed in: "+str((tps_fin - tps_int2))+" sec."
print str(len(result))+" result(s) found."
print '------------------------'
for doc in reversed(sorted(result.items (), key = operator.itemgetter (1) )):
    print " - "+doc[0]+" : "+cacm.search_by_doc_id(doc[0],['.T'])
