from .requester import get_text
import json

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
    if not resp: raise Exception("No response from https://zh.minecraft.wiki/w/api.php, ABORTED!")
    return json.loads(resp)