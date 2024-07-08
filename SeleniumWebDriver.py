#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: SeleniumWebDriver.py 
@time: 2024/06/28
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置ChromeDriver的路径
driver_path = '/path/to/chromedriver'

# 设置Chrome选项
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速

# 创建Chrome浏览器实例
driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

# 打开目标网页
driver.get("https://live.nowscore.com/odds/match.aspx?id=2545210")

try:
    # 等待id为odds的元素加载完成
    odds_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "odds"))
    )
    # 打印或处理元素中的数据
    print(odds_element.text)
finally:
    # 关闭浏览器
    driver.quit()
