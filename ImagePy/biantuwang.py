import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def dl_page(imgurl):
    res = requests.get(imgurl, headers=headers, proxies=proxies)
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


if __name__ == '__main__':

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "referer": "https://pic.netbian.com/4kmeinv/index.html",
        "cookie": "zkhanecookieclassrecord=%2C54%2C; __vtins__3GcHHlFooxXoEQzA=%7B%22sid%22%3A%20%220cbcd5a5-682b-550b-a5c1-d582cc2fce52%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201701007933804%2C%20%22ct%22%3A%201701006133804%7D; __51uvsct__3GcHHlFooxXoEQzA=1; __51vcke__3GcHHlFooxXoEQzA=0444cf11-246b-5d92-96d2-fa31d66a7017; __51vuft__3GcHHlFooxXoEQzA=1701006133806"

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