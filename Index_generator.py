from Config import Config
from collections import defaultdict
import re

# Class
# ------------------------------
class Index_generator:
    """
    Generates an Index based on a Raw_file

    """

    def __init__(self):
        self.my_config = Config()
        self.doc_max_tf = {}
        self.word_doc_index = defaultdict(str)
        self.doc_word_index = defaultdict(str)
        self.my_dict = {}
        self.load_file(self.my_config.path)
        self.doc_number = len(self.doc_word_index.keys())

    def __str__(self):
        return my_dict

    def load_file(self, path):
        lines = self.open_file(path)
        self.make_index(lines)

    def open_file(self, path):
        f = open(path,'r')
        data = f.read().splitlines()
        f.close()
        return data

    def make_index(self, lines):
        doc_id = ''
        doc_mark = ''
        for i, l in enumerate(lines):
            if l[:3] == '.I ':
                doc_id = l[3:]
                doc_mark = '.I '
                self.my_dict[doc_id] = defaultdict(str)
            else:
                if l[:2] in self.my_config.k_word:
                    doc_mark = l[:2]
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
                self.populate_index(self.doc_word_index, doc_id, element)
                self.populate_index(self.word_doc_index, element, doc_id)


    def populate_index(self, index, key1, key2):
        if not key1 in index:
            index[key1] = defaultdict(int)
        index[key1][key2] += 1


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
