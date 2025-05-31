from bs4 import BeautifulSoup

def prase_main_card(html_data: str):
    """
    解析 HTML 中的主卡片内容区域。

    此函数使用 BeautifulSoup 对传入的 HTML 字符串进行解析，并查找特定位置的主内容区域：
    通过选择器 "div.mp-inline-sections > div.mp-left > div:nth-child(5)" 进行定位。

    参数:
        html_data (str): HTML 源代码字符串。

    返回:
        bs4.element.Tag: 被匹配到的主卡片内容区域的 BeautifulSoup 标签对象。

    异常:
        Exception: 如果未能找到指定的主卡片区域，则抛出异常提示。
    """
    soup = BeautifulSoup(html_data, 'html.parser')
    card_content = soup.select_one("div.mp-inline-sections > div.mp-left > div:nth-child(5)")
    if not card_content: raise Exception("Card content is not found, ABORTED!")
    return card_content
