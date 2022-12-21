import time

import win32com.client as win32
from datetime import datetime
import os


# create function to send email with outlook application
def send_email(subject, body, to_email):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_email
    mail.Subject = subject
    mail.Body = body
    mail.Send()
    print('Email sent!')
    return


# create function to read mails from outlook application
def read_email():
    outlook = win32.Dispatch('outlook.application')
    mapi = outlook.GetNamespace("MAPI")
    inbox = mapi.GetDefaultFolder(6)
    messages = inbox.Items
    messages = messages.restrict("[Unread] = True")
    print(messages.count)
    for message in messages:
        print(message.Sender.GetExchangeUser().PrimarySmtpAddress)
        # if str(message.sender) == "Kozanecki, Bartosz":
        #     message.unread = False
        #     reply = message.Reply()
        #     reply.Body = "Dziękuję za wiadomość. Wkrótce się odezwę."
        #     reply.Send()


# execute function to send email
# send_email('Witaj', 'To nie jest mail testowy, odpisz mi :)', 'bartosz.kozanecki@assaabloy.com')

if __name__ == "__main__":
    while True:
        read_email()
        time.sleep(5)
