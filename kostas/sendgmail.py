#!/usr/bin/python
#title           :sendgmail.py
#description     :This script will email a set of files specified as arguments.
#author          :kostas
#date            :20130214
#version         :0.1
#usage           :python sendgmail.py [list of files]
#example         :python sendgmail.py *.csv
#==============================================================================
import sys,smtplib,email,email.encoders,email.mime.multipart

# Hardcoded user and email information can be set here
# if not set the script will ask for them on runtime
USERNAME = ''
PASSWORD = ''
DESTINATION = ''
SUBJECT = ''

"""
This function sends a set of attachments (array of paths to files) to a destination email
using a GMail account specified by the username and password parameters.
"""
def sendgmail(username = USERNAME, password = PASSWORD, destination = DESTINATION, 
              subject = SUBJECT, attachments = []):
    email_message = email.mime.multipart.MIMEMultipart()
    email_message['Subject'] = subject
    email_message['To'] =  destination
    email_message['From'] = username
    email_message.preamble = ""
	
    for attachment in attachments:
        fp = open(attachment, 'rb')
        file_attachment = email.mime.base.MIMEBase("application", "octet-stream")
        file_attachment.set_payload(fp.read())
        fp.close()
        email.encoders.encode_base64(file_attachment)
        file_attachment.add_header('Content-Disposition', 'attachment', 
                                    filename=attachment.split("/")[-1])
        email_message.attach(file_attachment)
    
    composed_email = email_message.as_string()
    mail_server = smtplib.SMTP('smtp.gmail.com:587')
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(username,password)
    mail_server.sendmail(email_message['From'], email_message['To'], composed_email)
    mail_server.quit()



if __name__ == "__main__":
    import getpass
    if USERNAME == '':
        USERNAME = raw_input("Enter username: ")
    if PASSWORD == '':
        PASSWORD = getpass.getpass("Enter password: ")
    if DESTINATION == '':
        DESTINATION = raw_input("Enter destination: ")
    if SUBJECT == '':
        SUBJECT = raw_input("Enter subject: ")
    
    sendgmail(username=USERNAME, password=PASSWORD, destination=DESTINATION,
              subject=SUBJECT, attachments=sys.argv[1:])
