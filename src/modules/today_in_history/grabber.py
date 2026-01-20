import json
import re
import requests
from datetime import datetime

from src.utils.get_template import get_template

HTTP_OK = list(range(200, 300))


def strip_html(text: str):
    return re.sub('<[^<]+?>', '', text)


def grab_data(lang="zh-CN"):
    now = datetime.now()
    month = "%02d" % now.month
    day = "%02d" % now.day

    url = f"https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json"
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    headers = {
        "host": "baike.baidu.com",
        "referer": "https://www.baidu.com",
        "User-Agent": agent,
        "Accept-Language": lang,
        "Accept": "text/html",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows"
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code not in HTTP_OK:
        raise KeyError(f"{'远程服务器返回错误' if lang == 'zh-CN' else 'Remote server returned an error'}:{response.status_code}")

    meta = json.loads(response.content.decode("utf-8"))
    data = meta[f"{month}"][f"{month}{day}"]

    for i in data:
        i["title"] = strip_html(i["title"])
        i["desc"] = strip_html(i["desc"])

    return data

def gen_list_item(day: dict):
    icon = day["pic_calendar"] if day['cover'] else "pack://application:,,,/images/Blocks/RedstoneLampOn.png"
    template = get_template("historytoday.fstring.xaml")
    output = template.format(
        title=day["title"],
        info=day["desc"],
        link=day['link'],
        cover=icon,
    )
    return output

def run():
    content = '<local:MyCard Title="历史上的今天" IsSwapped="True"><StackPanel Margin="8,38,8,15">' + "".join(
        [gen_list_item(day) for day in grab_data()]) + "</StackPanel></local:MyCard>"

    return content

if __name__ == "__main__":
    print(run())

