import ezdxf
import math
import numpy as np
from scipy.interpolate import BSpline
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
    # get the control points of the spline
    # control_points = np.array(spline.control_points)
    # degree = spline.dxf.degree
    # knots = spline.knots
    # # 计算参数t的范围
    # t_min = knots[degree]
    # t_max = knots[-degree - 1]
    # t_values = np.linspace(t_min, t_max, num)
    # # 生成B-spline曲线
    # spline = BSpline(knots, control_points, degree)
    # # 计算参数t对应的点
    # pts = np.array([spline(t) for t in t_values])
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
        pts = list(polyline.divide(2000))
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
def points2txt(points,fileName = "ccfPath.txt",z = 0.5):
    with open(fileName, "w") as f:
        for p in points:
            f.write(f"{p.x} {p.y} {z} {p.index}\n")
    f.close()

def element2points(points,element, idx):
    dxftype = element.dxftype()

    if element.dxftype() == "LINE":
        line2points(points,element, idx)
    elif element.dxftype() == "LWPOLYLINE":
        lwpolyline2points(points,element, idx)
    elif element.dxftype() == "CIRCLE":
        circle2points(points,element, idx)
    elif element.dxftype() == "ELLIPSE":
        ellipse2points(points,element, idx)
    elif element.dxftype() == "SPLINE":
        spline2points(points,element, idx)
    else:
        print(f"Unknow type: {element.dxftype()}")
