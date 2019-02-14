import requests
import re
from requests import RequestException
import json


def get_one_page(url):
    """
    页面源码
    :param url: 网址
    :return: 页面源码
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """
    解析页面
    :param html: 页面源码
    :return: 解析好的对象
    """
    pattern = re.compile('<li>.*?em class="">(.*?)</em>.*?src="(.*?)".*?class="title">(.*?)</span>.*?<p class="">\n(.*?)<br>\n(.*?)</p>'
                         +'.*?"v:average">(.*?)</span>.*?<span>(.*?)</span>.*?<span class="inq">(.*?)</span>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '电影': item[2],
            '导演及主演': (',').join(item[3].strip().split('&nbsp;')),
            '时间': ('').join(item[4].strip().split('&nbsp;')),
            '评分': item[5],
            '评论人数': item[6].strip(),
            '主题': item[7],
            '封面': item[1]
        }

def write_to_file(content):
    """
    写入文件夹
    :param content:
    :return:
    """
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(start):
    """
    主函数
    :param start:
    :return:
    """
    url = 'https://movie.douban.com/top250?start='+str(start)+'&filter='
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(start = i * 25)