"""
https://www.youtube.com/watch?v=WmgD2pPhj3Q&t=76s
https://haveibeenpwned.com/
"""

import sys, hashlib

password_file = '[PATH TO PASSOWRD FILE]'

pwd = input("Insert password to check: ")
message_digest = hashlib.sha1()
message_digest.update(bytes(pwd, encoding='utf-8'))
to_check = message_digest.hexdigest().upper()

leaked = False
with open(password_file) as file:
    for line in file:
        if to_check in line:
            print(f"Dein Passwort wurde {line.split(':')[1].strip()} mal geleaked!")
            leaked = True
            break
    if not leaked:
        print('Dein Passwort wurde noch nicht geleaked!')