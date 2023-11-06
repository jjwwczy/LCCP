import requests
import lxml
from bs4 import BeautifulSoup
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
import pdfkit
import pyperclip
import glob
import os
from docx import Document
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
c_path = 'C://Users/liming/PycharmProjects/36_city/chromedriver.exe'
re_sen = r'.*gov.cn/.*(.html|.htm|content.*|uuid.*|[0-9]+.aspx|.asp\?id.*|index\?code=[0-9]+|action\?messagekey=[0-9]+)'

def chrome_init():
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # option.add_argument("--window-size=1920,1080")
    # option.add_argument("--disable-extensions")
    # option.add_argument("--headless")
    # option.add_argument("--disable-gpu")
    # option.add_argument("--disable-software-rasterizer")
    # option.add_argument('--no-sandbox')
    # option.add_argument('--ignore-certificate-errors')
    # option.add_argument('--allow-running-insecure-content')
    # option.add_argument("blink-settings=imagesEnabled=false")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=option)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined})'})
    return driver

def get_link_1(city, input_url, key_word, button, num_page, link_type="href"): # 下一页，查看更多
# city = '北京'
# key_word = ('低碳试点', '绿色低碳', '建筑节能', '生态文明建设', '低碳技术',
#             '节能减排', '节能监察', '节能监测', '节能信息')
# website = 'http://www.beijing.gov.cn/'
# c_path = 'C://Users/liming/PycharmProjects/36_city/chromedriver.exe'
# 创建一个Chrome浏览器实例
# 定义第一页的URL
    valid_link = list()
    count = 0
    driver = chrome_init()
    for c in key_word:
        print("=====当前处理城市：{}；当前关键词：{}=====".format(city, c))
        # driver = webdriver.Chrome(c_path)
        url = input_url.format(c, c, c, c)
        driver.get(url)
        time.sleep(3)
        eleByClass = driver.find_elements(By.TAG_NAME, 'a')
        for i in eleByClass:
            href = i.get_attribute(link_type)
            href = str(href)
            if re.search(re_sen, href):
                if href not in valid_link:
                    valid_link.append(href)
                    # print(href)
        for ii in range(num_page-1):
            try:
                # 查找下一页按钮并点击它
                next_button = driver.find_element(By.XPATH, value=button)
                next_button.click()
                time.sleep(2)
                eleByClass = driver.find_elements(By.TAG_NAME, 'a')
                for i in eleByClass:
                    href = i.get_attribute(link_type)
                    href = str(href)
                    if re.search(re_sen, href):
                        if href not in valid_link:
                            valid_link.append(href)
                            # print(href)
            except:
                # 关闭浏览器实例
                # driver.quit()
                break
        count = count + ii + 2
        # if ii >= (num_page-2):
    driver.quit()
    print("====={}城市共打开{}页网页，获取链接{}个=====".format(city, count, valid_link.__len__()))
    if (valid_link.__len__() <= 10):
        print("xxxx{}城市无法获取网页链接！！！！xxxx".format(city))
    # print("-----------------分割线---------------------")

    file = open('网页地址/{}_网页地址_{}.txt'.format(city, valid_link.__len__()), 'w')
    for l in valid_link:
        file.write(str(l))
        file.write('\n')
    file.close()
    return valid_link, count


def get_link_2(city, input_url, key_word, button_1, button_2, num_page, link_type="href"):
    valid_link = list()
    count = 0
    driver = chrome_init()
    for c in key_word:
        print("=====当前处理城市：{}；当前关键词：{}=====".format(city, c))

        url = input_url.format(c, c, c, c)
        driver.get(url)
        time.sleep(3)
        eleByClass = driver.find_elements(By.TAG_NAME, 'a')
        for i in eleByClass:
            href = i.get_attribute(link_type)
            href = str(href)
            if re.search(re_sen, href):
                if href not in valid_link:
                    valid_link.append(href)
                    # print(href)
        for ii in range(2, num_page+1):
            try:
                # 查找下一页按钮并点击它
                driver.find_element(By.XPATH, value=button_1).clear()
                # next_button.click()
                driver.find_element(By.XPATH, value=button_1).send_keys(ii)
                driver.find_element(By.XPATH, value=button_2).click()
                time.sleep(2)
                eleByClass = driver.find_elements(By.TAG_NAME, 'a')
                for i in eleByClass:
                    href = i.get_attribute(link_type)
                    href = str(href)
                    if re.search(re_sen, href):
                        if href not in valid_link:
                            valid_link.append(href)
                            # print(href)
            except:
                # 关闭浏览器实例
                # driver.quit()
                break
        count = count + ii
        # if ii >= (num_page):
    driver.quit()
    print("====={}城市共打开{}页网页，获取链接{}个=====".format(city, count, valid_link.__len__()))
    if (valid_link.__len__() <= 10):
        print("xxxx{}城市无法获取网页链接！！！！xxxx".format(city))
    # print("-----------------分割线---------------------")

    file = open('网页地址/{}_网页地址_{}.txt'.format(city, valid_link.__len__()), 'w')
    for l in valid_link:
        file.write(str(l))
        file.write('\n')
    file.close()
    return valid_link, count

def get_link_3(city, url, key_word, num_page, page_option, link_type="href"):
    valid_link = list()
    driver = chrome_init()
    count = 0
    for c in key_word:
        print("=====当前处理城市：{}；当前关键词：{}=====".format(city, c))

        for p in range(1, num_page+1):
            try:
                len_pre = valid_link.__len__()
                if page_option == 0:
                    cur_url = url.format(p, c)
                elif page_option == 1:
                    cur_url = url.format(c, p)
                elif page_option == 2:
                    cur_url = url.format(p, c, c)
                elif page_option == 3:
                    cur_url = url.format(c, p, c)
                elif page_option == 4:
                    cur_url = url.format(c, c, p)
                else:
                    print("请输入页面跳转类型")
                    break
                driver.get(cur_url)
                time.sleep(2)
                eleByClass = driver.find_elements(By.TAG_NAME, 'a')
                for i in eleByClass:
                    href = i.get_attribute(link_type)
                    href = str(href)
                    if re.search(re_sen, href):
                        if href not in valid_link:
                            valid_link.append(href)
                            # print(href)
                    # 关闭浏览器实例
                len_after = valid_link.__len__()
                if len_after > len_pre:
                    continue
                else:
                    # driver.quit()
                    break
            except:
                print("第{}页页面不存在，无法打开".format(p))
        count = count + p
        # if p >= (num_page):
    driver.quit()
    print("====={}城市共打开{}页网页，获取链接{}个=====".format(city, count, valid_link.__len__()))
    if(valid_link.__len__() <= 10):
        print("!!!!!!!!!!{}城市无法获取网页链接！！！！!!!!!".format(city))
    # print("-----------------分割线---------------------")

    file = open('网页地址/{}_网页地址_{}.txt'.format(city, valid_link.__len__()), 'w')
    for l in valid_link:
        file.write(str(l))
        file.write('\n')
    file.close()
    return valid_link, count

def get_link_4(city, input_url, key_word, button_1, button_2, num_page, tar_res, c_title, link_type="href"): #用来处理链接中不包含搜索关键字的情况
    valid_link = list()
    driver = chrome_init()
    count = 0
    for c in key_word:
        driver.get(input_url)
        time.sleep(2)
        driver.find_element(By.XPATH, value=button_1).clear()
        # next_button.click()
        driver.find_element(By.XPATH, value=button_1).send_keys(c)
        driver.find_element(By.XPATH, value=button_2).click()
        time.sleep(3)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        eleByClass = driver.find_elements(By.TAG_NAME, 'a')
        for i in eleByClass:
            href = i.get_attribute(link_type)
            href = str(href)
            if re.search(re_sen, href):
                if href not in valid_link:
                    valid_link.append(href)
                    # print(href)

        if tar_res[c_title[4]] == 1:
            for ii in range(num_page - 1):
                try:
                    # 查找下一页按钮并点击它
                    next_button = driver.find_element(By.XPATH, value=tar_res[c_title[5]])
                    next_button.click()
                    time.sleep(2)
                    windows = driver.window_handles
                    driver.switch_to.window(windows[-1])
                    eleByClass = driver.find_elements(By.TAG_NAME, 'a')
                    for i in eleByClass:
                        href = i.get_attribute(link_type)
                        href = str(href)
                        if re.search(re_sen, href):
                            if href not in valid_link:
                                valid_link.append(href)
                                # print(href)
                except:
                    # 关闭浏览器实例
                    # driver.quit()
                    break
            count = count + ii + 2
        elif tar_res[c_title[6]] == 1:
            for ii in range(2, num_page + 1):
                try:
                    # 查找下一页按钮并点击它
                    driver.find_element(By.XPATH, value=tar_res[c_title[7]]).clear()
                    # next_button.click()
                    driver.find_element(By.XPATH, value=tar_res[c_title[7]]).send_keys(ii)
                    driver.find_element(By.XPATH, value=tar_res[c_title[8]]).click()
                    time.sleep(2)
                    eleByClass = driver.find_elements(By.TAG_NAME, 'a')
                    for i in eleByClass:
                        href = i.get_attribute(link_type)
                        href = str(href)
                        if re.search(re_sen, href):
                            if href not in valid_link:
                                valid_link.append(href)
                                # print(href)
                except:
                    # 关闭浏览器实例
                    # driver.quit()
                    break
            count = count + ii
        elif tar_res[c_title[9]] == 1:
            for ii in range(num_page - 1):
                try:
                    # 查找下一页按钮并点击它
                    next_button = driver.find_element(By.XPATH, value=tar_res[c_title[10]])
                    next_button.click()
                    time.sleep(2)
                    eleByClass = driver.find_elements(By.TAG_NAME, 'a')
                    for i in eleByClass:
                        href = i.get_attribute(link_type)
                        href = str(href)
                        if re.search(re_sen, href):
                            if href not in valid_link:
                                valid_link.append(href)
                                # print(href)
                except:
                    # 关闭浏览器实例
                    # driver.quit()
                    break
            count = count + ii + 2
        else:
            print('{}城市网站没有上述跳转方法'.format(tar_res[c_title[0]]))
            continue

    driver.quit()
    print("====={}城市共打开{}页网页，获取链接{}个=====".format(city, count, valid_link.__len__()))
    if (valid_link.__len__() <= 10):
        print("!!!!!!!!!!{}城市无法获取网页链接！！！！!!!!!".format(city))
    # print("-----------------分割线---------------------")

    file = open('网页地址/{}_网页地址_{}.txt'.format(city, valid_link.__len__()), 'w')
    for l in valid_link:
        file.write(str(l))
        file.write('\n')
    file.close()
    return valid_link, count

def city_judge(key_word, num_page, city_id):
    data_frame = pd.read_excel('城市链接判断_v1.xlsx', sheet_name='Sheet1')
    c_title = ['城市', '页码相关', '第一页', '页码跳转类型: 0-[p,c], 1-[c,p], 2-[p,c,c], 3-[c,p,c], 4-[c,c,p] ', '下一页', '下一页按钮', '输入框', '输入框内容按钮', '输入框跳转按钮',
           '查看更多', '查看更多按钮', '手动搜索', '手动搜索输入', '手动搜索跳转', '链接不同', '链接类型']

    i = city_id
    tar_res = data_frame.loc[i]
    print("-----------------分割线---------------------")
    print("当前城市ID：{}，处理{}".format(i, tar_res[c_title[0]]))
    if tar_res[c_title[14]] == 1:
          if tar_res[c_title[11]] == 1:
                 try:
                        get_link_4(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[12]], tar_res[c_title[13]], num_page, tar_res, c_title, tar_res[c_title[15]])
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[1]] == 1:
                 try:
                        get_link_3(tar_res[c_title[0]], tar_res[c_title[2]], key_word, num_page, tar_res[c_title[3]], tar_res[c_title[15]])
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[4]] == 1:
                 try:
                        get_link_1(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[5]], num_page, tar_res[c_title[15]])
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[6]] == 1:
                 try:
                        get_link_2(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[7]], tar_res[c_title[8]], num_page, tar_res[c_title[15]])
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[9]] == 1:
                 try:
                        get_link_1(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[10]], num_page, tar_res[c_title[15]])
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          else:
                 print('{}城市网站没有上述跳转方法'.format(tar_res[c_title[0]]))

    else:
          if tar_res[c_title[11]] == 1:
                 try:
                        get_link_4(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[12]], tar_res[c_title[13]], num_page, tar_res, c_title)
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[1]] == 1:
                 try:
                        get_link_3(tar_res[c_title[0]], tar_res[c_title[2]], key_word, num_page, tar_res[c_title[3]])
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[4]] == 1:
                 try:
                        get_link_1(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[5]], num_page)
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[6]] == 1:
                 try:
                        get_link_2(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[7]], tar_res[c_title[8]], num_page)
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          elif tar_res[c_title[9]] == 1:
                 try:
                        get_link_1(tar_res[c_title[0]], tar_res[c_title[2]], key_word, tar_res[c_title[10]], num_page)
                 except:
                        print("{}城市无法打开网页，excel格式有错误".format(tar_res[c_title[0]]))
          else:
                 print('{}城市网站没有上述跳转方法'.format(tar_res[c_title[0]]))


def is_valid(temp_str, key_word, key_word_2):
    k_valid = 0
    for i in key_word:
        if i in temp_str:
            k_valid = k_valid + 1
            break
        else:
            continue
    for i in key_word_2:
        if i in temp_str:
            k_valid = k_valid + 1
            break
        else:
            continue
    if k_valid == 2:
        return 1
    else:
        return 0

def judge_valid(city, time_wait, key_word, key_word_2, wkh_path):
    confg = pdfkit.configuration(wkhtmltopdf=wkh_path)
    pdfkit_options = {'encoding': 'UTF-8'}
    b_count = 0

    f_path = os.getcwd() + os.path.sep + '网页地址'
    f_name = '{}*_网页地址_*.txt'.format(city)
    f_name = glob.glob(f_path + os.path.sep + f_name)
    file = open(f_name[0], 'r')
    list_read = set()
    for line in file:
        line = line.strip('\n')
        if line not in list_read:
            list_read.add(line)
    driver = chrome_init()
    print('当前处理城市：{}，正在从{}个网页中寻找有效网页，请等待···'.format(city, list_read.__len__()))
    if len(list_read) < 1:
        print("This is null link txt.")
    else:
        for url in list_read:
            # url = num_link[0:-1]
            # print(url)
            try:
                driver.get(url)
                driver.set_page_load_timeout(time_wait)
                driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + "a")
                driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + "c")
                texts = pyperclip.paste()
                # print(texts)
                c_valid = 0
                c_valid = is_valid(texts, key_word, key_word_2)
                if c_valid == 1:
                    b_count = b_count + 1
                    # print('{}-有效网页-{}'.format(city, b_count))
                    texts = texts + url
                    # print(texts)
                    texts = str(texts)
                    texts = texts.replace('\\u3000','')
                    targetPath = os.getcwd() + os.path.sep + '网页内容' + os.path.sep + '{}'.format(city)
                    if not os.path.exists(targetPath):
                        os.makedirs(targetPath)
                    filename = '{}-{}.pdf'.format(city, b_count)
                    pdfkit.from_string(texts, targetPath + os.path.sep + filename, configuration=confg,
                                    options = pdfkit_options)
                else:
                    continue
            except:
                # print(url)
                continue
    driver.quit()

def pdf_get_line(curFile, indexMap, indexList, cityName, retIndex):
    retStrList = []
    with pdfplumber.open(curFile) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            txt = page.extract_text()
            #deal txt
            txtList = txt.strip().split("。")
            for line1 in txtList:
                    #print(line1)
                line1 = line1.replace('\n', '')
                line1 = line1.replace('\t', ' ')
                if(re.match("表 [0-9].*", line1)):
                    continue
                for index in indexList:
                    #print("===",index)
                    if re.match(index, line1):
                        #城市名、内部指标名、文档名、文档查找到的关键词、文档查找到的关键词对应的句子
                        #print(line1)
                        retStrList.append("城市:\t"+cityName +"\t内部指标名："+indexMap[index]+"\t文档名："+curFile +"\t关键词："+index+"\t句子："+ line1.replace('\n', ''))
                        retIndex[cityName][indexMap[index]] = 1
                        #break

            # deal table
            if (tables != None):
                for table in tables:
                    head = ",".join(map(str, table[0])).replace('\n', '').split("。")[0]
                    for row in table:
                        if (row == None):
                            continue
                        #有些表格是误识别
                        strlineList = ",".join(map(str, row)).replace('\n', '').split("。")
                        for strline in strlineList:
                            for index in indexList:
                                if (re.match(index, strline) != None):
                                    #print("here")
                                    #print(index + "====" + strline + "=======")
                                    retStrList.append("城市:\t" + cityName + "\t内部指标名：" + indexMap[
                                        index] + "\t文档名：" + curFile + "\t关键词：" + index + "\t表格：" + "[" + head + "][" + strline + "]")

                                    retIndex[cityName][indexMap[index]] = 1
                            #break

            #print(txt)
            #return 0
    return retStrList


#doc 、docx不能兼用，只支持docx
def docx_get_line(curFile, indexMap, indexList, cityName, retIndex):
    document = Document(curFile)
    retStrList = []

    for paragraph in document.paragraphs:
        txt=paragraph.text
        # deal txt
        txtList = txt.strip().split("。")
        for line1 in txtList:
            # print(line1)
            line1 = line1.replace('\n', '')
            line1 = line1.replace('\t', ' ')
            for index in indexList:
                if re.match(index, line1):
                    # 城市名、内部指标名、文档名、文档查找到的关键词、文档查找到的关键词对应的句子
                    # print(line1)
                    retStrList.append("城市:\t" + cityName + "\t内部指标名：" + indexMap[
                        index] + "\t文档名：" + curFile + "\t关键词：" + index + "\t句子：" + line1.replace('\n', ''))
                    retIndex[cityName][indexMap[index]] = 1

    return retStrList

def read_city_list(cityTxt):
    cityList = {}
    with open(cityTxt, "r", encoding='UTF-8') as infile:
        for line in infile:
            strList = line.strip("\n").split(" ")
            if(len(strList)) < 2:
                continue
            cityList[strList[0]] = strList[1]
    return cityList

def judge_city_name(item, cityList):
    for city in cityList.keys():
        if(re.match(cityList[city],item)):
            return city
    return "NULL"

def get_index_map(indexTxt):
    indexMap = {}
    calScoreMap = {}
    with open(indexTxt, "r", encoding='UTF-8') as infile:
        for line in infile:
            lineList = line.strip("\n").split(" ")
            #print(lineList)
            if(len(lineList) < 4):
                continue
            name = lineList[0] + "," + lineList[1]
            indexMap[lineList[2]] = lineList[0] + "," + lineList[1]
            calScoreMap[name] = int(lineList[3])
    return indexMap, list(indexMap.keys()), calScoreMap

def deal_score(retIndex,calScoreMap):
    scoreMap = {}
    scoreIndexNames = {}
    for city in retIndex.keys():
        scoreMap[city] = {}
        scoreIndexNames[city] = {}
        for v in retIndex[city]:
            indexName = v.split(",")
            if(indexName[0] in scoreMap[city].keys()):
                scoreMap[city][indexName[0]] += calScoreMap[v]
                scoreIndexNames[city][indexName[0]] = scoreIndexNames[city][indexName[0]] + "," + indexName[1]
            else:
                scoreMap[city][indexName[0]] = calScoreMap[v]
                scoreIndexNames[city][indexName[0]] = indexName[1]
    return scoreMap, scoreIndexNames

def city_rank(city, rule_name, city_exp):
    root = os.getcwd() + os.path.sep + '网页内容' + os.path.sep + '{}'.format(city)
    indexTxt = os.getcwd() + os.path.sep + '城市打分' + os.path.sep + rule_name
    # cityTxt = os.getcwd() + os.path.sep + '城市打分' + os.path.sep + city_exp

    #获取城市列表
    # cityList = read_city_list(cityTxt)
    cityList = {}
    cityList[city] = city_exp
    print(cityList)
    print('正在打分，请稍候···')
    #获取指标
    indexMap,indexList,calScoreMap = get_index_map(indexTxt)
    #print(indexMap,indexList)
    input_files = os.listdir(root)
    retIndex = {}
    #初始化
    for city in cityList.keys():
        retIndex[city]={}

    times = str(time.time()).split(".")[0]

    for item in input_files:
        #print("input files" + item)
        if (item.startswith(".") or item.startswith("~") ):
            continue

        curFile = os.path.join(root, item)
        #print(curFile)
        cityName = judge_city_name(item, cityList)
        #print("cityName" + cityName)
        if (cityName == "NULL"):
            print("%s:city name not in the fileName, ignore" %curFile)
            continue

        if (item.endswith("PDF") or item.endswith("pdf")):
            retStrList = pdf_get_line(curFile, indexMap, indexList, cityName, retIndex)
        elif (item.endswith("docx") ):
            retStrList = docx_get_line(curFile, indexMap, indexList, cityName, retIndex)
        else:
            print("%s:only pdf or docx, ignore" %curFile)
            continue
        f_path = '城市打分' + os.path.sep + '{}'.format(city)
        if not os.path.exists(f_path):
            os.makedirs(f_path)
        fwrite = open(f_path + os.path.sep + "findInfo" + cityName + times + ".txt", "a+", encoding='UTF-8')
        for line in retStrList:
            fwrite.write(line)
            fwrite.write("\n\n")
        fwrite.close()

    scoreMap, scoreIndexNames = deal_score(retIndex, calScoreMap)
    for city in scoreMap.keys():
        f_path = '城市打分' + os.path.sep + '{}'.format(city)
        if not os.path.exists(f_path):
            os.makedirs(f_path)
        fwrite1 = open(f_path + os.path.sep + "indexList" + city + times + ".txt", "a+", encoding='UTF-8')
        for key in scoreMap[city]:
            strRes = "指标：%s, 得分: %s, 得分点: %s" %(key, str(scoreMap[city][key]), scoreIndexNames[city][key])
            print(strRes)
            fwrite1.write(strRes)
            fwrite1.write("\n")
        fwrite1.close()