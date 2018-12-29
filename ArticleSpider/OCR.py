# -*- coding: utf-8 -*-

import os
import subprocess


# from PIL import Image
# from PIL import ImageEnhance
# I = Image.open('/Users/liutanqi/Desktop/ArticleSpider/ArticleSpider/22222.png')
# I.show()
# L = I.convert('L')  # 转化为灰度图
# L = I.convert('1')  # 转化为二值化图
# # L = ImageEnhance.Sharpness(L).enhance(3)
# #
# L.show()


import pytesseract
from PIL import Image

# open image
image = Image.open('/Users/liutanqi/Desktop/ArticleSpider/ArticleSpider/22222.png')
code = pytesseract.image_to_string(image, lang='chi_sim')
print code

# def image_to_string(img, cleanup=True, plus=''):
#     # cleanup为True则识别完成后删除生成的文本文件
#     # plus参数为给tesseract的附加高级参数
#     subprocess.check_output('tesseract ' + img + ' ' +
#                             img + ' ' + plus, shell=True)  # 生成同名txt文件
#     text = ''
#     with open(img + '.txt', 'r') as f:
#         text = f.read().strip()
#     if cleanup:
#         os.remove(img + '.txt')
#     return text
#
#
#
#
# print(image_to_string('/Users/liutanqi/Desktop/ArticleSpider/ArticleSpider/22222.png',
#                       lang='chi_sim'))  # 打印识别出的文本，删除txt文件

# from PIL import Image
#
# img = Image.open('/Users/liutanqi/Desktop/ArticleSpider/ArticleSpider/22222.png')  # 读入图片
# img = img.convert("RGBA")
#
# pixdata = img.load()
#
# # 二值化
#
# for y in xrange(img.size[1]):
#     for x in xrange(img.size[0]):
#         if pixdata[x, y][0] < 90:
#             pixdata[x, y] = (0, 0, 0, 255)
# #
# for y in xrange(img.size[1]):
#     for x in xrange(img.size[0]):
#         if pixdata[x, y][1] < 136:
#             pixdata[x, y] = (0, 0, 0, 255)
#
# for y in xrange(img.size[1]):
#     for x in xrange(img.size[0]):
#         if pixdata[x, y][2] > 0:
#             pixdata[x, y] = (255, 255, 255, 255)
#
# img.save("input-black.gif", "GIF")
#
# # 放大图像 方便识别
# im_orig = Image.open('input-black.gif')
# big = im_orig.resize((2000, 1000), Image.NEAREST)
