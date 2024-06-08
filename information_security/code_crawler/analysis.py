import pandas as pd
from snownlp import SnowNLP

# 本地情感分析函数
def isPostive(text):
    try:
        s = SnowNLP(text)
        # 使用分析结果的情感属性判断情感倾向
        if s.sentiments > 0.5:
            return "积极"
        else:
            return "消极"
    except Exception as e:
        print(f"分析文本时出错：{text}, 错误信息：{e}")
        return "未知"

if __name__ == '__main__':
    # 修改文件扩展名为 .xlsx
    file_path = 'weibodata/高考.xlsx'
    try:
        print(f"开始读取文件：{file_path}")
        data = pd.read_excel(file_path)
        print("文件读取成功")
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        exit(1)
    except Exception as e:
        print(f"读取文件时出错: {e}")
        exit(1)

    moods = []  # 存储情感分析结果
    total = len(data)
    print(f"总记录数：{total}")

    for count, text in enumerate(data['微博内容'], start=1):
        try:
            moods.append(isPostive(text))  # 进行情感分析并存储结果
            print(f"目前分析到：{count}/{total}")
        except Exception as e:
            print(f"分析文本时出错：{text}, 错误信息：{e}")
            moods.append("未知")  # 如果分析失败，标记为"未知"

    try:
        data['情感倾向'] = pd.Series(moods)  # 将情感分析结果添加到新列
        print("情感分析结果已添加到数据中")

        # 覆盖保存文件
        data.to_excel(file_path, index=False)
        print("分析完成，已保存")
    except Exception as e:
        print(f"保存文件时出错: {e}")


