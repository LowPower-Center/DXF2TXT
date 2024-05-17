# DXF2TXT
本程序用于将dxf文件转换为txt文件，这个转换会降低路径的精度，不是无损的。主要用于生成3D打印路径。

每行有4个值：x y z index

单位是mm,具有相同index的点在同一条多段线上

例如：

0 0 0 1

1 1 0 1

表示从(0,0)到(1,1)的一条线段

# usage
将所有文件下载到一个文件夹，然后运行dxfReader.py文件

程序会把运行目录下所有能找到的dxf转换为同名txt文件

# tips

绘制dxf的时候，多段线应该使用polyline绘制，而不是若干line的组合。

最理想的情况是，dxf的元素中只包含polyline/lwpolyline/spline，不包含其他元素。

# requirements

python3

ezdxf

pyinstaller
