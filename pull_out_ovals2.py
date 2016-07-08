import sys
new_ovals = ''
file1 = open(sys.argv[1],'r')
for line in file1:
	if '//' in line:
		for char in line:
			if (char.isdigit()) or (char==','):
				new_ovals+=char
		new_ovals+=','
file2 = open("3_small_plate_partial_macro.ijm",'r')
buffer = ''
for line in file2:
    if "newArray" not in line or ("Set Scale" not in line and sys.argv[2]):
        buffer+=line
    elif "Set Scale" in line and sys.argv[2]:
        dist = 0.04*int(sys.argv[2])*60###0.04 px/(DPI*mm^2)*x DPI*60mm = y px/mm e.g. 500 DPI -> 20 px/mm
        buffer+=('run("Set Scale...","distance='+dist+' known=60 unit=unit");')
    else:
        buffer+=('ovals = newArray('+new_ovals[:-1]+');\n')
file2.close()
file3 = open("3_small_plate_partial_macro.ijm",'w')
file3.write(buffer)
#file2 = open('extracted_ovals'+sys.argv[1][-5]+'.txt','w')
#file2.write(new_ovals)
file1.close()
file3.close()
