import re
import nltk
from nltk.corpus import stopwords


class Cleaner:
    def __init__(self):
        nltk.download('stopwords')
        self.stop = set(stopwords.words("english"))

    @staticmethod
    def trim_datetime(text: str):
        pattern = r"\b(\d{4}-\d{2}-\d{2})t\d{2}:\d{2}:\d{2}\.\d{6}z"
        pattern2 = r"\b(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}\.\d{6}Z"
        result = re.sub(pattern, "", text)
        result = re.sub(pattern2, "", result)
        return result

    def remove_stopwords(self, text: str):
        filtered_words = [word.lower() for word in text.split() if word.lower() not in self.stop]
        return " ".join(filtered_words)
