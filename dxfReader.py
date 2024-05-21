import ezdxf
# This program show how to convert dxf elements to a list of points
import math
from ezdxf import path
from ezdxf.math import ConstructionPolyline
# This program show how to convert dxf elements to a list of points


class Point:
    def __init__(self, x, y, z, index):
        self.x = x
        self.y = y
        self.z = z
        self.index = index

def spline2points(points,spline, idx,num = 50):
    if spline is not None:
        p = path.make_path(spline)
        polyline = ConstructionPolyline(p.flattening(0.01))
        # this also works for polylines including bulges (arcs)
        pts = list(polyline.divide(2000))
    for point in pts:
        x = point[0]
        y = point[1]
        z = point[2]
        points.append(Point(x, y, z, idx))

def ellipse2points(points,ellipse, idx, num = 50):
    # get the center of the ellipse
    x = ellipse.dxf.center[0]
    y = ellipse.dxf.center[1]
    z = ellipse.dxf.center[2]
    # get the major axis of the ellipse
    a = (ellipse.dxf.major_axis[0]**2 +ellipse.dxf.major_axis[1]**2)**0.5
    # get the minor axis of the ellipse
    b = a*ellipse.dxf.ratio
    # get the ratio of the ellipse
    ratio = ellipse.dxf.major_axis.angle
    # get the number of points to be generated
    n = num
    # generate the points
    start_point = Point(x + a*math.cos(ratio), y+a*math.cos(ratio), z, idx)
    for i in range(n):
        theta = 2 * math.pi * i / n
        px = x + a * math.cos(theta) * math.cos(ratio) - b * math.sin(theta) * math.sin(ratio)
        py = y + a * math.cos(theta) * math.sin(ratio) + b * math.sin(theta) * math.cos(ratio)
        points.append(Point(px, py, z, idx))


def circle2points(points,circle, idx ,num = 50,):
    # get the center of the circle
    x = circle.dxf.center[0]
    y = circle.dxf.center[1]
    z = circle.dxf.center[2]
    # get the radius of the circle
    r = circle.dxf.radius
    # get the number of points to be generated
    n = num
    # generate the points
    start_point = Point(x + r, y, z, idx)
    for i in range(n):
        px = x + r * math.cos(2 * math.pi * i / n)
        py = y + r * math.sin(2 * math.pi * i / n)
        points.append(Point(px, py, z, idx))
    points.append(start_point)

def lwpolyline2points(points,lwpolyline, idx):
    if lwpolyline is not None:
        p = path.make_path(lwpolyline)
        polyline = ConstructionPolyline(p.flattening(0.01))
        # this also works for polylines including bulges (arcs)
        pts = list(polyline.divide(1000))
    for point in pts:
        x = point[0]
        y = point[1]
        z = point[2]
        points.append(Point(x, y, z, idx))


def line2points(points,line, idx):
    # get the start point of the line
    x1 = line.dxf.start[0]
    y1 = line.dxf.start[1]
    z1 = line.dxf.start[2]
    # get the end point of the line
    x2 = line.dxf.end[0]
    y2 = line.dxf.end[1]
    z2 = line.dxf.end[2]
    points.append(Point(x1, y1, z1, idx))
    points.append(Point(x2, y2, z2, idx))
def points2txt(points,fileName = "ccfPath.txt",z_list = None):
    if z_list is not None:
        assert len(z_list) == 3
        assert z_list[0] < z_list[1]
        assert z_list[2] < z_list[1] - z_list[0]
        z = z_list[0]
        end = z_list[1]
        step = z_list[2]
        index = 0
        with open(fileName, "w") as f:
            while z < end:
                for p in points:
                    f.write(f"{p.x} {p.y} {z} {p.index+index}\n")
                z += step
                index += 1
    else:
        with open(fileName, "w") as f:
            for p in points:
                f.write(f"{p.x} {p.y} {p.z} {p.index}\n")
    f.close()

def element2points(points,element, idx):
    dxftype = element.dxftype()

    if element.dxftype() == "LINE":
        line2points(points,element, idx)
    elif element.dxftype() == "LWPOLYLINE" or element.dxftype() == "POLYLINE":
        lwpolyline2points(points,element, idx)
    elif element.dxftype() == "CIRCLE":
        circle2points(points,element, idx)
    elif element.dxftype() == "ELLIPSE":
        ellipse2points(points,element, idx)
    elif element.dxftype() == "SPLINE":
        spline2points(points,element, idx)
    else:
        print(f"Unknow type: {element.dxftype()}")


def process_dxf(dxf_file,output_file,z_list = None):
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
    points2txt(points,output_name,z_list)
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
    parser.add_option("-z", "--z_list", action="store", type="string", dest="z_list",
                      help="z_list to generate multi layer txt file")

    (options, args) = parser.parse_args()
    dxf_file = args[0]
    output_name = options.output
    if dxf_file is not None:
        if options.z_list is not None:
            z_list = options.z_list.split(',')
            z_list = [float(z) for z in z_list]
            process_dxf(dxf_file,output_name,z_list)
        else:
            process_dxf(dxf_file,output_name)
if __name__ == '__main__':
    main()



