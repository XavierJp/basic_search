# -*- coding: utf-8 -*-

# Imports
# -------
from Config import Config
import re
from abc import ABCMeta, abstractmethod
# Class
# ------------------------------

class Query:
    """
    Represent a query - Abstract class. Two inherited class : Boolean and Vectorial query

    """
    __metaclass__ = ABCMeta

    def __init__(self, query, index):
        self.my_index = index
        self.config = Config()
        self.indexed_query = self.indexize(query)
        self.results = self.execute_query()

    def __str__(self):
        return results

    @abstractmethod
    def indexize(self, query):
        pass

    @abstractmethod
    def execute_query(self):
        pass

    def compare(self, element):
        if element in self.config.words:
            return True
        return False
