# Class
# ------------------------------
class Config:
    """
    Represent all constant configuration informations

    """

    def __init__(self):
        self.common_words_path = 'cacm-2-/common_words'
        self.path = 'cacm-2-/cacm.all'
        self.k_word = ['.T','.W','.B','.A','.N','.X','.K']
        self.used_k_word = ['.T','.W','.K']
        self.words = self.common_words(self.common_words_path)

    def __str__(self):
        return 0

    def common_words(self, c_path):
        r = open(c_path,'r')
        words = r.read().splitlines()
        r.close()
        dict_w = {}
        for w in words:
            dict_w[w]=[]
        return dict_w
