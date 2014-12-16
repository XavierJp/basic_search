from Config import Config
import re
from abc import ABCMeta, abstractmethod
# Class
# ------------------------------

class Query:
    """
    Represent a query - Abstract class

    """
    __metaclass__ = ABCMeta

    def __init__(self, query, index):
        self.my_index = index
        self.my_query = query
        self.config = Config()
        self.indexed_query = self.indexize(query)
        self.results = self.project_index()


    @abstractmethod
    def indexize(self, query):
        pass

    def compare(self, element):
        if element in self.config.words:
            return True
        return False
