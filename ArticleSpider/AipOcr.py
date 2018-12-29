# -*- coding: utf-8 -*-

from aip import AipOcr
import json

""" 你的 APPID AK SK """
APP_ID = '11751980'
API_KEY = 'Szhpto3aOa4rf07SRuTkX5Yj'
SECRET_KEY = 'CNOB7dEpnw4HZDCyGubsSlztVqoOkLCG'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = "/Users/liutanqi/Desktop/ArticleSpider/ArticleSpider/table5.jpg"

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}
#
# # 调用通用文字识别接口
result = client.basicAccurate(get_file_content(filePath), options)
print result


# result = json.dumps(result).decode("unicode-escape")
# requestId = result['result'][0]['request_id']
# print requestId
# """ 调用表格识别结果 """
# client.getTableRecognitionResult(requestId)
#
# """ 如果有可选参数 """
# options = {}
# options["result_type"] = "json"
#
# """ 带参数调用表格识别结果 """
# aaa = client.getTableRecognitionResult(requestId, options)
#
# print aaa

#
#
# """ 读取图片 """
#
#
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
#
# image = get_file_content(filePath)
#
# """ 调用表格文字识别 """
# result = client.tableRecognitionAsync(image)
# print result
#

###自定义模板

# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
#
# image = get_file_content('/Users/liutanqi/Desktop/ArticleSpider/ArticleSpider/abcd.jpg')
# templateSign = "676c5ba36cb6352de9a8e26bc5d4b264"
#
# """ 调用自定义模版文字识别 """
# AA = client.custom(image, templateSign)
# print AA


#####表格###


""" 读取图片 """


# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
#
# image = get_file_content(filePath)
#
# """ 调用表格文字识别 """
# result = client.tableRecognitionAsync(image)
# print result
#
# requestId = result['result'][0]['request_id']
#
# """ 调用表格识别结果 """
# # client.getTableRecognitionResult(requestId)
#
# """ 如果有可选参数 """
# options = {}
# options["result_type"] = "excel"
#
# """ 带参数调用表格识别结果 """
# aa = client.getTableRecognitionResult(requestId, options)
# print aa


 # {u'log_id': 153568722632448, u'result': {u'percent': 0, u'ret_code': 1, u'ret_msg': u'\u672a\u5f00\u59cb', u'result_data': u'', u'request_id': u'11751980_450929'}}