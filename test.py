# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 18:41:35 2019

@author: safak
"""

import sqlite3
admin_db=sqlite3.connect('admin_details.sqlite3')
admin_curs=admin_db.cursor()
admin_curs.execute('''SELECT password FROM details;''')
record = admin_curs.fetchall()
print(record)
a=str(record[0][0])
print(a)
if a=='safa123':
    print("lol")
else:
    print("no")
print(type(record[0][0]))
print(a)
print(type(a))