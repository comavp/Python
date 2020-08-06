#! python3
# bulletPointAdder.py - Add special markers at the beginning of every string, 
# which is stored in change buffer

import pyperclip

text = pyperclip.paste()
marker = '* '

lines = text.split('\n')
for i in range(len(lines)):
	lines[i] = marker + lines[i]

text = '\n'.join(lines)
pyperclip.copy(text)