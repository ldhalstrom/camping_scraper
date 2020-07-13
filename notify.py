"""CAMPSITE AVAILABILITY NOTIFICAITON
use gmail stmp to send notifications

NOTE: Need to 'allow less secure apps' in gmail
"""

import smtplib
import os


def ReadEmailCredentials(ifile='email_credential.txt'):
    """Read email address and password of email to use for notificaitons and recipient
    1st line: sender email address, 2nd line: password, 3rd line: recipient address
    NOTE: you should make this file unreadable (chmod 700)
    """

    if not os.path.exists(ifile):
        print('FAILED TO SEND NOTIFICATION EMAIL')
        print('PLEASE ADD EMAIL CREDENTIAL FILE SO THAT I CAN LOG IN AND SEND EMAILS')
        return
    f = open(ifile, 'r')
    sender   = f.readline().strip()
    passwd   = f.readline().strip()
    reciever = f.readline().strip()
    f.close()

    return sender, passwd, reciever


def SendEmail(Subject, Content, reciever, sender, passwd):
    """Send an email

    Subject  --> email subject text
    Content  --> email content text
    reciever --> recipient email address
    sender   --> sender email address
    passwd   --> sender email password
    """

    #Construct email message
    message = 'Subject: {}\n\n{}'.format(Subject, Content)

    mail = smtplib.SMTP('smtp.gmail.com',587)
    # mail = smtplib.SMTP('smtp.gmail.com',465)

    mail.ehlo()

    mail.starttls()

    success = mail.login(sender,passwd)
    # print(success)

    mail.sendmail(sender,reciever,message)

    mail.close()













#FUNCTION FOR CREATING A SUMMARY OF ALL CAMPSITE QUERIES







def main(Subject, Content):


    #READ CREDENTIALS FOR SENDER EMAIL AND RECIPIENT
    sender, passwd, reciever = ReadEmailCredentials()

    #SEND THE EMAIL
    SendEmail(Subject, Content, reciever, sender, passwd)

if __name__ == "__main__":


    #test

    Subj = 'test subject'
    Cont = 'test content'


    main(Subj, Cont)














