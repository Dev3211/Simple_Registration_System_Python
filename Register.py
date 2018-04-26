#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import MySQLDB module so that we can make a db connection, re module for the regex match, bcrypt module for bcrypt hash

import MySQLdb
import re
import bcrypt

MySQLdb.escape_string("'")  # escape string

db = MySQLdb.connect(host='localhost', user='root',
                     passwd='', db='')  # creating a db connection

cur = db.cursor()

print ' Simple registration system using Python along with MySQL prepared statement'
print '\n'

username = raw_input(' Your username: ')  # we will take the inputs and use it in the MySQL insert statement
password = raw_input(' Your password: ')  # we will take the inputs and use it in the MySQL insert statement

# checks:

invalid_chars = '^<>/"|\{}[]~`$'  # used to block invalid chars for the username/password
if not username:
    raise Exception('Your username seems to be blank')  # check if username is blank
elif not password:
    raise Exception('Your password seems to be blank')  # check if password is blank
elif len(username) < 3:
    raise Exception('Username is way too short!')  # check if username is short
elif len(password) < 3:
    raise Exception('Password is way too short!')  # check if password is short
elif set(invalid_chars).intersection(username):
    raise Exception('Your username contains illegal chars')  # check if username has invalid chars to prevent mysql injection
elif set(invalid_chars).intersection(password):
    raise Exception('Your password contains illegal chars')  # check if password has invalid chars to prevent mysql injection
elif not re.search('[a-z]', password):
    raise Exception('Your password must contain at least one lower case letter'
                    )  # check if password has atleast one lower case letter
elif not re.search('[A-Z]', password):
    raise Exception('Your password must contain at least one upper case letter'
                    )  # check if password has atleast one upper case letter
elif not re.search('[0-9]', password):
    raise Exception('Your password must contain at least digit')  # check if password has at least one digit

sql = "SELECT COUNT(*) FROM %s WHERE username = '%s'" % ('Table',
        username)  # username check
cur.execute(sql)
result = cur.fetchone()
found = result[0]
if found == 1:
    raise Exception('Username exists')

if username and password:  # if username and password returns true after every check we continue forward
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())  # generate a bcrypt hash along with a random salt
    cur.execute('INSERT INTO Table (username, password) VALUES (%s, %s)'
                , (username, hashed))  # define parameters, one of the safest way to do it
    db.commit()  # commit the execution
    cur.close()  # close query
    db.close()  # close db connection
    print '\n'
    print 'You have successfully registered, your username is %s and your password is %s' \
        % (username, password)
else:
    raise Exception('An error occured')  # return this if the if statement returns false
