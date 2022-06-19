from flask import url_for
from smtplib import SMTP
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from config import settings

def  messageConfirm(email, link):
    message = EmailMessage()

    message['Subject'] = '¡Bienvenido(a)!'
    message['From'] = 'edisonchicunque2020@itp.edu.co'
    message['To'] = email
    message.set_content(
                        "Gracias por registrarte. Abre este link para terminar el proceso de confirmacion: {}".format(link)
                        )

    username = settings.SMPT_USERNAME
    password = settings.SMPT_PASSWORD

    server = SMTP(settings.SMPT_HOSTNAME)
    server.starttls()
    server.login(username, password)
    server.send_message(message)
    server.quit()