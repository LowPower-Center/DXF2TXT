import ezdxf
# This program show how to convert dxf elements to a list of points
import math
from ezdxf import path
from ezdxf.math import ConstructionPolyline
from fontTools.ttx import process


# This program show how to convert dxf elements to a list of points


class Point:
    def __init__(self, x, y, z, index):
        self.x = x
        self.y = y
        self.z = z
        self.index = index

def is_close(p1,p2,tol = 0.01):
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2 < tol**2

def merge_points(pts_lst, tol = 0.01):
    merged = []
    global_index = 0

    while pts_lst:
        # 从列表中取出一条线
        current_line = pts_lst.pop(0)
        merged_line = current_line

        # 尝试和剩下的线合并
        i = 0
        while i < len(pts_lst):
            other_line = pts_lst[i]
            # 当前线的最后一个点和另一条线的第一个点比较
            if is_close(merged_line[-1],other_line[0], tol):
                # 如果连接起来，则合并线段
                merged_line += other_line[1:]
                del pts_lst[i]
                i = 0
            # 另一种情况：当前线的第一个点和另一条线的最后一个点比较
            elif is_close(merged_line[0],other_line[-1], tol):
                # 如果连接起来，则合并线段
                merged_line = other_line[:-1] + merged_line
                del pts_lst[i]
                i = 0
            # 另一种情况：当前线的第一个点和另一条线的第一个点比较
            elif is_close(merged_line[0],other_line[0], tol):
                # 如果连接起来，则合并线段
                merged_line = other_line[::-1] + merged_line
                del pts_lst[i]
                i = 0
            # 另一种情况：当前线的最后一个点和另一条线的最后一个点比较
            elif is_close(merged_line[-1],other_line[-1], tol):
                # 如果连接起来，则合并线段
                merged_line += other_line[::-1]
                del pts_lst[i]
                i = 0
            else:
                i += 1

        # 更新合并后线段的点的 index
        for point in merged_line:
            point.index = global_index
        merged.extend(merged_line)
        global_index += 1

    return merged, global_index

def arc_to_points(arc, idx,tol = 0.01):
    # 使用 flattening 方法将弧线转为点集，tolerance 控制离散化精度
    path = arc.flattening(tol)
    points = [Point(p.x, p.y, p.z,idx) for p in path]
    return points

def spline2points(points,spline, idx,num = 150):
    if spline is not None:
        p = path.make_path(spline)
        polyline = ConstructionPolyline(p.flattening(0.01))
        # this also works for polylines including bulges (arcs)
        pts = list(polyline.divide(num))
    for point in pts:
        x = point[0]
        y = point[1]
        z = point[2]
        points.append(Point(x, y, z, idx))

def ellipse2points(points,ellipse, idx, num = 150):
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


def circle2points(points,circle, idx ,num = 150,):
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

def lwpolyline2points(points,lwpolyline, idx,num=150):
    if lwpolyline is not None:
        p = path.make_path(lwpolyline)
        polyline = ConstructionPolyline(p.flattening(0.01))
        # this also works for polylines including bulges (arcs)
        pts = list(polyline.divide(num))
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


def points2txt(points,fileName = "ccfPath.txt",z_list = None,mode = "w"):
    points,_add = merge_points(points)
    index = 0
    if z_list is not None:
        with open(fileName, mode) as f:
            for z in z_list:
                for p in points:
                    f.write(f"{p.x} {p.y} {z} {p.index+index}\n")
                index += _add
    else:
        with open(fileName, mode) as f:
            for p in points:
                f.write(f"{p.x} {p.y} {p.z} {p.index}\n")
    f.close()

def element2points(element, idx):
    points = []
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
    elif element.dxftype() == "ARC":
        points.extend(arc_to_points(element, idx))
    else:
        print(f"Unknow type: {element.dxftype()}")
    return points


def process_dxf(dxf_file,output_file,z_list = None,mode="w"):
    # point = x ,y , z, index
    pts_lst = []
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    idx = 0
    type_set = set()
    for e in msp:
        # get the coordinates of the entity
        type_set.add(e.dxftype())
        pts_lst.append(element2points(e, idx))
        idx += 1
    if output_file is None:
        output_name = dxf_file.split('.')[0] + '.txt'
    else:
        output_name = output_file
    points2txt(pts_lst,output_name,z_list,mode)
    print(type_set)
# search all .dxf in the current directory

def process_zlist(options):
    z_list = options.z_list
    z_list = z_list.split(',')
    z_list = [float(z) for z in z_list]
    if len(z_list) == 3:
        if z_list[1] > z_list[0] and z_list[1]-z_list[0] >= z_list[2]:
            z_list = [z_list[0] + i*z_list[2] for i in range(int((z_list[1] - z_list[0])/z_list[2] + 1))]
    return z_list

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
    parser.add_option("-f", "--file", action="append", type="string", dest="file",)

    (options, args) = parser.parse_args()

    output_name = options.output
    if args :  # process single file
        dxf_file = args[0]
        if options.z_list is not None:
            process_dxf(dxf_file,output_name,process_zlist(options))
        else:
            process_dxf(dxf_file,output_name)
    else:
        if options.file is not None:
            if options.z_list is not None:
                z_list = options.z_list.split(',')
                z_origin = [float(z) for z in z_list]
            else:
                raise ValueError("z_list is required for multiple files")
            if options.output is None:
                raise ValueError("outputfilename is required for multiple files")
            for i,f in enumerate(options.file):
                #z_list = [z_origin[0] + i*z_origin[2] + j*z_origin[2]*len(options.file) for j in range(int((z_origin[1] - z_origin[0])/z_origin[2]/len(options.file) + 1))]
                process_dxf(f,output_name,process_zlist(options),mode="a")

        else:
            raise ValueError("No file is provided")

if __name__ == '__main__':
    main()



