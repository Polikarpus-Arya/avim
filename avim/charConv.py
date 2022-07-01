def charConv(text):

	if text == 'BackSpace':
		text = '\u232B'
	elif text == 'Tab':
		text = '\u21B9'
	elif text == 'space':
		text = '\u23d8'
	elif text == 'Next':
		text = '\u21e9'
	elif text == 'Prior':
		text = '\u21e7'
	elif text == 'Return':
		text = '\u21a9'
	elif text == 'Delete':
		text = '\u2326'
	elif text == 'Control_R':
		text = '\u2318'
	elif text == 'Control_L':
		text = '\u2318'
	elif text == 'Shift_L':
		text = '\u21eb'
	elif text == 'Shift_R':
		text = '\u21eb'
	elif text == 'Win_L':
		text = '\u2317'
	elif text == 'Alt_L':
		text = '\u2387'
	elif text == 'Alt_R':
		text = '\u2387'
	elif text == 'Caps_Lock':
		text = '\u2302'
	elif text == 'Escape':
		text = '\u2397'
	elif text == 'Down':
		text = '↓'
	elif text == 'Up':
		text = '↑'
	elif text == 'Right':
		text = '→'
	elif text == 'Left':
		text = '←'
	elif text == 'greater':
		text = '>'
	elif text == 'less':
		text = '<'
	elif text == 'semicolon':
		text = ';'
	elif text == 'period':
		text = '.'
	elif text == 'bracketleft':
		text = '['
	elif text == 'braceleft':
		text = '{'
	elif text == 'bracketright':
		text = ']'
	elif text == 'braceright':
		text = '}'
	elif text == 'plus':
		text = '+'
	elif text == 'minus':
		text = '-'
	elif text == 'underscore':
		text = '_'
	elif text == 'equal':
		text = '='
	elif text == 'backslash':
		text = '\\'
	elif text == 'bar':
		text = '|'
	elif text == 'slash':
		text = '/'
	elif text == 'question':
		text = '?'
	elif text == 'grave':
		text = '`'
	elif text == 'asciitilde':
		text = '~'
	elif text == 'exclam':
		text = '!'
	elif text == 'at':
		text = '@'
	elif text == 'numbersign':
		text = '#'
	elif text == 'dollar':
		text = '$'
	elif text == 'percent':
		text = '%'
	elif text == 'asciicircum':
		text = '^'
	elif text == 'ampersand':
		text = '&'
	elif text == 'asterisk':
		text = '*'
	elif text == 'parenleft':
		text ='('
	elif text == 'parenright':
		text = ')'
	elif text == 'comma':
		text = ','
	elif text == 'colon':
		text = ':'
	elif text == 'quotedbl':
		text = '"'
	elif text == 'apostrophe':
		text = '\''
	elif text == '\u23b5':
		text = ' '

	return text