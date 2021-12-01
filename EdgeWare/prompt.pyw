import os, pathlib, json, random as rand, tkinter as tk
from tkinter import messagebox
from tkinter import *

hasData = False
textData = {}
maxMistakes = 3
submission_text = 'I Submit <3'
command_text	= 'Type for me, slut~'
PATH = str(pathlib.Path(__file__).parent.absolute())
os.chdir(PATH)

with open(PATH + '\\config.cfg') as settings:
	maxMistakes = int(json.loads(settings.read())['promptMistakes'])

if(os.path.exists(PATH + '\\resource\\prompt.json')):
	hasData = True
	with open(PATH + '\\resource\\prompt.json', 'r') as f:
		textData = json.loads(f.read())
		try:
			submission_text = textData['subtext']
		except:
			print('no subtext')
		try:
			command_text = textData['commandtext']
		except:
			print('no commandtext')

if(not hasData):
	messagebox.showerror('Prompt Error', 'Resource folder contains no "prompt.json". Either set prompt freq to 0 or add "prompt.json" to resource folder.')

def unborderedWindow():
	if(not hasData):
		exit()
	root = Tk()
	label = tk.Label(root, text='\n' + command_text + '\n')
	label.pack()
	
	global txt
	txt = buildText()

	wid = root.winfo_screenwidth() / 4
	hgt = root.winfo_screenheight() / 2

	textLabel = Label(root, text=txt, wraplength=wid)
	textLabel.pack()

	root.geometry('%dx%d+%d+%d' % (wid, hgt, 2*wid - wid / 2, hgt - hgt / 2))

	root.overrideredirect(1)
	root.frame = Frame(root, borderwidth=2, relief=RAISED)
	root.frame.pack_propagate(True)
	root.wm_attributes('-topmost', 1)

	global inputBox
	inputBox = Text(root)
	inputBox.bind("<KeyRelease>", OnEntryClick)
	inputBox.pack()

	subButton = Button(root, text=submission_text, command=lambda: checkTotal(root, txt, inputBox.get(1.0, "end-1c")))
	subButton.place(x=wid - 5 - subButton.winfo_reqwidth(), y=hgt - 5 - subButton.winfo_reqheight())
	root.mainloop()

def buildText():
	moodList = textData['moods']
	freqList = textData['freqList']
	outputPhraseCount = rand.randint(int(textData['minLen']), int(textData['maxLen']))
	strVar = ''
	selection = rand.choices(moodList, freqList, k=1)
	for i in range(outputPhraseCount):
		strVar += textData[selection[0]][rand.randrange(0, len(textData[selection[0]]))] + ' '
	return strVar.strip()

def getMistake(exp, actual):
	exp_arr=[char for char in exp]
	act_arr=[char for char in actual]
	
	for i in range(0,len(act_arr)):
		if(exp_arr[i] != act_arr[i]):
			return i
	
	return -1

def OnEntryClick(event):
	start=getMistake(txt,inputBox.get("1.0","end-1c"))
	if(start!=-1):
		inputBox.tag_configure("mistake",foreground="red")
		inputBox.tag_add("mistake", "1."+str(start), "end-1c")
	else:
		inputBox.tag_configure("correct",foreground="black")
		inputBox.tag_add("correct", "1.0", "end-1c")

def checkTotal(root, a, b):
	if checkText(a, b):
		root.destroy()

def checkText(a, b):
	mistakes = 0
	if len(a) != len(b):
		mistakes += abs(len(a)-len(b))
	for i in range(min(len(a), len(b))):
		if a[i] != b[i]:
			mistakes += 1
	return mistakes <= maxMistakes

try:
	unborderedWindow()
except Exception as e:
	messagebox.showerror('Prompt Error', 'Could not create prompt window.\n[' + str(e) + ']')