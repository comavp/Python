#! python3
# This is a simple program for unsafe storing passwords.

import sys, pyperclip

PASSWORDS = {
	'root': 'root',
	'user1': '12345'		
}
if len(sys.argv) < 2:
	print('Wrong number of arguments!')
	print('Right format: python passwordManager.py [name_of_account]\n')
	print('(programm will copy password of \'name_of_account\')')
	sys.exit()

account = sys.argv[1]

if account in PASSWORDS:
	pyperclip.copy(PASSWORDS[account])
	print('Password for \'' + str(account) + '\' was copied into buffer')
else:
	print('\'' + str(account) + '\' is an unknown account')