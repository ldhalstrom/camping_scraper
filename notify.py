"""CAMPSITE AVAILABILITY NOTIFICAITON
use gmail stmp to send notifications

NOTE: Need to 'allow less secure apps' in gmail
"""

import smtplib


def ReadEmailCredentials(ifile='email_credential.txt'):
    """Read email address and password of email to use for notificaitons
    1st line: email address, 2nd line: password
    NOTE: you should make this file unreadable (chmod 700)
    """

    f = open(ifile, 'r')
    email  = f.readline().strip()
    passwd = f.readline().strip()
    f.close()

    return email, passwd


def testsend(sender, passwd, reciever):
    content = ("Content to send")

    mail = smtplib.SMTP('smtp.gmail.com',587)

    mail.ehlo()

    mail.starttls()

    mail.login(sender,passwd)

    mail.sendmail(sender,reciever,content)

    mail.close()

    print("Sent")
















#FUNCTION FOR CREATING A SUMMARY OF ALL CAMPSITE QUERIES







def main():


    email, passwd = ReadEmailCredentials()
    # print(email)
    # print(passwd)

    testsend(email, passwd, email)

if __name__ == "__main__":
    main()














