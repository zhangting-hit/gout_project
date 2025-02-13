# -*- coding = utf-8 -*-
# -*- coding: gb2312 -*-
# @Time  : 2024/01/22 14:33
# @Author : 张听
# @File : changeFileName.py
# @Software: PyCharm
import os


def getfiles():
    filenames = os.listdir("D:/Users/Desktop/masks/0")
    for filename in filenames:
        # 修改文件名中的空格为下划线，并重命名文件
        file_path = "D:/Users/Desktop/masks/0/" + filename
        new_file_name = filename.replace('_mask', '')
        new_file_path = "D:/Users/Desktop/masks/0/" + filename.replace('_mask', '')
        os.rename(file_path, new_file_path)
        print(f"Renamed file: {filename} -> {new_file_name}")
    print(filenames)


if __name__ == '__main__':
    getfiles()
