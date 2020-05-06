# BaiDu-AIP-OCR
 use baidu aip to recognize text in pictures

# 一、用到的模块
from PIL import Image
from aip import AipOcr		(pip install baidu-aip)	#调用百度接口

# 二、调用百度aip进行图片文本识别
1、进入网址:https://console.bce.baidu.com/ai/#/ai/ocr/overview/index 创建应用，接口选择文字识别；
2、获取到刚刚创建的应用的：AppID，APIKey，SecretKey分别填入到：        
APP_ID = 'xxxxxxxx'  # 刚才获取的 ID，下同
API_KEY = 'xxxxxxxx'
SECRECT_KEY = 'xxxxxxxx'
3、运行Text_recognition.py即可进行图片文本识别。
