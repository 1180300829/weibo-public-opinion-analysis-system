# coding=gbk
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json


# �ж�ҳ���Ƿ���س���
def isPresent(driver):
    temp = 1
    try:
        driver.find_elements_by_css_selector(
            'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
    except:
        temp = 0
    return temp


# ΢��ˮ����������
def water_army(keyword, username, password, driver, i):
    # cookie��¼
    driver.set_window_size(452, 790)
    # ����������ʹ���������ָ����ַ
    driver.get("https://m.weibo.cn/")
    # �ж��Ƿ�����cookie�ļ�
    f1 = open('cookie.txt')
    cookie = f1.read()
    if cookie == "":  # ���cookieδ����cookie.txt����һ�ε�¼
        # ��������ԭ��cookie
        driver.delete_all_cookies()
        # ʹ���û������뼰��֤���¼
        # ����������ʹ���������ָ����ַ
        driver.set_window_size(452, 790)
        driver.get("https://passport.weibo.cn/signin/login")
        print("��ʼ�Զ���½����������֤���ֶ���֤")
        time.sleep(3)

        elem = driver.find_element_by_xpath("//*[@id='loginName']")
        elem.send_keys(username)
        elem = driver.find_element_by_xpath("//*[@id='loginPassword']")
        elem.send_keys(password)
        elem = driver.find_element_by_xpath("//*[@id='loginAction']")
        elem.send_keys(Keys.ENTER)
        print("��ͣ20�룬������֤����֤")
        time.sleep(20)

        # ��һ�ε�¼��cookieд���ļ�
        cookies = driver.get_cookies()
        f1 = open('cookie.txt', 'w')
        f1.write(json.dumps(cookies))
        f1.close()
    else:

        cookie = json.loads(cookie)
        for c in cookie:
            driver.add_cookie(c)
        # ˢ��ҳ��
        driver.refresh()

    while 1:  # ѭ������Ϊ1�ض�����
        result = isPresent(driver)
        # ���������֤���޷���ת������
        driver.get('https://m.weibo.cn/')
        print('�ж�ҳ��1�ɹ� 0ʧ��  �����=%d' % result)
        if result == 1:
            elems = driver.find_elements_by_css_selector(
                'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
            # return elems #�����װ����������ҳ��
            break
        else:
            print('ҳ�滹û���س�����')
            time.sleep(20)

    time.sleep(2)
    # ���ȶ�λ�����Ͻǵı�д΢����div��ǩ
    driver.find_element_by_xpath("//div[@class='lite-iconf lite-iconf-releas']").click()
    time.sleep(2)
    weibo_context = keyword + " ˮ���������� " + str(i)
    string_begin = 0
    send_weibo(driver, weibo_context, string_begin)
    print(weibo_context)


# ģ���˽��з�΢������
def send_weibo(driver, weibo_string, string_begin):
    # ���ڷ�����΢���к��С�#���������롰#��������Զ�����ѡ������棬Ȼ���쳣��
    # �����ڳ����쳣�󷵻���һ����΢���Ľ���
    try:
        # Ȼ��λ������΢�����ݵ�span��ǩ�µ�textarea��ǩ
        driver.find_element_by_xpath("//span[@class='m-wz-def']/textarea").send_keys(
            weibo_string[string_begin:])  # ����string_begin֮���ַ����е���������
        time.sleep(2)
        #  ���λ�����ϽǷ���΢����a��ǩ
        driver.find_element_by_xpath(
            "//div[@class='m-box m-flex-grow1 m-box-model m-fd-row m-aln-center m-justify-end m-flex-base0']/a").click()
        time.sleep(2)
        print("����һ��΢���ɹ�")
    except:  # ������һ�����棬����΢�����ݵ��ַ�����ȥ�ղŵġ�#���ַ�
        string_begin = string_begin + 1
        driver.back()
        time.sleep(2)
        send_weibo(driver, weibo_string, string_begin)


if __name__ == '__main__':
    username = "15586430583"  # ���΢����¼��
    password = "yutao19981119"  # �������
    driver = webdriver.Chrome()  # ���chromedriver�ĵ�ַ
    temp_filename = "�п�"
    keywords = ["#" + temp_filename + "#"]  # �˴��������ö�����⣬#����Ҫ����
    weibo_num = 100  # ˮ��΢��������
    # �����һ�����
    for keyword in keywords:
        for i in range(weibo_num):
            water_army(keyword, username, password, driver, i)
    print("����ˮ��΢���������")
