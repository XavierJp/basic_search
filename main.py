import re
import time
from Config import Config
from Raw_file import Raw_file



tps_debut = time.clock()

file = Raw_file('cacm','cacm-2-/cacm.all')

tps_fin = time.clock()

print "temps d'exectution : "+str((tps_fin - tps_debut))+ " sec"
