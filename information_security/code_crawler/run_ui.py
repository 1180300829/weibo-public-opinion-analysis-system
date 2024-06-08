# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from selenium import webdriver

from analysis import isPostive
from create_weibo import water_army
from multipattern_matching import all_weibo_to_string, Trie
from normal_topic_spyder import spider

from collections import Counter
import pandas as pd

from seg import init_seg, save_seg
import xlrd

from the_ui import Ui_MainWindow
from visualization import Read_Excel, emotion_pie, level_bar, emotion_bar, level_pie, Read_Excel_keyword, keyword_bar, keyword_pie


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.crawler)
        self.pushButton_2.clicked.connect(self.emotion_analysis)
        self.pushButton_3.clicked.connect(self.keyword_seg)
        self.pushButton_4.clicked.connect(self.visual)
        self.pushButton_5.clicked.connect(self.water_army_attack)
        self.pushButton_6.clicked.connect(self.pattern_matching)

    def crawler(self):
        button = ui.sender().objectName()  # 判断是哪个表下的查询
        if button == 'pushButton':
            if len(self.lineEdit.text()) != 0:
                username = ""  # 你的微博登录名
                password = ""  # 你的密码
                driver = webdriver.Chrome()  # 你的chromedriver的地址
                temp_filename = self.lineEdit.text()
                book_name_xls = "weibodata/" + temp_filename + ".xls"  # 填写你想存放excel的路径，没有文件会自动创建
                sheet_name_xls = '微博数据'  # sheet表名
                maxWeibo = 15000# 设置最多多少条微博
                keywords = ["#" + temp_filename + "#"]  # 此处可以设置多个话题，#必须要加上
                for keyword in keywords:
                    spider(username, password, driver, book_name_xls, sheet_name_xls, keyword, maxWeibo)
                QMessageBox.information(self, "结果", "爬虫结果已存入：" + "weibo_data/" + temp_filename + ".xls中！",
                                        QMessageBox.Yes)
                print("爬虫完成，已保存")

    def emotion_analysis(self):
        button = ui.sender().objectName()  # 判断是哪个表下的查询
        if button == 'pushButton_2':
            if len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                file_path = "weibodata/" + temp_filename + ".xls"
                data = pd.read_excel(file_path)
                moods = []
                count = 1
                for i in data['微博内容']:
                    moods.append(isPostive(i))
                    count += 1
                    print("目前分析到：" + str(count))
                data['情感倾向'] = pd.Series(moods)
                # 此处为覆盖保存
                data.to_excel(file_path)
                QMessageBox.information(self, "结果", "情感分析结果已存入：" + "weibo_data/" + temp_filename + ".xls中！",
                                        QMessageBox.Yes)
                print("情感分析完成，已保存")

    def keyword_seg(self):
        button = ui.sender().objectName()  # 判断是哪个表下的查询
        if button == 'pushButton_3':
            if len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                # 需要进行分词的文件
                cnt = Counter()
                data = pd.read_excel('weibodata/' + temp_filename + '.xls')
                init_seg(temp_filename, cnt, data)
                # 统计词汇出现次数
                word_num = 20  # 次数最多的词汇量
                book_name_xls = "seg_result/" + temp_filename + "话题微博词汇统计.xls"  # 填写你想存放excel的路径，没有文件会自动创建
                sheet_name_xls = '微博数据'  # sheet表名
                save_seg(book_name_xls, sheet_name_xls, cnt, word_num)
                QMessageBox.information(self, "结果", "统计结果已存入：" + "seg_result/" + temp_filename + "话题微博词汇统计.xls中！",
                                        QMessageBox.Yes)
                print("词汇统计完成，已保存")

    def visual(self):
        button = ui.sender().objectName()  # 判断是哪个表下的查询
        if button == 'pushButton_4':
            if len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                filename = self.lineEdit.text()
                # 导入Excel 文件
                data = xlrd.open_workbook("weibodata/" + temp_filename + ".xls")
                # 载入第一个表格
                table = data.sheets()[0]
                tables = []
                Read_Excel(table, tables)
                emotion_bar(tables, temp_filename)
                emotion_pie(tables, temp_filename)
                level_bar(tables, temp_filename)
                level_pie(tables, temp_filename)

                # 词汇统计可视化
                temp_filename = temp_filename + "话题微博词汇统计"  # 文件名
                # 导入Excel 文件
                data = xlrd.open_workbook("seg_result/" + temp_filename + ".xls")
                # 载入第一个表格
                table = data.sheets()[0]
                tables = []
                Read_Excel_keyword(table, tables)
                keyword_bar(tables, temp_filename)
                keyword_pie(tables, temp_filename)
                QMessageBox.information(self, "结果",
                                        "图形结果已存入：" + "chart_emotion, chart_keybord, chart_level/" + filename + "相关的html文件中！",
                                        QMessageBox.Yes)
                print("图形绘制完成，已保存")

    def water_army_attack(self):
        button = ui.sender().objectName()  # 判断是哪个表下的查询
        if button == 'pushButton_5':
            if len(self.lineEdit.text()) != 0 and len(self.lineEdit_2.text()) != 0:
                username = "15586430583"  # 你的微博登录名
                password = "yutao19981119"  # 你的密码
                driver = webdriver.Chrome()  # 你的chromedriver的地址
                temp_filename = self.lineEdit.text()
                keywords = ["#" + temp_filename + "#"]  # 此处可以设置多个话题，#必须要加上
                weibo_num = int(self.lineEdit_2.text())  # 水军微博的数量
                # 载入第一个表格
                for keyword in keywords:
                    for i in range(weibo_num):
                        water_army(keyword, username, password, driver, i)
                QMessageBox.information(self, "结果", "所有水军攻击微博已发送完毕", QMessageBox.Yes)
                print("所有水军攻击微博已发送完毕")


    def pattern_matching(self):
        button = ui.sender().objectName()  # 判断是哪个表下的查询
        if button == 'pushButton_6':
            if len(self.lineEdit_3.text()) != 0 and len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                the_input = self.lineEdit_3.text()
                keywords = []
                if the_input.find("，"):  # 多模式匹配需要隔开
                    keywords = the_input.split("，")
                else:
                    keywords = keywords.append(the_input)
                data = pd.read_excel('weibodata/' + temp_filename + '.xls')
                all_weibo = ""
                all_weibo = all_weibo_to_string(all_weibo, data)
                model = Trie(keywords)
                # defaultdict(<class 'list'>, {'不知': [(0, 1)], '不觉': [(3, 4)], '忘了爱': [(13, 15)]})
                list = model.search(all_weibo)
                the_result = ""
                for i in list:
                    the_result = the_result + "关键词:" +  i + "\t出现次数:" + str(len(list[i])) + "\n"
                print(the_result)
                self.textBrowser.setText(the_result)
                QMessageBox.information(self, "结果", "多模式匹配成功,结果已展示出来", QMessageBox.Yes)
                print("多模式匹配成功")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.setWindowTitle('微博舆情分析')
    ui.show()
    sys.exit(app.exec_())

