# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:16:20 2019

Establish SMTP connection to my Gmail acct
@author: Najd
"""

import smtplib

s = smtplib.SMTP(host='smtp.gmail.com', port=465)

s.starttls()
s.login(sammy.najd@gmail.com, RSd9697!)