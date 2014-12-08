# Class
# ------------------------------
class Index:
    """
    Represent an Index

    """

    def __init__(self):
        self.doc_i = {}
        self.word_i = {}

    def __str__(self):
        return doc_i, word_i

    def search_w(self, word):
        return self.word_i[word]

    def search_d(self, doc):
        return self.doc_i[doc]
