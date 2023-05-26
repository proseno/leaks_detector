from tokenizer import LogTokenizer
from cleaner import Cleaner
import numpy
import pandas as pd
from io import StringIO
import os
import csv


class Transformer:
    def __init__(self, log_tokenizer: LogTokenizer):
        self.tokenizer = log_tokenizer
        self.cleaner = Cleaner()

    def transform(self, text):
        df = self.convert_to_data_frame(text)
        df["text"] = df.text.map(self.cleaner.trim_datetime)
        df["text"] = df.text.map(self.cleaner.remove_stopwords)
        return self.tokenizer.get_padded(df.text.to_numpy(), 200)

    @staticmethod
    def convert_to_data_frame(text: str):
        path = '/var/www/html/var/tmp/data_tmp.csv'
        with open(os.path.join(path), 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['text'])
            csv_writer.writerow([text])
        df = pd.read_csv(path)
        os.remove(path)
        return df
