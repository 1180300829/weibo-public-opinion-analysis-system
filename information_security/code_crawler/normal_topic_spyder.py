import time
import xlrd
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import excelSave as save
import json


def Transfer_Clicks(driver, scroll_times=5):
    for _ in range(scroll_times):
        time.sleep(5)
        try:
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        except Exception as e:
            print(f"滚动页面时出错: {e}")
    return "Transfer successfully \n"


def isPresent(driver):
    try:
        driver.find_elements(By.CSS_SELECTOR,
                             'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
        return 1
    except Exception:
        return 0


def collect_data(elems, name, yuedu, taolun):
    data = []
    for elem in elems:
        weibo_username = elem.find_elements(By.CSS_SELECTOR, 'h3.m-text-cut')[0].text
        weibo_userlevel = "普通用户"

        try:
            weibo_userlevel_color_class = elem.find_elements(By.CSS_SELECTOR, "i.m-icon")[0].get_attribute(
                "class").replace("m-icon ", "")
            if weibo_userlevel_color_class == "m-icon-yellowv":
                weibo_userlevel = "黄v"
            elif weibo_userlevel_color_class == "m-icon-bluev":
                weibo_userlevel = "蓝v"
            elif weibo_userlevel_color_class == "m-icon-goldv-static":
                weibo_userlevel = "金v"
            elif weibo_userlevel_color_class == "m-icon-club":
                weibo_userlevel = "微博达人"
        except Exception:
            weibo_userlevel = "普通用户"

        weibo_content = elem.find_elements(By.CSS_SELECTOR, 'div.weibo-text')[0].text
        shares = elem.find_elements(By.CSS_SELECTOR, 'i.m-font.m-font-forward + h4')[0].text
        comments = elem.find_elements(By.CSS_SELECTOR, 'i.m-font.m-font-comment + h4')[0].text
        likes = elem.find_elements(By.CSS_SELECTOR, 'i.m-icon.m-icon-like + h4')[0].text
        weibo_time = elem.find_elements(By.CSS_SELECTOR, 'span.time')[0].text

        data.append(
            [weibo_username, weibo_userlevel, weibo_content, shares, comments, likes, weibo_time, name, name, yuedu,
             taolun])
    return data


def get_current_weibo_data(driver, name, yuedu, taolun, maxWeibo):
    data = []
    after = 0
    n = 0
    total_scrolls = 0
    while True:
        before = after
        Transfer_Clicks(driver)
        time.sleep(5)
        elems = driver.find_elements(By.CSS_SELECTOR, 'div.card.m-panel.card9')
        print(f"当前包含微博最大数量：{len(elems)}, n当前的值为：{n}, n值到5说明已无法解析出新的微博")
        after = len(elems)
        total_scrolls += 1
        if after > before:
            n = 0
        if after == before:
            n += 1
        if n == 5 or len(elems) > maxWeibo or total_scrolls > 200:
            print(f"当前关键词最大微博数为：{after}")
            data.extend(collect_data(elems, name, yuedu, taolun))
            break
    return data


def login(driver, username, password):
    try:
        driver.get("https://passport.weibo.cn/signin/login")
        print("开始自动登陆，若出现验证码手动验证")
        time.sleep(3)

        driver.find_element(By.XPATH, "//*[@id='loginName']").send_keys(username)
        driver.find_element(By.XPATH, "//*[@id='loginPassword']").send_keys(password)
        driver.find_element(By.XPATH, "//*[@id='loginAction']").send_keys(Keys.ENTER)
        print("暂停20秒，用于验证码验证")
        time.sleep(20)

        cookies = driver.get_cookies()
        with open('cookie.txt', 'w') as f1:
            f1.write(json.dumps(cookies))
        print("登录成功并保存cookie")
    except Exception as e:
        print(f"登录过程中出错: {e}")


def spider(username, password, driver, book_name_xls, sheet_name_xls, keyword, maxWeibo):
    new_data = []

    if os.path.exists(book_name_xls):
        print("文件已存在，读取现有数据...")
        workbook = xlrd.open_workbook(book_name_xls)
        worksheet = workbook.sheet_by_index(0)
        rows_old = worksheet.nrows
        print(f"现有数据条数: {rows_old}")
    else:
        print("文件不存在，重新创建")
        value_title = [["rid", "用户名称", "微博等级", "微博内容", "微博转发量", "微博评论量", "微博点赞", "发布时间",
                        "搜索关键词", "话题名称", "话题讨论数", "话题阅读数"]]
        save.write_excel_xls(book_name_xls, sheet_name_xls, value_title)
        rows_old = 1  # 标题行

    driver.set_window_size(452, 790)
    driver.get("https://m.weibo.cn/")

    with open('cookie.txt', 'r') as f1:
        cookie = f1.read()

    if cookie:
        cookies = json.loads(cookie)
        for c in cookies:
            driver.add_cookie(c)
        driver.refresh()
        time.sleep(5)

        if isPresent(driver) == 0:
            print("Cookie 失效，重新登录")
            login(driver, username, password)
    else:
        print("没有找到cookie文件，进行初始登录")
        login(driver, username, password)

    while True:
        result = isPresent(driver)
        driver.get('https://m.weibo.cn/')
        print(f'判断页面1成功 0失败 结果是={result}')
        if result == 1:
            break
        else:
            print('页面还没加载出来呢')
            time.sleep(20)

    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@class='m-text-cut']").click()
    time.sleep(2)
    search_box = driver.find_element(By.XPATH, "//*[@type='search']")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    print("话题链接获取完毕，休眠2秒")
    time.sleep(2)
    yuedu_taolun = driver.find_element(By.XPATH, "//h4[@class='m-text-cut']/span").text
    result = yuedu_taolun.split(" ")
    yuedu = result[0]
    taolun = result[1]
    print(yuedu)
    print(taolun)

    time.sleep(2)
    new_data = get_current_weibo_data(driver, keyword, yuedu, taolun, maxWeibo)

    # 插入新数据
    for i, row in enumerate(new_data, start=rows_old):
        new_data[i - rows_old].insert(0, i)

    # 保存所有数据
    save.write_excel_xls_append_norepeat(book_name_xls, new_data)
    print(f"已插入{len(new_data)}条数据")


if __name__ == '__main__':
    username = "你的微博登录名"
    password = "你的密码"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    temp_filename = "高考"
    book_name_xls = "weibodata/" + temp_filename + ".xls"
    sheet_name_xls = '微博数据'
    maxWeibo = 10000
    keywords = ["#" + temp_filename + "#"]
    try:
        for keyword in keywords:
            spider(username, password, driver, book_name_xls, sheet_name_xls, keyword, maxWeibo)
    except KeyboardInterrupt:
        print("爬虫中断，保存已获取的数据...")
        driver.quit()
        print("保存完成，程序已终止。")




