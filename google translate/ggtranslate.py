from urllib.parse import urlencode

__all__ = ['translate_url']

base_url = 'https://translate.google.cn/translate_a/single?'

params = {
    'client': 'webapp',
    'sl': 'auto',
    'tl': 'zh-CN',
    'hl': 'zh-CN',
    'otf': 1,
    'ssel': 5,
    'tsel': 5,
    'xid': 45662847,
    'kc': 4,
    'tk': 0,
    'q': ''
}

dt = '&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t'


##########
#  构造 url
##########
def translate_url(words='', from_language='auto', to_language='zh-CN'):
    '''
    words           需翻译字符
    from_language   需翻译语言
    to_language     目标语言
    zh-CN(中文)、ko(韩语)、ja(日语)、en(英语)，其他语言code，在index src上查看
    return          url
    '''
    params['q'] = words
    params['sl'] = from_language
    params['tl'] = to_language
    params['tk'] = tk(words)
    ps = urlencode(params) + dt
    return base_url + ps


##########
#  js 解密
##########
def yu(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        d = ord(d[0]) - 87 if 'a' <= d else int(d)
        d = a >> d if '+' == b[c + 1] else a << d
        a = a + d & 4294967295 if '+' == b[c] else a ^ d
    return a


def tk(a):
    '''
    计算tk
    '''
    # TKK = 443594.1479499615，在index src
    d = ['443594', '1479499615']
    b = int(d[0])

    e = []
    f = g = 0

    while g < len(a):
        h = ord(a[g])
        if 128 > h:
            e.append(h)
        else:
            if 2048 > h:
                e[f] = h >> 6 | 192
                f += 1
            else:
                if 55296 == (h & 64512) and g + 1 < len(a) and 56320 == (
                        ord(a[g + 1]) & 64512):
                    g += 1
                    h = 65536 + ((h & 1023) << 10) + (ord(a[g + 1]) & 1023)
                    e.append(h >> 18 | 240)
                    e.append(h >> 12 & 63 | 128)
                else:
                    e.append(h >> 12 | 224)
                    e.append(h >> 6 & 63 | 128)
            e.append(h & 63 | 128)
        g += 1

    a = b
    for f in range(0, len(e)):
        a += e[f]
        a = yu(a, '+-a^+6')
    a = yu(a, '+-3^+b+-f')
    a ^= int(d[1]) | 0

    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a = int(a % 1E6)
    return f'{a}.{a^b}'