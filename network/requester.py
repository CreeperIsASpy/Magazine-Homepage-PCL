from typing import Optional, Dict, Union
import requests

default_header = {
    "User-Agent": "PCL2 Magazine Homepage Bot/0.0.0",
}

def get_text(
    url: str,
    params: Optional[Dict[str, Union[str, int]]] = None,
    headers: Optional[Dict[str, str]] = default_header,
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
        response.raise_for_status()  # 抛出 4xx/5xx 错误
        if encoding:
            response.encoding = encoding  # 手动设置编码（如 'utf-8'、'gbk'）
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 请求失败: {e}")
        return None
