# coding=utf-8

import requests
from bs4 import BeautifulSoup
import time
import sys
import re
from itertools import islice
import random

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


def parse(category, url):
    parse_url = "http://www.anzhi.com" + url
    r = sessions.get(parse_url)
    r.encoding = 'utf-8'
    result = []
    soup = BeautifulSoup(r.text, "html5lib")
    content = soup.find(attrs={'class': 'content'}) \
        .find(attrs={'class': 'content_left'}) \
        .find(attrs={'class': 'app_list border_three'}) \
        .find_all('li')
    for c in content:
        temp = c.find(attrs={'class': 'app_info'})
        app_name = temp.find(attrs={'class': 'app_name'}).find('a')["title"]
        app_downloand_num = temp.find(attrs={'class': 'app_top'}).find(attrs={'class': 'app_downnum l'}).text.replace(
            "下载：", "")
        app_version = temp.find(attrs={'class': 'app_top'}).find(attrs={'class': 'app_version l'}).text.replace("版本：",
                                                                                                                "")
        result.append([category, app_name, app_downloand_num, app_version])

    if len(result)==0:
        raise Exception("content not found")
    return result


def next_page(url):
    groups = re.match(r"(^/sort_\d+_)(\d+)(_hot.html$)", url)
    left = groups.group(1)
    page = groups.group(2)
    right = groups.group(3)
    next = int(page) + 1
    return left + str(next) + right


def write_csv(parse_results):
    file_name = "安智手机市场" + ".csv"
    with open(file_name, 'a') as fp:
        for row in parse_results:
            content = '%s,%s,%s,%s \r\n' % (row[0], row[1], row[2], row[3])
            fp.write(content)


def parse_one_category(category, url):
    parse_url = url
    failed_times = 0
    while failed_times < 3:
        try:
            temp = parse(category, parse_url)
            write_csv(temp)
            parse_url = next_page(parse_url)
        except Exception as e:
            failed_times += 1
            print "url" + "解析失败"

        sleep_time = random.uniform(0.5,4)
        time.sleep(sleep_time)


if __name__ == '__main__':
    with open("/Users/hebao/PycharmProjects/data-mining/datasets/app_games.csv") as fp:
        lines = fp.readlines()
        for line in islice(lines, 1, None):
            category = line.strip('\r\n').split(",")
            parse_one_category(category[1], category[0])
