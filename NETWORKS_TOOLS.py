#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.request import urlopen, Request


def get_resultstr_with_url(urlStr):
    resultStr = ''
    headers = {'User-Agent': 'Baiduspider'}
    response = requests.get(urlStr,headers=headers)
    if response.ok:
        resultStr = response.content
    return resultStr

def get_htmlcontent_with_url(url, htmldecode = 'utf-8'):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        # 'User-Agent': 'Baiduspider',
    }
    # 创建请求对象
    request = Request(url, headers=headers)
    # request = urllib2.Request(url=url, headers=header)  # 模拟浏览器进行访问
    # response = urllib2.urlopen(request)
    # Make an HTTP request and read the HTML content
    try:
        # 发送 HTTP 请求获取网页内容
        response = urlopen(request)
        html_content = response.read().decode(htmldecode)  # 使用正确的解码方式
        print(html_content)
        return html_content
    except Exception as e:
        print(f"Error: {e}")
        return ""