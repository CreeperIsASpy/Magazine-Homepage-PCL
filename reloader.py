import datetime
import hashlib
import re
import time
import json
import struct
from typing import Optional, Dict, Union

import requests
from bs4 import BeautifulSoup

VERSION = "0.0"
headers = {
    'User-Agent':
        f'PCL2 Magazine Homepage Bot/{VERSION}',
}

global obj


def get_text(
        url: str,
        params: Optional[Dict[str, Union[str, int]]] = None,
        headers: Optional[Dict[str, str]] = headers,
        timeout: float = 10.0,
        allow_redirects: bool = True,
        encoding: Optional[str] = None
) -> Optional[str]:
    """
    发起通用 GET 请求并返回响应文本。

    此函数封装 requests.get，用于向指定 URL 发送 GET 请求。支持传入查询参数、请求头、自定义编码、
    是否跟随重定向等设置。请求成功时返回响应文本；若出现异常则返回 None。

    参数:
        url (str): 请求地址。
        params (dict[str, str | int], 可选): URL 查询参数。
        headers (dict[str, str], 可选): 请求头信息。默认为 default_header。
        timeout (float): 请求超时时间（单位：秒），默认 10.0。
        allow_redirects (bool): 是否允许自动重定向，默认 True。
        encoding (str, 可选): 手动指定响应的编码格式（如 'utf-8'、'gbk' 等）。

    返回:
        str | None: 响应内容字符串；若请求失败则返回 None。

    异常:
        无抛出；若请求失败，会捕获异常并打印错误信息。
    """
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=timeout,
            allow_redirects=allow_redirects
        )
        response.raise_for_status()  # 根据状态码抛出错误
        if encoding:
            response.encoding = encoding  # 手动设置编码（如 'utf-8'、'gbk'）
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 请求失败: {e}")
        return None


def get_wiki_data():
    """
    获取中文 Minecraft Wiki 的页面解析数据。

    此函数使用 get_text() 向 zh.minecraft.wiki 的 API 发起请求，获取 "Minecraft_Wiki" 页面
    的解析内容（以 JSON 格式返回）。若请求失败，则抛出异常终止程序。

    参数:
        无。

    返回:
        dict: 从 Wiki API 返回的解析后的 JSON 数据。

    异常:
        Exception: 若请求失败（无响应），抛出异常并中止。
    """
    resp: str | None = get_text("https://zh.minecraft.wiki/api.php", {
        "action": "parse",
        "format": "json",
        "page": "Minecraft_Wiki"
    })
    if not resp:
        raise Exception("No response from https://zh.minecraft.wiki/w/api.php, ABORTED!")
    html = json.loads(resp)["parse"]["text"]["*"]

    global obj
    obj = BeautifulSoup(html, 'html.parser')

    return html


def while_delete(del_txts, txt, replacement=''):
    for del_txt in del_txts:
        while del_txt in txt:
            txt = txt.replace(del_txt, replacement)
    return txt


def get_news_card():
    response = requests.get("https://news.bugjump.net/apis/versions/latest-card")
    if response.status_code != 200:
        _404 = f"""<local:MyCard>
<StackPanel Style="{{StaticResource ContentStack}}">
<Border Style="{{StaticResource HeadImageBorder}}">
<local:MyImage Source="https://http.cat/{response.status_code}.jpg" Stretch="UniformToFill" VerticalAlignment="Center"/>
</Border>
<Border Style="{{StaticResource TitleBorder}}">
<TextBlock Style="{{StaticResource TitleBlock}}" Text="{response.status_code}" />
</Border>
<TextBlock TextWrapping="Wrap" Text="新闻主页API 出错啦！可以去提醒一下……"
    HorizontalAlignment="Center" VerticalAlignment="Bottom" FontSize="16" Foreground="{{DynamicResource ColorBrush4}}" Margin="8,8,8,8"/>
</StackPanel>
</local:MyCard>"""

    result = str(response.text)
    return result


def get_link_txt(txt):
    raw_links = re.findall(r'<a href=".*?" title=".*?"', txt, re.S)
    links = {}
    for link in raw_links:
        key = re.findall(r'title="(.*?)"', link, re.M)[0]
        ref = re.findall(r'href="(.*?)"', link, re.M)[0]
        links[key] = "https://zh.minecraft.wiki" + ref
    return links


def link_to_xaml(lk):
    xaml = f'''<Underline><local:MyTextButton EventType="打开网页" \
EventData="{lk[1]}" Margin="0,0,0,-8">{lk[0]}</local:MyTextButton></Underline>'''
    return xaml


def gr():
    # 这个函数做的非常精密，我虽然觉得很屎山，但是一改就炸……
    # 别骂了别骂了

    origin = str(obj.select_one("div.mp-inline-sections > div.mp-left > div:nth-child(5)").text)
    result = origin.lstrip("\n特色条目").strip().split("。")
    result = [i.strip("\n") for i in result]
    #   print(result)
    result = [f"""<ListItem><Paragraph Foreground="{{DynamicResource ColorBrush1}}">{i}。</Paragraph></ListItem>""" for i in result]

    # 获取原始HTML内容
    html_content = str(obj.select_one("div.mp-inline-sections > div.mp-left > div:nth-child(5)"))

    # 提取所有链接
    links = get_link_txt(html_content)

    # 按照键的长度降序排序，确保先替换长的复合词
    sorted_links = sorted(links.items(), key=lambda x: len(x[0]), reverse=True)

    # 处理每个段落
    for i, item in enumerate(result):
        # 提取段落文本内容（不包含ListItem和Paragraph标签）
        paragraph_text = re.search(
            r'<ListItem><Paragraph Foreground="\{DynamicResource ColorBrush1}">(.*?)</Paragraph></ListItem>', item)
        if paragraph_text:
            text_content = paragraph_text.group(1)

            # 创建一个标记数组，记录哪些位置已经被替换过
            text_length = len(text_content)
            replaced = [False] * text_length

            # 对每个链接进行替换，按长度降序处理
            for key, url in sorted_links:
                # 查找所有匹配位置
                start_pos = 0
                while True:
                    pos = text_content.find(key, start_pos)
                    if pos == -1:
                        break

                    # 检查这个位置是否已经被替换过
                    if not any(replaced[pos:pos + len(key)]):
                        # 标记这些位置为已替换
                        for j in range(pos, pos + len(key)):
                            if j < text_length:
                                replaced[j] = True

                        # 替换文本
                        before = text_content[:pos]
                        after = text_content[pos + len(key):]
                        text_content = before + link_to_xaml((key, url)) + after

                        # 更新标记数组以适应新的文本长度
                        new_length = len(text_content)
                        replaced = replaced[:pos] + [True] * len(link_to_xaml((key, url))) + replaced[pos + len(key):]

                    # 移动到下一个可能的位置
                    start_pos = pos + 1

            # 重新组装段落
            result[i] = f"""<ListItem><Paragraph Foreground="{{DynamicResource ColorBrush1}}">{text_content}</Paragraph></ListItem>"""

    result.pop()
    return result


def gs():
    img_src = 'https://zh.minecraft.wiki' + obj.select_one("div.mp-featured-img img").get('src')
    img_src = re.sub(r'&', '&amp;', img_src)
    return img_src


def get_version():
    dt = datetime.datetime.now().strftime("%y%m%d")
    hsh = hashlib.md5(struct.pack('<f', time.time())).hexdigest()
    vid = f"{dt}:{hsh[:7]}"
    with open("Custom.xaml.ini", 'w') as f:
        f.write(f"{dt}:{hsh}")
    return vid


def get_wiki_page():
    return list(get_link_txt(str(obj.select_one("div.mp-inline-sections > div.mp-left > div:nth-child(5)"))).values())[
        0]


def get_topic():
    return list(get_link_txt(str(obj.select_one("div.mp-inline-sections > div.mp-left > div:nth-child(5)"))).keys())[0]


def validate_template(template):
    # 查找未转义的独立 % 符号（非占位符）
    standalone_percent = re.findall(r"(?<!%)%(?!\()", template)
    if standalone_percent:
        print(f"发现未转义的 % 符号: {len(standalone_percent)} 处")

    # 查找占位符
    placeholders = re.findall(r"%\((\w+)\)s", template)
    print(f"发现占位符：{len(placeholders)} 处")


def update():
    now = datetime.datetime.now()
    with open("template.fstring", "r", encoding="utf-8") as f:
        content_text = f.read()

    #   validate_template(content_text) 防止出现 f-string 问题
    content_text = re.sub(r"(?<!%)%(?!\()", "%%", content_text)
    #   test = "{%(datetime)s} \n %(WikiPage)s \n %(topic)s \n %(intro)s \n %(intro_2)s \n %(body)s \n %(alt)s \n %(img)s \n %(NewsCard)s \n %(version)s"
    meta = {
        'WikiPage': get_wiki_page(),
        'version': get_version(),
        'img': gs(),
        'topic': get_topic(),
        'intro': gr()[0],
        'intro_2': gr()[1],
        'body': '\n'.join(gr()[2:]),
        'datetime': f'最后更新: {now.strftime("%Y-%m-%d")}',
        'NewsCard': get_news_card()
    }
    for k, v in meta.items():
        meta[k] = str(v)

    #   content_text = re.sub(r'}', "}}", re.sub(r'\{', '{{', content_text))
    content_text = content_text.replace("}", "}}").replace("{", "{{")
    #   output = re.sub(r'}}', "}", re.sub(r'\{\{', '{', (content_text % meta)))
    output = (content_text % meta).replace("}}", "}").replace("{{", "{")
    print(output)
    with open("Custom.xaml", "w", encoding='UTF-8') as f:
        f.write(output)


def print_out():
    print(f'INTRO $1:\n\t{gr()[0]}\n')
    print(f'INTRO $2:\n\t{gr()[1]}\n')
    BODYTXT = '\n'.join(gr()[2:-1])
    print(f'BODY:    \n{BODYTXT}\n')
    ALTTXT = gr()[-1].replace("<ListItem>", '').replace("</ListItem>", '')
    print(f'ALT:\n\t{ALTTXT}\n')
    print(f'IMG: \n\t{gs()}\n')
    print(f'$NEWSCARD:     \n{get_news_card()}\n')
    print(f'$VID:     {get_version()}')


if __name__ == "__main__":
    get_wiki_data()
    update()
