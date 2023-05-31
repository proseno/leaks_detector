import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import pandas as pd
from collections import Counter
from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
from cleaner import Cleaner
from tokenizer import LogTokenizer
from tensorflow.keras.preprocessing.text import Tokenizer



def main():
    cleaner = Cleaner()
    log_model = LogModel(cleaner)

    log_model.clean_df()

    model = log_model.init_model()

    # train_sentences, train_labels = log_model.get_train()
    # log_tokenizer = LogTokenizer(Tokenizer(num_words=log_model.get_num_unique_words()))
    # log_tokenizer.fit(train_sentences)
    # train_padded = log_tokenizer.get_padded(train_sentences, 200)

    # predictions = model.predict(train_padded)
    # predictions = [1 if p > 0.5 else 0 for p in predictions]
    #
    # print(train_sentences[10:20])
    # print(train_labels[10:20])
    # print(predictions[10:20])


class LogModel:
    def __init__(self, cleaner: Cleaner):
        # TODO file name could be with timestamp, change to parameter
        self.df = pd.read_csv('/var/www/html/var/mysql/train/merged/merged_logs.csv')
        self.cleaner = cleaner
        self.train_size = int(self.df.shape[0] * 0.8)
        self.max_length = 200
        self.model = None

    def clean_df(self):
        self.df["text"] = self.df.text.map(self.cleaner.trim_datetime)
        self.df["text"] = self.df.text.map(self.cleaner.remove_stopwords)

    def get_num_unique_words(self):
        count = Counter()
        for text in self.df.text.values:
            for word in text.split():
                count[word] += 1
        return len(count)

    def get_train(self):
        # return tuple with sentences and labels
        train_df = self.df[:self.train_size]
        return train_df.text.to_numpy(), train_df.target.to_numpy()

    def get_val(self):
        # return tuple with sentences and labels
        val_df = self.df[self.train_size:]
        return val_df.text.to_numpy(), val_df.target.to_numpy()

    def get_model(self):
        if self.model is None:
            model = tf.keras.models.load_model('/var/www/html/var/model')
            if isinstance(model, keras.models.Sequential):
                self.model = model
            else:
                raise RuntimeError(
                    'Model is not Sequential. Something went wrong when loading model. Please, re-train model'
                )

        return self.model

    def init_model(self):
        # differentiate between train and validation
        train_sentences, train_labels = self.get_train()
        val_sentences, val_labels = self.get_val()

        # tokenizer training
        log_tokenizer = LogTokenizer(self.get_num_unique_words()).set_default_tokenizer()
        log_tokenizer.fit(train_sentences)

        # preprocessing data for training
        train_padded = log_tokenizer.get_padded(train_sentences, self.max_length)
        val_padded = log_tokenizer.get_padded(val_sentences, self.max_length)

        # model initialization
        model = keras.models.Sequential()
        model.add(layers.Embedding(self.get_num_unique_words(), 32, input_length=self.max_length))

        model.add(layers.LSTM(64, dropout=0.1))
        model.add(layers.Dense(1, activation="sigmoid"))

        loss = keras.losses.BinaryCrossentropy(from_logits=False)
        optim = keras.optimizers.Adam(lr=0.001)
        metrics = ["accuracy", tf.keras.metrics.Recall(), tf.keras.metrics.Precision()]

        model.compile(loss=loss, optimizer=optim, metrics=metrics)

        # model training
        model.fit(train_padded, train_labels, epochs=20, validation_data=(val_padded, val_labels), verbose=2)

        # model saving
        model.save('/var/www/html/var/model')

        return log_tokenizer, model
#
#
# main()
