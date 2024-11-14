import pickle

class CustomTokenizer:
    def __init__(self, oov_token="<UNK>"):
        """
        Initializes the tokenizer with empty mappings and an OOV (out-of-vocabulary) token.
        """
        self.word_to_id = {}
        self.id_to_word = {}
        self.oov_token = oov_token

        self.word_to_id[oov_token] = 0
        self.id_to_word[0] = oov_token

    def load(self, word_list):
        """
        Dynamically loads a list of words into the tokenizer and assigns free IDs.

        Args:
            word_list (list of str): The list of words to add to the tokenizer.
        """
        # Ensure all words are lowercase
        word_list = [word.lower() for word in word_list]

        # Start assigning IDs from the current maximum ID + 1
        next_id = max(self.word_to_id.values()) + 1

        for word in word_list:
            if word not in self.word_to_id:
                self.word_to_id[word] = next_id
                self.id_to_word[next_id] = word
                next_id += 1

    def encode(self, text):
        """
        Encodes a string into a list of IDs.

        Args:
            text (str): The input text to encode.

        Returns:
            list of int: List of word IDs.
        """
        words = text.lower().split()  # Convert text to lowercase and split into words
        return [self.word_to_id.get(word, self.word_to_id[self.oov_token]) for word in words]

    def decode(self, ids):
        """
        Decodes a list of IDs into a string.

        Args:
            ids (list of int): List of word IDs to decode.

        Returns:
            str: The decoded string.
        """
        return ' '.join(self.id_to_word.get(i, self.oov_token) for i in ids)

    def export(self, filename):
        """
        Exports the word_to_id and id_to_word mappings to a binary file.

        Args:
            filename (str): The path of the file to save the mappings.
        """
        with open(filename, 'wb') as f:
            pickle.dump((self.word_to_id, self.id_to_word), f)

    def import_mappings(self, filename):
        """
        Loads word_to_id and id_to_word mappings from a binary file.

        Args:
            filename (str): The path of the file to load the mappings from.
        """
        with open(filename, 'rb') as f:
            self.word_to_id, self.id_to_word = pickle.load(f)
