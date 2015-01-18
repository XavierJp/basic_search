# -*- coding: utf-8 -*-

# Imports
# -------
import os
from collections import defaultdict

# Class
# ------------------------------
class Query_set:
	"""
	Loads a set of predefined queries and their results

	"""
	def __init__(self):
		self.queries = self.get_queries()
		self.results = self.get_rels()

	def __str__(self):
		return queries

	def load_file(self, path):
		""" open file and copy it into a string """
		raw_file = open(path, 'r')
		content = raw_file.read().splitlines()
		raw_file.close()
		return content

	def get_queries(self):
		queries = self.load_file('cacm-2-/query.text')
		query_index =defaultdict(str)
		for pos, l in enumerate(queries):
			if l[:2] == '.I':
				q_id = l[3:]
				p = pos +1
				if queries[p][:2] == '.W':
					W = True
					p +=1
					while W:
						query_index[q_id] += queries[p]
						p +=1
						if queries[p][:2] in ['.A', '.C', '.N']:
							W = False
		return query_index

	def get_rels(self):
		res = self.load_file('cacm-2-/qrels.text')
		rel_index = defaultdict(list)
		for l in res:
			q_id = int(l[:2])
			res_temp = str(int(l[3:7]))
			rel_index[q_id].append(res_temp)
		return rel_index


# Testing
# ------------------------------
if __name__ == "__main__":
	q = Query_set()
	print q.queries.keys()
	print q.get_rels()
    #os.system("pause")