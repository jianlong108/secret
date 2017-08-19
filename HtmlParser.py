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


def gethtmllistwithlabel(html, label, attrs={}):
    soup = BeautifulSoup(html, "html.parser")
    elementlist = []
    targetelement = None
    if attrs != {}:
        targetelement = soup.find_all(label, attrs=attrs)
    else:
        targetelement = soup.find_all(label)
    elementlist.extend(targetelement)
    return elementlist

def getsoup(html ):
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

