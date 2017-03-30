#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
# from urllib2 import Request
import requests





def download(url):
    # print("downloading", url)
    try:
        html = requests.urlopen(url).read()
    except requests.URLError as e:
        print("download error")
        html = None
    return html


def getHtmlListWithLabel(html, label,attrs={}):

    soup = BeautifulSoup(html, "html.parser")

    trList = []
    if attrs != {}:
        tr_ni = soup.find_all(label,attrs=attrs)
    else:
        tr_ni = soup.find_all(label)

    trList.extend(tr_ni)
    return trList

def getSoup(html):

    soup = BeautifulSoup(html, "html.parser")

    return soup

def filterList(list, label):
    tempList = []
    tempList.extend(list)
    for ele in list:
        value = str(ele).find(label)
        if value < 0:
            tempList.remove(ele)

    return tempList

