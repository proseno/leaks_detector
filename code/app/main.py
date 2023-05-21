import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers


stop = set(stopwords.words("english"))


def main():
    # path_handler = PathHandler()
    df = pd.read_csv('/var/www/html/var/mysql/train/merged/merged_logs.csv')
    df["text"] = df.text.map(trim_datetime)
    df['text'] = df.text.map(remove_stopwords)

    counter = counter_word(df.text)
    num_unique_words = len(counter)

    # Split dataset into training and validation set
    train_size = int(df.shape[0] * 0.8)
    # TODO mix dataset because now it is sorted by target
    train_df = df[:train_size]
    val_df = df[train_size:]

    # split text and labels
    train_sentences = train_df.text.to_numpy()
    train_labels = train_df.target.to_numpy()
    val_sentences = val_df.text.to_numpy()
    val_labels = val_df.target.to_numpy()

    tokenizer = Tokenizer(num_words=num_unique_words)
    tokenizer.fit_on_texts(train_sentences)

    word_index = tokenizer.word_index

    train_sequences = tokenizer.texts_to_sequences(train_sentences)
    val_sequences = tokenizer.texts_to_sequences(val_sentences)

    max_length = 100

    train_padded = pad_sequences(train_sequences, maxlen=max_length, padding="post", truncating="post")
    val_padded = pad_sequences(val_sequences, maxlen=max_length, padding="post", truncating="post")

    reverse_word_index = dict([(idx, word) for (word, idx) in word_index.items()])

    model = keras.models.Sequential()
    model.add(layers.Embedding(num_unique_words, 32, input_length=max_length))

    model.add(layers.LSTM(64, dropout=0.1))
    model.add(layers.Dense(1, activation="sigmoid"))

    loss = keras.losses.BinaryCrossentropy(from_logits=False)
    optim = keras.optimizers.Adam(lr=0.001)
    metrics = ["accuracy"]

    model.compile(loss=loss, optimizer=optim, metrics=metrics)

    model.fit(train_padded, train_labels, epochs=20, validation_data=(val_padded, val_labels), verbose=2)

    predictions = model.predict(train_padded)
    predictions = [1 if p > 0.5 else 0 for p in predictions]

    print("Training Accuracy: {:.4f}".format(accuracy_score(train_labels, predictions)))


# TODO check what this shit do
def accuracy_score(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)


def decode(sequence, reverse_word_index):
    return " ".join([reverse_word_index.get(idx, "?") for idx in sequence])


def remove_stopwords(text):
    filtered_words = [word.lower() for word in text.split() if word.lower() not in stop]
    return " ".join(filtered_words)


def trim_datetime(text):
    pattern = r"\b(\d{4}-\d{2}-\d{2})t\d{2}:\d{2}:\d{2}\.\d{6}z"
    pattern2 = r"\b(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}\.\d{6}Z"
    result = re.sub(pattern, "", text)
    result = re.sub(pattern2, "", result)
    return result


def counter_word(text_col):
    count = Counter()
    for text in text_col.values:
        for word in text.split():
            count[word] += 1
    return count

main()
