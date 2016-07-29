# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 11:38:04 2016

@author: Eamon
"""
import numpy as np
from scipy import stats as st
import os
from PIL import Image as im
from PIL import ImageDraw as imd
from scipy import ndimage as nd
import warnings
import copy
def open_file(name):
    '''Does what it says on the tin, checks to make sure directory isn't misspelled first'''
    path = '/'.join(name.split('/')[:-1])
    try:    
        assert os.path.exists(path)#works for both files and directories
        file = im.open(name)
#        x_sf = int(round(file.size[0]/10200.0,0))#makes a scaling factor by finding size over the 1200 DPI size
#        y_sf = int(round(file.size[1]/14039.0,0))
        arr = np.array(file)
        return arr#,x_sf,y_sf
    except AssertionError:
        print(path," does not exist.  Check for misspellings.")
        return None
def rough_fit(arr):#,x_sf,y_sf):
    '''finds the upper left hand corners for the search areas''' 
    corners = []
    x = arr.shape[1]
    y = arr.shape[0]
    for i in range(0,4):
        for j in range(0,3):
            com = nd.measurements.center_of_mass(arr[int(i/4*y):int((i+1)/4*y),int(j/3*x):int((j+1)/3*x)])
            com = list(com)
            if j==0:
                com[0] = int(com[0]+(i/4)*y-1500)#*y_sf)
                com[1] = int(com[1]+(j/3)*x-1500)#*x_sf)
            elif j==1:
                com[0] = int(com[0]+(i/4)*y-1550)#*y_sf)
                com[1] = int(com[1]+(j/3)*x-1550)#*x_sf)
            else:
                com[0] = int(com[0]+(i/4)*y-1550)#*y_sf)
                com[1] = int(com[1]+(j/3)*x-1750)#*x_sf)
            corners.append(com)
    return corners
def fit_quadratic(arr):
    '''Does what it says on the tin'''
    t = np.column_stack(np.where(arr>0))
    x = []
    y = []
    for a in t:
        x.append(a[1])
        y.append(a[0])
    quad  = np.polyfit(x,y,2)
    return quad
def solve_for_vertex(quad):
    '''Finds vertex from std form equation'''
    a = quad[0]
    b = quad[1]
    c = round(quad[2],0)
    h = b/(2*a)
    x = -h
    y = a*x**2+b*x+c
    vtx = [x,y]
    return vtx
def find_radius(arr):
    '''Fits 2 quadratics to circle to find verteces and :. diameter/radius'''
    
    roi1 = copy.copy(arr)
    roi1[:int(arr.shape[0]/2),:] = 0
    roi1[:,:int(arr.shape[1]/4)] = 0
    roi1[:,int(3*arr.shape[1]/4):] = 0
#    roi1[roi1>222] = 0
    roi2 = copy.copy(arr)
    roi2[int(arr.shape[0]/2):,:] = 0
    roi2[:,:int(arr.shape[1]/4)] = 0
    roi2[:,int(3*arr.shape[1]/4):] = 0
#    roi2[roi2>222] = 0
    fx = fit_quadratic(roi1)
    gx = fit_quadratic(roi2)
#    print(fx,'\t',gx)
    vtx1 = solve_for_vertex(fx)
    vtx2 = solve_for_vertex(gx)
    radius = int((vtx1[1]-vtx2[1])/2)
#    print(vtx1,vtx2,radius)
    return radius-180
def find_centers(arr):#,x_sf,y_sf):
    '''Use center of mass of thresholded image to find center point of each region of template'''
    centers = []
    radii = []
    arr_t = copy.copy(arr)
    arr_t[arr_t>210] = 0
    predefined = [[576, 312],[3744, 264],[6960, 312],[552, 3624],[3768, 3624],[6936, 3696],[504, 7080],[3720, 7080],[6912, 7104],[552, 10391],[3696, 10487],[6888, 10511]]
    for pair in predefined:
#        pair[0]*=x_sf
#        pair[1]*=y_sf
        pair.reverse()
    
    if np.average(arr[:,-500:])>190: 
        target_regions = predefined
    else:
        target_regions = rough_fit(arr_t)#,x_sf,y_sf)
        warnings.warn("Template is not properly aligned in scanner!  Double check all ROIs for image: "+img_name.split('/')[-1],RuntimeWarning)
    add = [3300,3250]#[3300*y_sf,3250*x_sf]
    count = 0

    for pair in target_regions:
        count+=1
#        pair.reverse()
        max_y = pair[0]+add[1] if pair[0]+add[1]<arr.shape[0] else arr.shape[0]
        max_x = pair[1]+add[0] if pair[1]+add[0]<arr.shape[1] else arr.shape[1]
        roi = arr[pair[0]:max_y,pair[1]:max_x]
        roi1 = copy.copy(roi)###Necessary because  roi1 = roi -> roi1 IS roi
        roi1[roi1>210] = 0
        roi[roi<212] = 0
        roi[roi>218] = 0
        try:
            cp = nd.measurements.center_of_mass(roi1)
            cp = list(cp)
            cp[0] = int(cp[0]+pair[0])
            cp[1] = int(cp[1]+pair[1])
            cp.reverse()
        except ValueError:
            cp = [0,0]
            print("Center acquisition failed on plate: ",count)
            print("All values in region were identical, likely 0")
        pair.reverse()
    
    return centers,radii
def make_ovals(centers,radii):
    '''ImageJ makes ovals by defining the upper left hand corner and the width and height from that'''
    ovals = []
    for i in range(len(centers)):
        cp = centers[i]
        radius = radii[i]
        pt_x = int(round(cp[0]-radius,0))#(np.sqrt(2)/2*radius),0))
        pt_y = int(round(cp[1]-radius,0))#(np.sqrt(2)/2*radius),0))
        oval = [pt_x,pt_y,2*radius,2*radius]#int(round(np.sqrt(2)*radius,0)),int(round(np.sqrt(2)*radius,0))]
        ovals+=oval
#    print(ovals)
    ovals = [str(oval) for oval in ovals]
#    print(len(ovals)/4)
    return ovals
def edit_file(file,arg,new_ovals):
    '''Does what it says on the tin.  It will edit a file containing the lines "newArray" or "Set Scale..." and update their values'''
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
            buffer+=('ovals = newArray('+','.join(new_ovals)+');\n')
        elif "Set Scale" in line and arg:
            dist = 0.04*int(arg)*60###0.04 px/(DPI*mm^2)*x DPI*60mm = y px/mm e.g. 500 DPI -> 20 px/mm
            buffer+=('\t\trun("Set Scale...","distance='+str(dist)+' known=60 unit=unit");\n')
        else:
            buffer+=line
#    print(buffer.split('\n')[:2])
    return buffer
def main():
    global img_name
    img_name = sys.argv[1]
    arr = open_file(img_name)
    if not None in list(arr):
        centers,radii = find_centers(arr)#,x_sf,y_sf)
        new_ovals = make_ovals(centers,radii)
        file = open(sys.argv[2],'r')
        dpi = 1200#sys.argv[3]
        buffer = edit_file(file,dpi,new_ovals)
        file.close()
        file = open(sys.argv[2],'w')
        file.write(buffer)
        file.close()
main()
