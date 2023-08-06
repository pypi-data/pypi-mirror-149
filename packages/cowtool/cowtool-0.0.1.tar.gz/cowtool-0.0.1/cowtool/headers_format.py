#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/27 14:52
# @Author  : lj
# @File    : headers_format.py

from typing import List


class HeaderFormat():

    def __init__(self) -> None:
        self.__headers_dict = {}



    def init(self, header: str):
        self.headers = header
        self.__format()

    def __format(self):
        one_lists = self.headers.split('\n')
        one_lists = [i.replace(' ', '') for i in one_lists if i][:-1]
        self.__split(one_lists)



    def __split(self, one_list: List[str]):

        for one in one_list:
            key, value = one.split(':',1)
            self.__headers_dict.setdefault(key, value)



    def header_add(self, **kwargs):
        for one_key, one_value in kwargs.items():

            if one_value:
                self.__headers_dict[one_key] = one_value
            else:
                self.__headers_dict.pop(one_key)



    def to_dict(self)->dict:
        return self.__headers_dict


if __name__ == '__main__':
    headers = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: UM_distinctid=17d60239fd61241-0229394b867104-a7d193d-1fa400-17d60239fd7df6
Host: ssr1.scrape.center
Pragma: no-cache
sec-ch-ua: "Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36
    '''
    header = HeaderFormat(headers)
    dd = {
        'Accept': 1,
        'b': 2,
        'Cookie':None
    }

    header.header_add(**dd)
    print(header.to_dict())
