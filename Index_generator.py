from Config import Config
from Index import Index
import re

# Class
# ------------------------------
class Index_generator:
    """
    Represent a Raw_file

    """

    def __init__(self):
        self.my_config = Config()
        self.index = Index()
        self.my_dict = {}
        self.load_file(self.my_config.path)

    def __str__(self):
        return my_dict

    def open_file(self, path):
        f = open(path,'r')
        data = f.read().splitlines()
        f.close()
        return data

    def load_file(self, path):
        lines = self.open_file(path)
        self.make_index(lines)

    def make_index(self, lines):
        doc_id = ''
        doc_mark = ''
        for i, l in enumerate(lines):
            if l[:3] == '.I ':
                doc_id = l[3:]
                doc_mark = '.I '
                self.my_dict[doc_id] = {}
            else:
                if l[:2] in self.my_config.k_word:
                    doc_mark = l[:2]
                    if doc_mark in self.my_config.used_k_word:
                        self.my_dict[doc_id][doc_mark] = ""
                else:
                    if doc_mark in self.my_config.used_k_word:
                        self.tokenize(l, doc_id)
                        self.my_dict[doc_id][doc_mark] += l

    def tokenize(self, str, doc_id):
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+",str)
        for element in wordsBuffer:
            element = element.lower()
            if not self.compare(element):
                # populate doc_index
                self.populate_index(self.index.doc_i, doc_id, element)
                # populate word_index
                self.populate_index(self.index.word_i, element, doc_id)

    def populate_index(self, index, key1, key2):
        if not key1 in index:
            index[key1]={}
        if key2 in index[key1]:
            index[key1][key2] += 1
        else:
            index[key1][key2] = 1

    def compare(self, element):
        if element in self.my_config.words:
            return True
        return False

    def search_by_doc_id(self, doc_id,k_words):
        if doc_id in self.my_dict:
            for k in k_words:
                if k in self.my_dict[doc_id]:
                    return self.my_dict[doc_id][k]
                else:
                    return ""
        else:
            return "Sorry, there is no :"+doc_id+" document"
