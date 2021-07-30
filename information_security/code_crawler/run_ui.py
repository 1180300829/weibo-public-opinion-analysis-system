# coding=gbk
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
        button = ui.sender().objectName()  # �ж����ĸ����µĲ�ѯ
        if button == 'pushButton':
            if len(self.lineEdit.text()) != 0:
                username = "15586430583"  # ���΢����¼��
                password = "yutao19981119"  # �������
                driver = webdriver.Chrome()  # ���chromedriver�ĵ�ַ
                temp_filename = self.lineEdit.text()
                book_name_xls = "weibodata/" + temp_filename + ".xls"  # ��д������excel��·����û���ļ����Զ�����
                sheet_name_xls = '΢������'  # sheet����
                maxWeibo = 20  # ������������΢��
                keywords = ["#" + temp_filename + "#"]  # �˴��������ö�����⣬#����Ҫ����
                for keyword in keywords:
                    spider(username, password, driver, book_name_xls, sheet_name_xls, keyword, maxWeibo)
                QMessageBox.information(self, "���", "�������Ѵ��룺" + "weibo_data/" + temp_filename + ".xls�У�",
                                        QMessageBox.Yes)
                print("������ɣ��ѱ���")

    def emotion_analysis(self):
        button = ui.sender().objectName()  # �ж����ĸ����µĲ�ѯ
        if button == 'pushButton_2':
            if len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                file_path = "weibodata/" + temp_filename + ".xls"
                data = pd.read_excel(file_path)
                moods = []
                count = 1
                for i in data['΢������']:
                    moods.append(isPostive(i))
                    count += 1
                    print("Ŀǰ��������" + str(count))
                data['�������'] = pd.Series(moods)
                # �˴�Ϊ���Ǳ���
                data.to_excel(file_path)
                QMessageBox.information(self, "���", "��з�������Ѵ��룺" + "weibo_data/" + temp_filename + ".xls�У�",
                                        QMessageBox.Yes)
                print("��з�����ɣ��ѱ���")

    def keyword_seg(self):
        button = ui.sender().objectName()  # �ж����ĸ����µĲ�ѯ
        if button == 'pushButton_3':
            if len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                # ��Ҫ���зִʵ��ļ�
                cnt = Counter()
                data = pd.read_excel('weibodata/' + temp_filename + '.xls')
                init_seg(temp_filename, cnt, data)
                # ͳ�ƴʻ���ִ���
                word_num = 20  # �������Ĵʻ���
                book_name_xls = "seg_result/" + temp_filename + "����΢���ʻ�ͳ��.xls"  # ��д������excel��·����û���ļ����Զ�����
                sheet_name_xls = '΢������'  # sheet����
                save_seg(book_name_xls, sheet_name_xls, cnt, word_num)
                QMessageBox.information(self, "���", "ͳ�ƽ���Ѵ��룺" + "seg_result/" + temp_filename + "����΢���ʻ�ͳ��.xls�У�",
                                        QMessageBox.Yes)
                print("�ʻ�ͳ����ɣ��ѱ���")

    def visual(self):
        button = ui.sender().objectName()  # �ж����ĸ����µĲ�ѯ
        if button == 'pushButton_4':
            if len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                filename = self.lineEdit.text()
                # ����Excel �ļ�
                data = xlrd.open_workbook("weibodata/" + temp_filename + ".xls")
                # �����һ�����
                table = data.sheets()[0]
                tables = []
                Read_Excel(table, tables)
                emotion_bar(tables, temp_filename)
                emotion_pie(tables, temp_filename)
                level_bar(tables, temp_filename)
                level_pie(tables, temp_filename)

                # �ʻ�ͳ�ƿ��ӻ�
                temp_filename = temp_filename + "����΢���ʻ�ͳ��"  # �ļ���
                # ����Excel �ļ�
                data = xlrd.open_workbook("seg_result/" + temp_filename + ".xls")
                # �����һ�����
                table = data.sheets()[0]
                tables = []
                Read_Excel_keyword(table, tables)
                keyword_bar(tables, temp_filename)
                keyword_pie(tables, temp_filename)
                QMessageBox.information(self, "���",
                                        "ͼ�ν���Ѵ��룺" + "chart_emotion, chart_keybord, chart_level/" + filename + "��ص�html�ļ��У�",
                                        QMessageBox.Yes)
                print("ͼ�λ�����ɣ��ѱ���")

    def water_army_attack(self):
        button = ui.sender().objectName()  # �ж����ĸ����µĲ�ѯ
        if button == 'pushButton_5':
            if len(self.lineEdit.text()) != 0 and len(self.lineEdit_2.text()) != 0:
                username = "15586430583"  # ���΢����¼��
                password = "yutao19981119"  # �������
                driver = webdriver.Chrome()  # ���chromedriver�ĵ�ַ
                temp_filename = self.lineEdit.text()
                keywords = ["#" + temp_filename + "#"]  # �˴��������ö�����⣬#����Ҫ����
                weibo_num = int(self.lineEdit_2.text())  # ˮ��΢��������
                # �����һ�����
                for keyword in keywords:
                    for i in range(weibo_num):
                        water_army(keyword, username, password, driver, i)
                QMessageBox.information(self, "���", "����ˮ������΢���ѷ������", QMessageBox.Yes)
                print("����ˮ������΢���ѷ������")


    def pattern_matching(self):
        button = ui.sender().objectName()  # �ж����ĸ����µĲ�ѯ
        if button == 'pushButton_6':
            if len(self.lineEdit_3.text()) != 0 and len(self.lineEdit.text()) != 0:
                temp_filename = self.lineEdit.text()
                the_input = self.lineEdit_3.text()
                keywords = []
                if the_input.find("��"):  # ��ģʽƥ����Ҫ����
                    keywords = the_input.split("��")
                else:
                    keywords = keywords.append(the_input)
                data = pd.read_excel('weibodata/' + temp_filename + '.xls')
                all_weibo = ""
                all_weibo = all_weibo_to_string(all_weibo, data)
                model = Trie(keywords)
                # defaultdict(<class 'list'>, {'��֪': [(0, 1)], '����': [(3, 4)], '���˰�': [(13, 15)]})
                list = model.search(all_weibo)
                the_result = ""
                for i in list:
                    the_result = the_result + "�ؼ���:" +  i + "\t���ִ���:" + str(len(list[i])) + "\n"
                print(the_result)
                self.textBrowser.setText(the_result)
                QMessageBox.information(self, "���", "��ģʽƥ��ɹ�,�����չʾ����", QMessageBox.Yes)
                print("��ģʽƥ��ɹ�")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.setWindowTitle('΢���������')
    ui.show()
    sys.exit(app.exec_())