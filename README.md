# DXF2TXT
本程序用于将dxf文件转换为txt文件，这个转换会降低路径的精度，不是无损的。主要用于生成3D打印路径。

每行有4个值：x y z index

单位是mm,具有相同index的点在同一条多段线上

例如：

0 0 0 1

1 1 0 1

表示从(0,0)到(1,1)的一条线段

# usage
可以使用pyinstall打包本文件，用法为 


pyinstaller -F dxfReader.py


若要使用，则为

./dxfReader.exe -o output.txt input.dxf

或者

./dxfReader.exe -o output.txt -f input1.dxf -f input2.dxf -f input3.dxf ...

# tips

最理想的情况:
dxf的元素中只包含polyline/lwpolyline/spline，不包含其他元素。

目前可以对多个line进行合并，或者混合类型合并

# requirements

python3

ezdxf

pyinstaller
