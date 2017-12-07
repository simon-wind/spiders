# coding=utf-8

import requests
from bs4 import BeautifulSoup
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

header = {
    'Host': 'www.anzhi.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2700.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
}
sessions = requests.session()


def lable_urls():
    urls = []
    base = "http://www.anzhi.com/widgetcat_1.html"
    r = sessions.get(base)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html5lib")
    content = soup.find_all(attrs={'class': 'itemlist'})


    for c in content:
        herfs = c.find_all('a', href=True)

        for herf in herfs:
            urls.append([herf['href'], herf.text.strip()])

    return urls


def save_to_csv(urls):
    with open("/Users/hebao/PycharmProjects/data-mining/datasets/app_urls.csv", 'w') as fp:
        headers = 'url,label\r\n'.encode('utf-8')
        fp.write(headers)
        for url in urls:
            temp = '%s,%s\r\n' % (url[0], url[1])
            print temp.decode("UTF-8").encode('GBK')
            fp.write(temp)


if __name__ == '__main__':
    result = lable_urls()
    save_to_csv(result)
