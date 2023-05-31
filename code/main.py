import sys
sys.path.append('train')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

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

    print("Start analysis")
    additional_text = ''
    data = log.get_data()
    print(f"Data size: {len(data)}")
    for text in data:
        data_to_analyze = transformer.transform(text)
        prediction = model.predict(data_to_analyze)
        if prediction > 0.9:
            additional_text += '-----------------------------------------------------' + text

    if additional_text != '':
        sender.send_error_email(additional_text)
        print("Email sent with error")

    print("Finished")

main()
