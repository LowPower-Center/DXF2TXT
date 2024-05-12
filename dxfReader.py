
import os
from utils import *
# This program show how to convert dxf elements to a list of points
def process_dxf(dxf_file,output_file):
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
    if output_file is None:
        output_name = dxf_file.split('.')[0] + '.txt'
    else:
        output_name = output_file
    points2txt(points,output_name)
    print(type_set)
# search all .dxf in the current directory




# add a var to process certain file
from optparse import OptionParser

def main():
    """
    Main Cura entry point. Parses arguments, and starts GUI or slicing process depending on the arguments.
    """
    parser = OptionParser(usage="usage: %prog [options] <filename>.dxf")
    parser.add_option("-o", "--output", action="store", type="string", dest="output",
                      help="path to write txt file to")

    (options, args) = parser.parse_args()
    dxf_file = args[0]
    output_name = options.output
    if dxf_file is not None:
        process_dxf(dxf_file,output_name)
if __name__ == '__main__':
    main()



