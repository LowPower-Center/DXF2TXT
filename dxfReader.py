
import os
from utils import *
# This program show how to convert dxf elements to a list of points
def process_dxf(dxf_file):
    # point = x ,y , z, index
    points = []
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    idx = 0
    type_set = set()
    for e in msp:
        # get the coordinates of the entity
        type_set.add(e.dxftype())
        element2points(points,e, idx)
        idx += 1
    output_name = dxf_file.split('.')[0] + '.txt'
    points2txt(points,output_name)
    print(type_set)
# search all .dxf in the current directory

for item in os.listdir():
    if item.endswith('.dxf'):
        process_dxf(item)




