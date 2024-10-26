# DXF2TXT
本程序用于将dxf文件转换为txt文件。主要用于生成3D打印路径。

每行有4个值：x y z index

单位是mm,具有相同index的点在同一条多段线上

例如：

0 0 0 1

1 1 0 1

表示在z=0高度上从(0,0)到(1,1)的一条线段

# usage
可以使用pyinstall打包本文件，用法为 


pyinstaller -F dxfReader.py


若要使用，则为

./dxfReader.exe -o output.txt input.dxf

或者

./dxfReader.exe -o output.txt -f input1.dxf -f input2.dxf -f input3.dxf ...

# tips

程序运行后会输出dxf中包含的所有图元类型

重复运行程序不会覆盖输出文件，为避免重复建议自查生成的txt

# requirements

python3

ezdxf

pyinstaller
