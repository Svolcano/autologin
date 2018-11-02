import requests

http_header = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/63.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept-Language": "zh-CN,en-US;q=0.8",
}


def login(user, passwd):
    url = ''
    paras = {

    }
    resp = requests.post(url, paras)