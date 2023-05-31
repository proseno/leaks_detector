import os.path
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class LogTokenizer:
    def __init__(self, num_words=0):
        self.tokenizer = None
        self.num_words = num_words
        if os.path.exists('/var/www/html/var/model/tokenizer/') is False:
            os.makedirs('/var/www/html/var/model/tokenizer')
        self.tokenizer_path = '/var/www/html/var/model/tokenizer/tokenizer.pickle'

    def fit(self, texts):
        self.tokenizer.fit_on_texts(texts)
        self.save_tokenizer()

    def get_sequence(self, texts):
        return self.tokenizer.texts_to_sequences(texts)

    def get_padded(self, texts, max_length=100):
        self.check()
        sequences = self.get_sequence(texts)
        return pad_sequences(
            sequences,
            maxlen=max_length,
            padding="post",
            truncating="post"
        )

    def save_tokenizer(self):
        with open(self.tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_tokenizer(self):
        if os.path.exists(self.tokenizer_path) is False:
            return False

        with open(self.tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)

        if isinstance(tokenizer, Tokenizer) is False:
            return False

        return tokenizer

    def set_default_tokenizer(self):
        self.tokenizer = Tokenizer(self.num_words)
        return self

    def set_tokenizer(self):
        if self.tokenizer is None:
            self.tokenizer = self.load_tokenizer()

        if self.tokenizer is False:
            raise RuntimeError('Tokenizer not found in ' + self.tokenizer_path + ". Please, run model training")
        return self.tokenizer

    def get(self):
        self.set_tokenizer()
        self.check()
        return self

    def check(self):
        if self.tokenizer is None:
            raise RuntimeError('Tokenizer is not defined. Try set_default_tokenizer() or set_tokenizer()')
