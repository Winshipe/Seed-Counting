import sys
new_ovals = ''
file1 = open(sys.argv[1],'r')
for line in file1:
	if '//' in line:
		for char in line:
			if (char.isdigit()) or (char==','):
				new_ovals+=char
		new_ovals+=','
file2 = open('extracted_ovals'+sys.argv[1][-5]+'.txt','w')
file2.write(new_ovals)
file1.close()
file2.close()
