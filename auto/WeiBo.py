import requests
import random
import string
import time
import re
import base64
import rsa
import binascii



retry_sleep_time = 5

http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept-Language": "zh-CN,en-US;q=0.8",
}


proxy = {

}



def gen_su():
    a = 'MTM1MjE2MzUxMDM'
    print(len(a))
    su_str = ''.join(random.sample(string.ascii_letters + string.digits, len(a))) + '%3D'
    print(su_str)
    return su_str

def gen_timestamp():
    t = time.time()
    return str(int(time.time() * 1000))


def login(user, passwd):
    '''
    :param user:
    :param passwd:
    :return: cookies {}
    '''
    default_cookies = {}
    s = requests.Session()
    s.headers.update(http_header)
    retry = 3
    resp = None
    while retry:
        try:
            t = gen_timestamp()
            su = gen_su()
            k = (u"https://login.sina.com.cn/sso/prelogin.php?entry=weibo&"
                 "callback=sinaSSOController.preloginCallBack&su=%s"
                 "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=%s" % (su, t))
            resp = s.get(k, verify=False)
            if resp.status_code == 200:
                break
        except Exception as e:
            print(e)
        time.sleep(retry_sleep_time)
        retry -= 1
    if not resp or resp.status_code != 200:
        return default_cookies

    key_data = resp.text
    pat = re.compile(
        r'"servertime":(.*?),.*"nonce":"(.*?)","pubkey":"(.*?)"')

    res = pat.findall(key_data)
    if not res:
        return default_cookies
    servertime, nonce, pubkey = res[0]
    name = base64.b64encode(user.encode()).decode()
    key = rsa.PublicKey(int(pubkey, 16), 65537)
    message = ('%s\t%s\n%s' % (servertime, nonce, passwd)).encode()
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd).decode()

    data = {
        "entry": "account", "gateway": "1",
        "from": "", "savestate": "30",
        "useticket": "0", "pagerefer": "", "vsnf": "1",
        "su": name, "service": "sso",
        "servertime": servertime,
        "nonce": nonce, "pwencode": "rsa2",
        "rsakv": "1330428213",
        "sp": passwd, "sr": "1920*1080", "encoding": "UTF-8",
        "cdult": "3", "domain": "sina.com.cn",
        "prelt": "24", "returntype": "TEXT",
    }
    post_resp = s.post(
        'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)',
        data=data, verify=False)
    if post_resp.status_code != 200:
        return default_cookies
    post_resp_json = post_resp.json()
    if post_resp_json['retcode'] == '0':
        c1 = post_resp.cookies.get_dict()
        print(1, c1)
    home_url = 'http://my.sina.com.cn/'
    host_resp = s.get(home_url, verify=False)
    if host_resp.status_code == 200:
        c2 = s.cookies.get_dict()
        print(2, c2)
    print(c1 == c2)
    return c2

user = '13521635103'
passwd = 'JINGmeiti0424'
login(user, passwd)