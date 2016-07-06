import sys
new_ovals = ''
file1 = open(sys.argv[1],'r')
for line in file1:
	if '//' in line:
		for char in line:
			if (char.isdigit()) or (char==','):
				new_ovals+=char
		new_ovals+=','
file2 = open("7_small_plate_partial_macro.ijm",'r')
buffer = ''
for line in file2:
    if "newArray" not in line:
        buffer+=line
    else:
        buffer+=('ovals = newArray('+new_ovals[:-1]+');\n')
file2.close()
file3 = open("3_small_plate_partial_macro.ijm",'w')
file3.write(buffer)
#file2 = open('extracted_ovals'+sys.argv[1][-5]+'.txt','w')
#file2.write(new_ovals)
file1.close()
file3.close()
