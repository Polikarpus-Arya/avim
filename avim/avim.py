from tkinter import *
import subprocess
import json
import os
import charConv
import tkinter.font as tkfont
from PIL import Image, ImageTk

fontName  = 'Cascadia Mono'
fontSize  = 12
tabLength = 4

# Color
backGroundColor = '#1A1E24'
insertColor     = 'yellow'

# 'Perfect Dos VGA 437 Win'
# 'Modern DOS 8x14'

insertMode 	  = False
insertCommand = False

fileName = None
fileExte = None
pathName = os.getcwd()
pathName = pathName.replace('\\', '/')

statusText = None

jsonFile = open('buildSystem.json')
langFile = json.load(jsonFile)

def getFileExtension(file):
	return file.split('.')[1]

def getFontName(widget):
	arg = widget['font']
	tmpFontName = ''
	argBool = False
	for ch in arg:
		if ch == '}':
			break
		if argBool:
			tmpFontName = tmpFontName + ch
		if ch == '{':
			argBool = True 
	return tmpFontName

def changeFontSize(event, change):
	global fontSize, statusText

	if event.delta > 0:
		change = 1
	elif event.delta < 0:
		change = -1

	if change == -1:
		if fontSize > 1:
			fontSize += change
	else:
		fontSize += change
	for widget in window.winfo_children():
		if isinstance(widget, Label) or isinstance(widget, Text) or isinstance(widget, Entry):
			tmpFontName = getFontName(widget)
			widget.config(font = (tmpFontName, fontSize))
		elif isinstance(widget, Frame):
			for widget2 in widget.winfo_children():
				if isinstance(widget2, Label) or isinstance(widget2, Text) or isinstance(widget2, Entry):
					tmpFontName = getFontName(widget2)
					widget2.config(font = (tmpFontName, fontSize))

def formatCommand(tmpCommand):
	# fileName
	# fileBaseName
	# filePath
	tmpCommand = tmpCommand.replace('$fileName', fileName)
	tmpCommand = tmpCommand.replace('$filePath', pathName)
	tmpCommand = tmpCommand.replace('$fileBaseName', fileName.replace('.' + fileExte, ''))
	return tmpCommand

class listCommand:
	global statusText
	global fileName, fileExte, pathName

	# Saving file
	def sav(args = None):
		global statusText, fileName, fileExte
		if fileName == None and len(args) == 0:
			statusText = "No file name provided!"
			return
		elif fileName == None and len(args) > 0:
			fileName = args[0]
		open(pathName + '/' + fileName, 'w').write(content.get('1.0', END))
		fileExte = getFileExtension(fileName)
		statusText = "File saved!"
		window.title('avim (' + pathName + '/' + fileName + ')')

	# Build file
	def build(args):
		global statusText
		listCommand.sav(fileName)
		global statusText
		buildCommand = langFile[fileExte].get('Build')
		buildCommand = formatCommand(buildCommand)
		result = subprocess.run(buildCommand, stderr = subprocess.PIPE)
		# It has to be decode
		res = result.stderr.decode('utf-8')
		if len(res) == 0:
			res = "Program compiled successfully :)"
			status.config(fg = '#00FFFF')
		else:
			status.config(fg = 'red')
		statusText = res

	# Run file
	def run(args):
		global statusText
		runCommand = langFile[fileExte].get('Run')
		runCommand = formatCommand(runCommand)
		command.delete(0, END)
		result = subprocess.run(runCommand, shell = True, stdout = subprocess.PIPE)
		statusText = result.stdout.decode('utf-8')

	# Open file
	def e(args):
		global statusText, fileName, fileExte
		# Check whether the file is exist or not
		
		if len(args) == 0:
			statusText = 'No argument provided!\nExpected 1 argument!'
			return

		if args[0] not in os.listdir(pathName):
			statusText = 'File not found!'
			return

		fileName = args[0]
		fileContent = open(pathName + '/' + fileName, 'r').read()
		fileExte = getFileExtension(fileName)
		content.config(state = NORMAL)
		content.delete('1.0', END)
		content.insert(END, fileContent)
		content.config(state = DISABLED)
		statusText = '\'{}\''.format(fileName)
		window.title('avim (' + pathName + '/' + fileName + ')')

	# Print working directory
	def pwd(args = None):
		global statusText
		statusText = pathName

	# Change directory
	def cd(args):
		global statusText, pathName
		if len(args) == 0:
			statusText = pathName
			return
		if args[0] == '..':
			if len(pathName) > 2:
				while pathName[-1] != '/':
					pathName = pathName[:-1]
				pathName = pathName[:-1]
			
			if pathName[-1] == ':':
				pathName = pathName + '/'
			
			statusText = pathName
			return

		tmpPathName = os.path.join(pathName, args[0])
		if os.path.exists(tmpPathName) and os.path.isdir(tmpPathName):
			pathName = tmpPathName
		else:
			status.config(fg = 'red')
			statusText = 'Path not found!'
			return

		pathName = pathName.replace('\\', '/')

		# Handle such case like d:, c:, etc
		if pathName[-1] == ':':
			pathName = pathName + '/'

		statusText = pathName

	# Make directory
	def mkdir(args):
		global statusText
		if len(args) == 0:
			statusText = "No folder name provided!"
		else:
			if not os.path.exists(pathName + '/' + args[0]):
				os.mkdir(args[0])
				statusText = 'Folder created!'

	# List of directory content
	def ls(args):
		global statusText
		statusText = ''
		listDir = os.listdir(pathName)
		for i in range(0, len(listDir)):
			if i == 0:
				statusText = listDir[i]
			else:
				statusText += '   ' + listDir[i] 

			if os.path.isdir(listDir[i]):
				statusText += '/'

	# Help command
	def help(args):
		global statusText
		commandList = []
		for attr in dir(listCommand):
			if attr[0] != '_':
				commandList.append(attr)
		commandList.sort()
		print("List of available command")
		commandToPrint = ':' + commandList[0]
		for i in range(1, len(commandList)):
			commandToPrint += ' :' + commandList[i]
		statusText = commandToPrint

	# Exit program
	def q(args):
		exit()

# Display all character pressed
def handle(event):
	charStat.config(state = NORMAL)
	charStat.insert(END, charConv.charConv(event.keysym))
	charStat.config(state = DISABLED)
	charStat.xview_moveto(1)
	if insertMode == True:
		content.focus()
	else:
		command.focus()

# Set status widget content
def setStatus():
	global statusText
	status.config(state = NORMAL)
	status.delete('1.0', END)
	status.insert(END, statusText)
	status.config(state = DISABLED)
	# The return value of this function is in tuple
	rowCount = status.count('1.0', END, 'displaylines')[0] 
	if rowCount == 0:
		status.config(height = 1)
	elif rowCount <= 5:
		status.config(height = rowCount)
	else:
		status.config(height = 5)

# entering insert mode
def focusContent():
	global insertMode, insertCommand, statusText
	if insertMode == False and (insertCommand == False or len(command.get()) == 0):
		insertMode = True
		command.config(state = DISABLED)
		content.config(state = NORMAL)
		content.focus()
		status.config(fg = 'purple')
		rowPos, colPos = map(int, content.index(INSERT).split('.'))
		statusText = "INSERT, Line " + str(rowPos) + ", Column " + str(colPos)
		setStatus()

# entering command mode
def focusCommand(event):
	global insertMode, statusText
	insertMode = False
	status.config(fg = 'purple')
	statusText = 'COMMAND MODE'
	setStatus()
	content.config(state = DISABLED)
	command.focus()
	handle(event)

def toInsertCommand():
	global insertCommand
	insertCommand = True
	command.config(state = NORMAL)

# Submit command from commandLine to be execute
def submitCommand(event):
	status.config(fg = 'yellow')
	global insertCommand, statusText
	insertCommand = False
	args = command.get().split(' ')
	args[0] = args[0][1:]
	command.delete(0, END)
	command.config(state = DISABLED)

	# Calling method inside listCommand
	# args[0]  -> method name
	# args[1:] -> parameters
	
	try:
		getattr(listCommand, args[0])(args[1:])
	except AttributeError as e:
		status.config(fg = 'red')
		statusText = 'Command not found!'

	setStatus()
	window.update()

# AutoCLose bracket or parenthesis
def autoClose(event):
	char = None
	if event.keysym == 'bracketleft':
		char = '[' + ']'
	elif event.keysym == 'braceleft':
		char = '{' + '}'
	elif event.keysym == 'parenleft':
		char = '(' + ')'
	elif event.keysym == 'grave':
		char = '`' + '`'
	elif event.keysym == 'apostrophe':
		char = '\'' + '\''
	elif event.keysym == 'quotedbl':
		char = '\"' + '\"'
	
	rowPos, colPos = map(int, content.index(INSERT).split('.'))
	content.insert(str(rowPos) + '.' + str(colPos), char)
	content.mark_set('insert', str(rowPos) + '.' + str(colPos + 1))
	handle(event)
	return 'break' # To make sure the character we pressed doesn't inputed to the widget

# Auto Tab feature 
def alignTab(event):
	global tabLength
	tabCount = 0
	rowPos, colPos = map(int, content.index(INSERT).split('.'))
	prevRow = content.get(str(rowPos) + '.0', str(rowPos + 1) + '.' + str(colPos))

	for i in range(0, len(prevRow)):
		if prevRow[i] == '\t':
			tabCount += 1
		else:
			break

	# Special case
	if prevRow[colPos - 1:colPos + 1] == '{' + '}' \
		or prevRow[colPos - 1:colPos + 1] == '(' + ')' \
		or prevRow[colPos - 1:colPos + 1] == '[' + ']':

		content.delete(str(rowPos) + '.' + str(colPos), str(rowPos) + '.' + str(colPos + 1))
		content.insert(str(rowPos) + '.' + str(colPos), '\n')
		content.insert(str(rowPos + 1) + '.0', '\t' * (tabCount + 1) + '\n')
		content.insert(str(rowPos + 2) + '.0', '\t' * (tabCount) + prevRow[colPos])
		content.mark_set('insert', str(rowPos + 1) + '.' + str((tabCount + 1) * tabLength))
	
	else:
		content.insert(str(rowPos) + '.' + str(colPos), '\n')
		content.insert(str(rowPos + 1) + '.0', '\t' * tabCount)
	
	handle(event)
	return 'break' # To make sure the character we pressed doesn't inputed to the widget

# Updating window appearance when some window things is update
# such as: status text height, etc
def update():
	global statusText
	rowCount = status.count('1.0', END, 'displaylines')[0] 
	if rowCount == 0:
		status.config(height = 1)
	elif rowCount <= 5:
		status.config(height = rowCount)
	else:
		status.config(height = 5)
	if insertMode == True:
		rowPos, colPos = map(int, content.index(INSERT).split('.'))
		statusText = "INSERT, Line " + str(rowPos) + ", Column " + str(colPos)
		setStatus()
	status.after(100, update)

window = Tk()
window.geometry('650x650+5+6')
window.config(bg = backGroundColor, padx = 15, pady = 15)
window.title('aVim')
# icon = PhotoImage(file = 'icon.png')
# window.iconphoto(True, icon)
window.iconbitmap('avim_logo.ico')

# Widget
charStat= Entry(window, state = 'readonly', borderwidth = 0, width = 15, disabledbackground = backGroundColor, bg = backGroundColor, fg = 'green', font = (fontName, fontSize), readonlybackground = backGroundColor)
content = Text(window, borderwidth = 0, bg = backGroundColor, fg = 'white', font = (fontName, fontSize), selectbackground = backGroundColor, insertbackground = insertColor, wrap = NONE)
status 	= Text(window, borderwidth = 0, height = 4, bg = backGroundColor, fg = 'purple', font = (fontName, fontSize), wrap = CHAR)
command = Entry(window, state = DISABLED, borderwidth = 0, bg = backGroundColor, fg = 'green', font = (fontName, fontSize), disabledbackground = backGroundColor, insertbackground = 'green')

# Setting tab size
fontTabs = tkfont.Font(font = content['font'])
content.config(tabs = fontTabs.measure(' ' * tabLength))


command.pack(side = BOTTOM, fill = 'x')
status .pack(side = BOTTOM, fill = 'x')
charStat.pack(side = TOP, anchor = E)
content.pack(side = TOP, fill = 'both', expand = True)

status .config(state = DISABLED)
content.config(state = DISABLED)
command.config(state = DISABLED)
command.focus_force()

# Keybinding
window .bind('<Key>'	, lambda event : handle(event))
 
content.bind('<Escape>'	, lambda event : focusCommand(event))
content.bind('<Return>'	, lambda event : alignTab(event))

command.bind('<i>'		, lambda event : focusContent())
command.bind('<:>'		, lambda event : toInsertCommand())
command.bind('<Return>'	, lambda event : submitCommand(event))

# Auto close key binding
content.bind('<bracketleft>', autoClose)
content.bind('<braceleft>' 	, autoClose)
content.bind('<parenleft>' 	, autoClose)
content.bind('<quotedbl>'  	, autoClose)
content.bind('<grave>'		, autoClose)
content.bind('<apostrophe>'	, autoClose)

# Changing font size
content.bind('<Control-equal>'		, lambda event : changeFontSize(event, 1))
content.bind('<Control-minus>'		, lambda event : changeFontSize(event, -1))
content.bind('<Control-MouseWheel>'	, lambda event : changeFontSize(event, 1))

update()

window.mainloop()

# Install command
# pyinstaller --icon=avim_logo.ico --onefile avim.py
# INPUT DATA