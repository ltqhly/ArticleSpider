# -*- coding: utf-8 -*-
import hashlib


def get_md5(url):

    if isinstance(url, str):
        url = url.encode("utf-8")

    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


# print(get_md5("http://jobBole.com".encode("utf-8")))

if __name__ == '__main__':
    print(get_md5("http://jobBole.com"))
