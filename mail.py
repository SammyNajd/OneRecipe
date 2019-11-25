# -*- coding: utf-8 -*-
"""
Starting point:
    In this file, we will be able to read the list of contacts
    Add to the list of contact
"""

import smtplib
from string import Template
import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import schedule
import time


def get_contacts(file):
    """
    Get contacts from contacts file
    """
    
    names = []
    emails = []
    with open(file, mode='r', encoding='utf-8') as contacts:
        for contact in contacts:
            names.append(contact.split()[0])
            emails.append(contact.split()[2])
    return names, emails


def read_template(file):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(file, 'r', encoding='utf-8') as template:
        template_content = template.read()
    return Template(template_content)

def send_mail(ingredient_links):
    names, emails = get_contacts(config.CONTACTS) # read contacts
    message_template = read_template(config.OUT_MESSAGE)   

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(config.ADDRESS, config.PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()     

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())
        counter = 1
        for link in ingredient_links:
            message += str(counter) + '. ' + link 
            counter += 1

        message += config.SIGN_OFF
        # setup the parameters of the message
        msg['From']= config.ADDRESS
        msg['To']= 'sammy.najd@gmail.com'
        msg['Subject']="Your daily recipe"
        
        # add in the message body
        msg.attach(MIMEText(message, 'html'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
   

def main():
    schedule.every().day.at("21:50").do(send_mail)

    while True:
        schedule.run_pending()
        time.sleep(60)
        
if __name__ == '__main__':
    main()
    
