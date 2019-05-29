# -*- coding: utf-8 -*
# homepage:https://github.com/LiKunWHU/
# 版权保护，只可以用于科研
# python2.7 ，gdal库与xlwt库请自行匹配


from osgeo import gdal
from gdalconst import *
import xlwt
import os

osdata=[]
# 文件相对路径
osdirs=[]
# 文件绝对路径
ndvi=[]
# ndvi存放

# 读取目录文件，保存子文件名等
def file_name_fun(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(files) #当前路径下所有非目录子文件
        print files.__len__()
        for i in range(files.__len__()):
            osdata.append(root+files[i])
            # osdirs.append(osdirs[i])
    print osdata

# 绝对路径的方式打开
file_name_fun(r'D:/Data/study/models/qixiangEffects/2003-2004/2/')

wb = xlwt.Workbook()

ws = wb.add_sheet('A Test Sheet')
# 创建一个表格，name：A Test Sheet


# 遍历每个img文件
for k in range(osdata.__len__()):
    # print k,'图像'
    gdal.AllRegister()
    filename = osdata[k]
    print filename
    data = gdal.Open(filename, GA_ReadOnly)
    # 查看大小、波段
    print("Size is {} x {} x {}".format(data.RasterXSize,
                                        data.RasterYSize,
                                        data.RasterCount))
    # 将图像读到数组
    lc = data.ReadAsArray()
    print '图像大小（x,y）：'

    # 创建0二维数组
    N = [[0.0]*data.RasterXSize for i in range(data.RasterYSize)]

    count = 0   #计数
    sum  = 0    #累计和

    # 遍历每个像素--NDVI计算公式
    for i in range(data.RasterYSize):
        for j in range(data.RasterXSize):
            # print i,j
            if( (lc[1][i][j]+lc[0][i][j])!=0 or ( lc[1][i][j]-lc[0][i][j]>0) ):
                N[i][j]=    ( float(lc[1][i][j]-lc[0][i][j])  )/  (   float(lc[1][i][j]+lc[0][i][j])   )
                if ( N[i][j]!=0):
                    count=count+1
                    sum = sum+N[i][j]
                # print N[i][j],count,sum

    ave=sum/count
    print k,'--平均值：',ave
    ndvi.append(ave)
    # 写入excel中，注意此时不能保存，因为设置excel打开方式是overwrite!
    ws.write(k, 0, ave)
    ws.write(k, 1,filename)

# 保存excel至一个路径
wb.save('C:/Users/likun3/Desktop/ndvi.xlsx')