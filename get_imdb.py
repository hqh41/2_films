# coding=utf-8

from __future__ import unicode_literals, print_function

import requests
from time import sleep
from lxml.etree import HTML, tostring


def get_top250link():
    top250resp = requests.get("http://www.imdb.com/chart/top?ref_=nv_mv_250_6")
    html = HTML(top250resp.text)
    xpaths = '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr/td[2]/a'
    links = html.xpath(xpaths)
    results = [{'name': x.text, 'link': x.get('href'), 'ranking': y} for x, y in zip(links, range(1, 251))]
    return results


def get_movie_performers(url):
    resp = requests.get(url)
    html = HTML(resp.text)
    xpaths = '//tr/td/a/span'
    result = [x.text for x in html.xpath(xpaths)]
    return result


def main():
    top250mv = get_top250link()
    for item in top250mv:
        url = "http://www.imdb.com{}".format(item['link'])
        performers = get_movie_performers(url)
        item.update(performers=performers)
        # sleep(2)
        break

    print(top250mv[0].keys())


if __name__ == '__main__':
    main()
