import pandas as pd
from utils import city_judge
from utils import judge_valid
from utils import city_rank
import pinyin
data_frame = pd.read_excel('城市链接判断_v1.xlsx', sheet_name='Sheet1')
c_title = ['城市', '页码相关', '第一页', '页码跳转类型: 0-[p,c], 1-[c,p], 2-[p,c,c], 3-[c,p,c], 4-[c,c,p] ', '下一页', '下一页按钮', '输入框', '输入框内容按钮', '输入框跳转按钮',
       '查看更多', '查看更多按钮', '手动搜索', '手动搜索输入', '手动搜索跳转', '链接不同', '链接类型']

key_word = ['低碳']
key_word_2 = ['工作']
num_page = 20 # 浏览多少页来获取网页链接
city_id = range(27, 28)
wait_time = 10 # 判断网页有效时等待多少秒
rule_name = 'En_index.txt'
wkh_path = 'wkhtmltopdf/bin/wkhtmltopdf.exe'

for i in city_id:
       tar_res = data_frame.loc[i]
       city_name = tar_res[c_title[0]]

       # 获取网址链接
       try:
              city_judge(key_word, num_page, i)
       except:
              print('错误：{}城市无法获取网页链接！！！'.format(city_name))
              continue

       # 判断网页内容是否符合
       try:
              judge_valid(city_name, wait_time, key_word, key_word_2, wkh_path)
       except:
              print('错误：{}城市无法判断网页内容是否符合！！！'.format(city_name))
              continue

       # 进行打分
       # texts = str(city_name)
       # texts = texts.replace('市', '')
       # texts_2 = pinyin.get_initial(texts, delimiter="").upper()
       # city_exp = '.*{}.*|{}-.*'.format(texts, texts_2)
       # try:
       #        city_rank(city_name, rule_name, city_exp)
       # except:
       #        print('错误：{}城市无法进行打分！！！'.format(city_name))
       #        continue
