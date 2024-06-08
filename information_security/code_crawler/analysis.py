from aip import AipNlp
import pandas as pd
#为了提高效率，我将使用本地算法解决问题，频繁的调用根本不具有实用性，所以原有的代码弃用
# # 调用百度的ai接口进行情感分析
# def isPostive(text):
#     APP_ID = '24359968'
#     API_KEY = '9SbGCCXdhu2GvEGo6WS3qVLV'
#     SECRET_KEY = 'x9EUbsSkg9aX2bBlBdnDAU2Fl4RTAnAX'
#
#     client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
#     try:
#         if client.sentimentClassify(text)['items'][0]['positive_prob'] > 0.5:
#             return "积极"
#         else:
#             return "消极"
#     except:
#         return "积极"
#
#
# if __name__ == '__main__':
#     # 读取文件，注意修改文件路径
#     file_path = 'weibodata/高考.xls'
#     data = pd.read_excel(file_path)
#     moods = []
#     count = 1
#     for i in data['微博内容']:
#         moods.append(isPostive(i))
#         count += 1
#         print("目前分析到：" + str(count))
#     data['情感倾向'] = pd.Series(moods)
#
#     # 此处为覆盖保存
#     data.to_excel(file_path)
#     print("分析完成，已保存")

import pandas as pd
from textblob import TextBlob

# 本地情感分析函数
def isPostive(text):
    analysis = TextBlob(text)
    # 使用分析结果的 polarity 属性判断情感倾向
    if analysis.sentiment.polarity > 0:
        return "积极"
    else:
        return "消极"

if __name__ == '__main__':
    # 读取文件，注意修改文件路径
    file_path = 'weibodata/高考.xls'
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"读取文件时出错: {e}")
        exit(1)

    moods = []  # 存储情感分析结果
    total = len(data)
    for count, text in enumerate(data['微博内容'], start=1):
        moods.append(isPostive(text))  # 进行情感分析并存储结果
        print(f"目前分析到：{count}/{total}")

    data['情感倾向'] = pd.Series(moods)  # 将情感分析结果添加到新列

    # 覆盖保存文件
    try:
        data.to_excel(file_path, index=False)
        print("分析完成，已保存")
    except Exception as e:
        print(f"保存文件时出错: {e}")


