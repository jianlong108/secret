#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:wangjianlong
@file: AoMenKaiPanZao.py 
@time: 2023/11/27
@contact: jlwang108@gmail.com
@site:  
@software: PyCharm 
"""
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import datetime
from GetData.SOCCER_MODELS import FootballGame
from BEAUTIFUL_SOUP_HELPER import *
import urllib.request

def get_today_soccer_games():
	# 获取当前日期和时间
	current_datetime = datetime.now()

	# 提取年、月、日信息
	year = current_datetime.year
	month = current_datetime.month
	day = current_datetime.day

	# 打印结果
	today = f"{year}-{month}-{day}"
	print(today)
	# url = 'https://live.titan007.com/index2in1.aspx?id=1'
	url = 'https://vip.titan007.com/AsianOdds_n.aspx?id=2523045'
	try:
		# 使用 Chrome 浏览器
		driver = webdriver.Chrome()

		# 打开网页
		driver.get(url)
		# 等待 id 为 odds 的元素加载完成
		# odds_element = WebDriverWait(driver, 20).until (
		# 	EC.presence_of_element_located((By.ID, "oddsDetail"))
		# )
		# 打印或处理元素中的数据
		# print(odds_element.text)
		# 等待页面加载（你可能需要根据实际情况调整等待时间）
		driver.implicitly_wait(20)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# setting_ele = driver.find_element(By.CLASS_NAME, 'setting')
		# setting_ele.click()
		table_element = driver.find_element(By.ID, 'oddsDetail')
		print(table_element.text)
		# driver.implicitly_wait(5)
		# 找到 id 为 "table_live" 的表格元素
		# table_element = driver.find_element(By.ID, 'table_live')
		# 如果找到了表格元素，继续查找 tbody 中的所有带有 index 属性的 tr 元素
		# if table_element:
		# 	tbody_element = driver.find_element(By.TAG_NAME, 'tbody')
		# 	if tbody_element:
		# 		tr_elements = tbody_element.find_elements(By.XPATH, '//tr[@index]')
		#
		# 		# 输出找到的 tr 元素的文本内容
		# 		for tr_ele in tr_elements:
		# 			gameid_ori = tr_ele.get_attribute('id')
		# 			print(gameid_ori)
		# 			match1 = re.search(r'_(\d+)', gameid_ori)
		# 			if match1:
		# 				gameid = match1.group(1)
		# 			print(f"gameid:{gameid}")
		#
		# 			leagueEle = tr_ele.find_elements(By.TAG_NAME, 'td')[1].find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'a')
		# 			# leagueEle = tr_ele.find_element(By.XPATH, "//td/span/a[@title='进入资料库']")
		# 			leagueUrl = leagueEle.get_attribute('href')
		#
		# 			leagueName = leagueEle.text
		# 			# 使用正则表达式提取 SclassID 的值
		# 			match2 = re.search(r'SclassID=(\d+)', leagueUrl)
		# 			if match2:
		# 				league_id = match2.group(1)
		# 			print(f"leagueUrl:{leagueUrl},league_id: {league_id}, leagueName:{leagueName}")
		#
		# 			begintimeEle = tr_ele.find_element(By.ID, f"mt_{gameid}")
		# 			beginTime_str = f"{today} {begintimeEle.text}:00"
		# 			print(f"开赛时间:{beginTime_str}")
		#
		# 			horder_ele = tr_ele.find_element(By.ID, f"horder_{gameid}")
		# 			match3 = re.search(r'\[([^\]]+)\]', horder_ele.text)
		# 			if match3:
		# 				horder_str = match3.group(1)
		# 			print(f"主队排名:{horder_str}")
		#
		# 			home_ele = tr_ele.find_element(By.ID, f"team1_{gameid}")
		# 			horder_str = home_ele.text
		# 			print(f"主队:{horder_str}")
		#
		# 			gorder_ele = tr_ele.find_element(By.ID, f"gorder_{gameid}")
		# 			match4 = re.search(r'\[([^\]]+)\]', gorder_ele.text)
		# 			if match4:
		# 				horder_str = match4.group(1)
		# 			print(f"客队排名:{horder_str}")
		#
		# 			away_ele = tr_ele.find_element(By.ID, f"team2_{gameid}")
		# 			away_str = away_ele.text
		# 			print(f"客队:{away_str}")
		#
		# 			scoreEle = tr_ele.find_element(By.XPATH, f"//td[@aloc={gameid}]")
		# 			print(f"比分:{scoreEle.text}")
		#
		# # 关闭浏览器
		# driver.quit()
	except Exception as e:
		print(e)
	finally:
		# 关闭浏览器
		driver.quit()


def loadlockhtml():
	try:
		# 本地HTML文件的路径
		local_file_path = '/Users/jl/Desktop/a.html'

		# 使用 file 协议加载本地文件
		url = 'file://' + local_file_path

		# 打开并读取文件内容
		with urllib.request.urlopen(url) as f:
			html_content = f.read().decode('utf-8')

		soup = BeautifulSoup(html_content, 'html.parser')

		# 找到 id 为 'odddetails' 的元素
		odddetails_element = soup.find(id='oddsDetail')

		# 输出元素的内容
		if odddetails_element:
			# print(odddetails_element)
			# 找到所有行标签 <tr>
			rows = odddetails_element.find_all('tr')
			companynames = []
			# 遍历每一行，并输出其内容
			for row in rows:
				# 检查是否为 class="thead2" 的 <tr> 标签
				if 'thead2' in row.get('class', []):
					# 找到该行中的所有标题标签 <th>
					headers = row.find_all('th')

					# 输出每个 <th> 的文本内容
					for header in headers:
						name = header.text.strip()
						if name != '比分' and name != '变化时间':
							print("公司名："+name)  # 输出每个 <th> 的文本内容（去除两端的空白）
							companynames.append(name)
						else:
							print(name)

				else:
					# 找到该行中的所有列标签 <td>
					columns = row.find_all('td', style='background: #dcfbff')

					# 输出每个符合条件的 <td> 元素的文本内容和其在 <tr> 中的索引位置
					for idx, td in enumerate(row.find_all('td')):
						if td in columns:
							print(f'Text: {td.text.strip()}, Index in <tr>: {idx} {companynames[idx]}')
		else:
			print("未找到 id 为 'odddetails' 的元素。")
	except Exception as e:
		print(e)
	finally:
		print('----')



if __name__ == '__main__':
	# print('澳门初盘大于其他一个盘')
	# get_today_soccer_games()
	loadlockhtml()