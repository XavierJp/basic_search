from Config import Config
from Index import Index
import re

# Class
# ------------------------------
class Raw_file:
    """
    Represent a Raw_file

    """

    def __init__(self, name, path, load_bool):
        self.my_name = name
        self.my_config = Config()
        self.index = Index()
        self.load_file(path, load_bool)

    def __str__(self):
        return my_dict

    def open_file(self, path):
        f = open(path,'r')
        data = f.read().splitlines()
        f.close()
        return data

    def load_file(self, path):
        lines = self.open_file(path)
        self.parse(lines)

    def parse(self, lines):
        doc_id = ''
        doc_mark = ''
        for i, l in enumerate(lines):
            if l[:3] == '.I ':
                doc_id = l[3:]
                doc_mark = '.I '
            else:
                if l[:2] in self.my_config.k_word:
                    doc_mark = l[:2]
                else:
                    if doc_mark in self.my_config.used_k_word:
                        self.tokenize(l, doc_id)

    def tokenize(self, str, doc_id):
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+",str)
        for e in reversed(range(0, len(wordsBuffer))):
            wordsBuffer[e] = wordsBuffer[e].lower()
            if self.compare(wordsBuffer[e]):
                wordsBuffer.pop(e)
            else:
                # doc_index
                self.add_to_index(self.index.doc_i, doc_id, wordsBuffer[e])
                # word_index
                self.add_to_index(self.index.word_i, wordsBuffer[e], doc_id)

    def add_to_index(self, index, key1, key2):
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
