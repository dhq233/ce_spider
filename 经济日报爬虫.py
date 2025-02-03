# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:46:31 2025

@author: DuOH
"""

import requests
from bs4 import BeautifulSoup
import time

time=time.localtime()
date=time[2]
year_month=str(time[0])+f'{time[1]:02d}'

# 设置搜索的 URL 和表单数据
url_base = f'http://paper.ce.cn/pc/layout/{year_month}/{date}/node_01.html'
#想跨月就手动修改一下日期的月份，下面文件名别忘了改

#以当天为基准往前爬
#date=21#这里写你的基准日期（就是几号）
day=input("想爬几天的？(从今天开始）")
if not day.isdigit():
    print("输入需要是正整数")
else:
    day=int(day)
for j in range(0,day):
    
    new_date=date-j
   
    url_day=url_base.replace(f'/{date:02d}/',f'/{new_date:02d}/')

    txt=''
    for i in range(1, 12):  # 从 1 到 11，视觉版面不要
        # 使用字符串格式化方法替换 URL 中的 node_01 部分
        url=url_day.replace('node_01', f'node_{i:02d}')
        
        # 发送 GET 请求
        response = requests.get(url)
        a_herfs=[]
        
        # 检查响应状态
        if response.status_code == 200:
            # 获取页面内容
            page_content = response.text
            
            # 使用 BeautifulSoup 解析页面
            soup = BeautifulSoup(page_content, 'html.parser')
        
           
            titles = soup.find_all('li',class_='clearfix')  
            for li in titles:
               # 查找每个 <li> 标签中的 <a> 标签
               a_tag = li.find('a', href=True)  # 查找具有 href 属性的 <a> 标签
               if a_tag:
                   a_herfs.append(a_tag['href'])
                  # print(a_tag['href'])  # 打印链接和链接文本
        else:
              print(f"出错啦:未找到{new_date:02d}日版面{i:02d}")
        # 基础 URL
        base_url = "http://paper.ce.cn/pc/"
        # 使用列表推导式批量处理每个路径
        paths = [base_url + a_herf.lstrip("../../../") for a_herf in a_herfs]
       
        for path in paths:
            
            new_url=path
            # 发送 GET 请求
            response = requests.get(new_url)
            
            # 检查响应状态
            if response.status_code == 200:
                # 显式设置响应的编码为 UTF-8
                response.encoding = 'utf-8'
            
                # 获取页面内容
                page_content = response.text
                # 使用 BeautifulSoup 解析页面
                soup = BeautifulSoup(page_content, 'html.parser')
            
                # 提取你需要的信息（例如：标题、文章内容等）
                p=soup.find_all('p')
                txt+='{'
                for content in p:
                    if content.find_parent('div', class_='newsNav') is None:
                        
                        txt+=(content.text)
                txt+='}'
            else:
                   print("出错啦:未找到正文 ")          
    
    file_path=f'{year_month}.{new_date}.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
               f.write(txt)
    print(f"已爬取{year_month}{new_date:02d}日")