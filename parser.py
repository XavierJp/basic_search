import re
import time

tps_debut = time.clock()

common_wordsPath = 'cacm-2-/common_words'
cacmPath = 'cacm-2-/cacm.all'
k_word = ['.T','.W','.B','.A','.N','.X','.K']
used_k_word = ['.T','.W','.K']

f = open(cacmPath,'r')
lines = f.read().splitlines()
f.close()

r = open(common_wordsPath,'r')
words = r.read().splitlines()
r.close()

index = {}

def parse(lines):
  d_dict={}
  doc_id = ''
  doc_mark = ''
  for i, l in enumerate(lines):
    if l[:3] == '.I ':
      doc_id = l[3:]
      index[doc_id]={}
      doc_mark = '.I '
      d_dict[doc_id] = {}
    else:
      if l[:2] in k_word:
        doc_mark = l[:2]
        d_dict[doc_id][doc_mark] = []
      else:
        if doc_mark in used_k_word:
          tokenized_l = tokenize(l, doc_id)
          for t in tokenized_l:
            d_dict[doc_id][doc_mark].append(t)
        else:
          d_dict[doc_id][doc_mark].append(l)
  return d_dict

def tokenize(str, doc_id):
  split_str = re.split('[-*$(),;/:. ]',str)
  for e in reversed(range(0, len(split_str))):
    if len(split_str[e])==0 or compare(split_str[e]):
      split_str.pop(e)
    else:
      split_str[e] = split_str[e].lower()
      if split_str[e] in index[doc_id]:
        index[doc_id][split_str[e]] += 1
      else:
        index[doc_id][split_str[e]] = 1
  return split_str

def compare(element):
  if element.lower() in words:
    return True
  return False

def reverse_index(m_dict):
  rev_dict = {}
  for k in m_dict:
    for word in m_dict[k]:
        if not word in rev_dict:
          rev_dict[word] = {}
        rev_dict[word][k] = {}
        rev_dict[word][k] = m_dict[k][word]
  return rev_dict

parse(lines)
#print reverse_index(index)
tps_fin = time.clock()
print "temps d'exectution : "+str((tps_fin - tps_debut))+ " sec"
