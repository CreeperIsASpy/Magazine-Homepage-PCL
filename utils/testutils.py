from os import path, mkdir

def dump_any_to_file(format: str, content: str, name: str = "test") -> None:
    """
    将任意字符串内容写入文件（用于调试或内容输出）。

    此函数用于快速将字符串内容写入指定后缀的文件，便于本地调试、查看接口返回或中间结果。
    文件以 UTF-8 编码保存，默认文件名为 "test"。

    参数:
        format (str): 文件后缀名（如 'txt'、'html'、'json'）。
        content (str): 要写入的字符串内容。
        name (str): 文件名（不包含后缀），默认值为 "test"。

    返回:
        None: 无返回值。
    """
    if not path.exists(".temp/"): mkdir(".temp")
    with open(f".temp/{name}.{format}", "w", encoding="utf-8") as f:
        f.write(content)