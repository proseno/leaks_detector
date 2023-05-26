import smtplib
import os


class Sender:
    def __init__(self):
        self.email = os.environ.get('GMAIL_ADDRESS')
        self.password = os.environ.get('GMAIL_PASSWORD')
        self.admin_email = os.environ.get('ADMIN_EMAIL')

    def send_email(self, subject, body):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.email, self.password)
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(self.email, self.admin_email, msg)

    def send_error_email(self, additional_text: str):
        subject = 'Error! Data leak detection'
        body = 'Please check your MySQL server:\n' + additional_text
        self.send_email(subject, body)
