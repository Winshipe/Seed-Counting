import sys
def edit_file(file,new_ovals):
    try:    
        assert new_ovals
    except AssertionError:
        print('No Ovals!')
    try:
        assert file
    except AssertionError:
        print("No file!")
    buffer = ''
    for line in file:
        if "newArray" in line:
            buffer+=('ovals = newArray('+new_ovals[:-1]+');\n')
        elif "Set Scale" in line and sys.argv[2]:
            dist = 0.04*int(sys.argv[2])*60###0.04 px/(DPI*mm^2)*x DPI*60mm = y px/mm e.g. 500 DPI -> 20 px/mm
            buffer+=('\t\trun("Set Scale...","distance='+str(dist)+' known=60 unit=unit");')
        else:
            buffer+=line
#    print(buffer.split('\n')[:2])
    return buffer
n_ovals = ''
file1 = open(sys.argv[1],'r')
for line in file1:
	if '**' in line:
		for char in line:
			if (char.isdigit()) or (char==','):
				n_ovals+=char
		n_ovals+=','
file2 = open("3_small_plate_partial_macro.ijm",'r')
buffer = edit_file(file2,n_ovals)
file2.close()
try:
    assert buffer
    file3 = open("3_small_plate_partial_macro.ijm",'w')
    file3.write(buffer)
    file3.close()
except AssertionError:
    print("Failed to make buffer for macro 3!")
file4 = open("4_small_plate_partial_macro.ijm",'r')
buffer = edit_file(file4,n_ovals)
file4.close()
try:
    assert buffer
    file5 = open("4_small_plate_partial_macro.ijm",'w')
    file5.write(buffer)
    file5.close()
except AssertionError:
    print("Failed to make buffer for macro 4!")
file1.close()
