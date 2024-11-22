import pickle

class CustomTokenizer:
    def __init__(self, oov_token="<UNK>"):
        self.word_to_id = {}
        self.id_to_word = {}
        self.oov_token = oov_token

        self.word_to_id[oov_token] = 0
        self.id_to_word[0] = oov_token

    def load(self, word_list):
        word_list = [word.lower() for word in word_list]
        next_id = max(self.word_to_id.values()) + 1

        for word in word_list:
            if word not in self.word_to_id:
                self.word_to_id[word] = next_id
                self.id_to_word[next_id] = word
                next_id += 1

    def encode(self, text):
        words = text.lower().split()  # Convert text to lowercase and split into words
        return [self.word_to_id.get(word, self.word_to_id[self.oov_token]) for word in words]

    def decode(self, ids):
        return ' '.join(self.id_to_word.get(i, self.oov_token) for i in ids)

    def export(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.word_to_id, self.id_to_word), f)

    def import_mappings(self, filename):
        with open(filename, 'rb') as f:
            self.word_to_id, self.id_to_word = pickle.load(f)
