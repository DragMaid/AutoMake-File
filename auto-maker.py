import os
import re

# Dir always in the current path 
directory = "./" 
CPPS = []
DATASET = {}

def sort(file):
	if file.endswith(".cpp"):
		CPPS.append(file)
	else:
		pass 

def FindIncluded(file):
	checkpoint = []
	f = open(str(file), "r")
	fl = f.readlines()
	for line in fl:
		if line[0] == "#":
			try:
				checkpoint.append(re.findall(r'\"(.+?)\"',line)[0]) #The func itself is loop through the same line => a list => [0] to get the first argument
			except:
				pass
	f.close()
	DATASET[file] = checkpoint

def AddDep(name):
	recompile = ""
	text2 = f"{name.split('.')[0]}.o: {name} "
	for item in DATASET[name]:
		text2 += f"{item} "
		if str(item).endswith(".cpp"):
			recompile += f"{item} "
	text2 += f"\n	g++ -c {name} {recompile}\n"
	return text2

def writeFile(NAME):
	text = f"a: "
	for x in CPPS:
		text += f"{(x.split('.'))[0]}.o "
	text += "\n	"
	text += f"g++ -o {NAME}{text[2:-1]}"
	for x in CPPS:
		text += AddDep(x)
	f = open("makefile", "w+")
	f.write(text)

def start():
	print("What do you want to name your executable: ")
	NAME = str(input())
	for file in os.listdir(directory):
		try:
			for inner in os.listdir(file):
				sort(inner)
		except:
			sort(file)

	for x in CPPS:
		FindIncluded(x)
	writeFile(NAME)

if __name__ == "__main__":
	start()
