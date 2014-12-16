from Query import Query
from math import sqrt, log
# Class
# ------------------------------
class Index:
    """
    Represent an Index

    """

    def __init__(self):
        self.doc_i = {}
        self.word_i = {}
        self.words_space = []

    def __str__(self):
        return self.doc_i, self.word_i

    #frequence normalise. You can use either w_normalized() or tf_idf() in the cos()
    def w_normalized(self, word, doc_id):
        indexed_doc = self.doc_i[doc_id]
        w = indexed_doc[word]
        w_max = 0
        for m in indexed_doc:
            if indexed_doc[m] > w_max: w_max = indexed_doc[m]
        return float(w)/float(w_max)

    #tf_idf
    def tf_idf(self, word, doc_id):
        return self.tf(word, doc_id)*self.idf(word)

    #Log(inverse de la proportion de documents qui contiennent le terme)
    def idf(self, word):
        a = 0
        for d in self.word_i[str(word)]: a += int(d)
        N = len(self.doc_i.keys())
        return log(float(N)/float(a))

    # Nb occurrences de ce terme dans le document
    def tf(self, word, doc_id):
        if str(word) in self.doc_i[str(doc_id)]:
            a = self.doc_i[str(doc_id)][str(word)]
            if a >0: return 1 + log(a)
        return 0

    #project query_vector over every doc_vector
    def project_on_space(self, vect):
        vectors_list={}
        #boucle sur chaque document
        for doc_id in self.doc_i.keys():
            #cosinus(vecteur-requete,vecteur-document_courant)
            c = self.cosinus(vect, doc_id)
            if c:
                vectors_list[doc_id] = c
        return vectors_list

    #create a new query and project it on document_vectors
    def new_query(self, query):
        q = Query(query)
        results = self.project_on_space(q.indexed_query)
        q.results = results
        return results

    #calculates cosinus between two vectors of w_space
    def cosinus(self, indexed_query, doc_id):
        p = 0
        n = 0
        for w in indexed_query.keys():
            if w in self.doc_i[doc_id]:
                p += float(indexed_query[w])*float(self.tf_idf(w,doc_id))
            n += int(indexed_query[w])*int(indexed_query[w])
        if p != 0:
            n = sqrt(n)
            return float(float(p)/(n*self.norm(self.doc_i[doc_id])))
        else:
            return 0

    def norm(self, vect):
        n=0
        for val in vect.keys():
            n += int(vect[val])*int(vect[val])
        return sqrt(float(n))
