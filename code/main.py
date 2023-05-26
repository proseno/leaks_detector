import sys
sys.path.append('train')

from train.transformer import Transformer
from train.tokenizer import LogTokenizer
from train.trainer import LogModel
from train.cleaner import Cleaner
from app.loader import Log
from app.mail_provider import Sender


def main():
    tokenizer = LogTokenizer().get()
    cleaner = Cleaner()
    model = LogModel(cleaner).get_model()
    transformer = Transformer(tokenizer)
    sender = Sender()
    log = Log()

    additional_text = ''
    data = log.get_data()
    for text in data:
        data_to_analyze = transformer.transform(text)
        prediction = model.predict(data_to_analyze)
        if prediction > 0.9:
            additional_text += '-----------------------------------------------------' + text

    if additional_text != '':
        sender.send_error_email(additional_text)


main()
