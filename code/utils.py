import os
import point
import fileinput

def read_input(file_name):
    #fh = open(file_name)
    #lines = fh.readlines()
    lines = []
    for lin in fileinput.input(file_name):
        lines.append(lin)
    #
    k,error_type  = list(map(int,lines[0].strip().split()))
    np  = int(lines[1].strip())
    points = []
    for i in range(np):
        line = lines[i+2]
        x,y = list(map(int,line.strip().split()))
        points.append(point.Point2D(i,x,y))
    #
    return k,error_type,points

def get_error_fn(error_type):
    if error_type == 0:
        return mse
    elif error_type == 1:
        return mae

def mse(a,b):
    return a+b

def mae(a,b):
    return max(a,b)

