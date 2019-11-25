# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:13:06 2019

Purpose: This function will read/return a template of the message
@author: Najd
"""

from string import Template

def read_template(file):
    with open(file, 'r', encoding='utf-8') as template:
        template_content = template.read()
    return Template(template_content)

