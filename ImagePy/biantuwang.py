import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def dl_page(url):
    res = requests.get(url, headers=headers, proxies=proxies)
    res.encoding = "gbk"
    main_page = BeautifulSoup(res.text, "html.parser")
    main_url = main_page.find("ul", attrs={"class": "clearfix"})
    alist = main_url.find_all("a")
    url_ = "https://pic.netbian.com"
    for a in alist:
        href = a.get("href")
        url_real = url_ + href
        resp = requests.get(url_real, headers=headers, proxies=proxies)
        resp.encoding = "gbk"
        child_page = BeautifulSoup(resp.text, "html.parser")
        img_page = child_page.find("a", attrs={"id": "img"})
        img = img_page.find("img")
        src = img.get("src")
        src_real = url_ + src
        img_res = requests.get(src_real)

        img_name = src.split("/")[-1]  # 拿到最后一个杠后面的内容
        with open("img/" + img_name, mode="wb") as f:
            f.write(img_res.content)  # 括号内内容为字节，不能打印
        print("over", img_name)
        time.sleep(10)
    print("提取完毕")


#
if __name__ == '__main__':

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44",
        "referer": "https://pic.netbian.com/4kmeinv/index.html",
        "cookie": "__yjs_duid=1_c427763b6a77b795723fe580805d86f41635746735356; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1635749214,1636550738,1636550843; zkhanecookieclassrecord=%2C54%2C; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1635746736,1636550853,1636557267,1636606416; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1636606416; yjs_js_security_passport=d0fe81024fb5a59de630df3fb7dd52134fe3a84c_1636606550_js"

    }
    proxies = {
        "http": "http://113.125.156.47:8888"
    }
    url = "https://pic.netbian.com/4kmeinv/index.html"
    dl_page(url)
    #     # for i in range(2,148):#此效率会极其低下
    #     #     dl_page(f"https://pic.netbian.com/4kmeinv/index_{i}.html")
    with ThreadPoolExecutor(10) as t:
        for i in range(2, 30):
            t.submit(dl_page, f"https://pic.netbian.com/4kmeinv/index_{i}.html")

    print("全部下载完毕！！！")