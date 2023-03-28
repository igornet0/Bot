import bs4
import requests
import html

headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def get_lst_prepod() -> list:
    URL = 'https://guap.ru/rasp/'
    req = requests.get(URL, headers)
    soup = bs4.BeautifulSoup(html.unescape(req.text), "html.parser")
    soup = soup.find("select", {"name": "ctl00$cphMain$ctl06"})
    lst = []
    for i in soup:
        if isinstance(i, bs4.element.Tag):
            d = i.text.split()
            lst.append([d[0], d[1], ''.join(d[3:]), i['value']])
            #print([d[0], d[1], ''.join(d[3:]), i['value']])
    return lst

def get_resp_prepod(value: int) -> dict:
    URL = 'https://guap.ru/rasp/'
    URL = URL + f"?p={value}"
    req = requests.get(URL, headers)
    soup = bs4.BeautifulSoup(html.unescape(req.text), "html.parser")
    soup = soup.find("div", {"class": "result"})
    lst = {}
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    p = {}
    flag = False
    for i in soup:
        if i.text in days:
            if p:
                lst.setdefault(key1, p)
            key1 = i.text
            p = {}
            flag = True
        elif flag:
            if 'ауд.' in i.text.split():
                d = i.find("span").text.split('–')
                aut = i.find("span").find("em").text.split()[-1]
                place = i.find("span").find("em").text.split('ауд.')[0].replace('–', '').replace(',', '').lstrip()
                group = i.find("div").find("span", {"class": "groups"}).text.split(':')[1]
                l = [*d[0].split(), d[1].lstrip(), place, aut, group]
                if len(l) == 5:
                    l = [1] + l
                p[key].append(l)
            else:
                key = i.text
                p.setdefault(key, [])
    lst.setdefault(key1, p)
    return lst



