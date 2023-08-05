import pandas as pd
import random
import smtplib
from getpass import getpass

class list_upload:

    def __init__(self,url):
        self.url = url
        global URL
        URL =self.url

    @property
    def show(self):
        df = pd.read_csv(URL)
        return df
    
    @property
    def welcome(self):
        df = self.show
        col = df["nombres"]
        for nombre in col:
            print("BIENVENIDO AL CURSO"+" "+ nombre.upper())

    @property
    def winner(self):
        df = self.show
        col = df["nombres"]
        ganador = random.choice(col)
        return ganador

    def send_mail(self,asunto,mensaje,test_mail=False):
        df = self.show
        gmail_user = 'jhonny.osorio@profesores.uamerica.edu.co'
        gmail_password = getpass("Enter password ")

        subject = asunto
        message = mensaje 

        if test_mail== True:
            nombre = df["nombres"][0].split()[0]
            mail_from = gmail_user
            mail_to   = gmail_user
            mail_subject = subject
            mail_message_body = message.format(nombre)
            mail_message ='Subject: {}\n\n{}'.format(mail_subject, mail_message_body)
            # Sent Email
            # https://www.google.com/settings/security/lesssecureapps
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_password)
            server.sendmail(mail_from, mail_to, mail_message)
            server.close()
            print("Mail Sent Successfully")

        else:
            
            for i in range(df.shape[0]):
                nombre = df["nombres"][i].split()[0]
                mail_from = gmail_user
                mail_to   = df["correos"][i].split()[0]
                mail_subject = subject
                mail_message_body = message.format(nombre)
                mail_message ='Subject: {}\n\n{}'.format(mail_subject, mail_message_body)
                # Sent Email
                # https://www.google.com/settings/security/lesssecureapps
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(gmail_user, gmail_password)
                server.sendmail(mail_from, mail_to, mail_message)
                server.close()
            print("Successfully Sent Emails")
