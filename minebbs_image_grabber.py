from bs4 import BeautifulSoup
from minebbs_grabber import grab_post_lists, request_with_header

posts = grab_post_lists()

from bs4 import BeautifulSoup
import re


def extract_content_and_images(html_content):
    """
    正确提取文章内容和图片
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到文章正文区域
    article_body = soup.find('article', class_='message-body')
    if not article_body:
        return [], []

    paragraphs = []
    images = []

    # 查找所有图片容器
    image_wrappers = article_body.find_all('div', class_='bbImageWrapper')
    print(f"找到 {len(image_wrappers)} 个图片容器")

    for i, wrapper in enumerate(image_wrappers):
        img = wrapper.find('img')
        if img:
            # 尝试多种可能的属性获取图片URL
            src = (img.get('data-src') or
                   img.get('src') or
                   img.get('data-url'))
            if src:
                print(f"图片 {i + 1}: {src}")
                images.append({
                    "url": src,
                    "alt": img.get('alt', ''),
                    "title": wrapper.get('title', '')
                })

    # 提取文本内容
    bb_wrapper = article_body.find('div', class_='bbWrapper')
    if bb_wrapper:
        # 获取所有文本内容
        text_content = bb_wrapper.get_text()

        # 按行分割
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]

        # 配对英文和中文段落
        for i in range(0, len(lines) - 1, 2):
            if i + 1 < len(lines):
                en_line = lines[i]
                cn_line = lines[i + 1]

                # 简单的语言检测
                if (contains_mostly_english(en_line) and
                        contains_chinese(cn_line)):
                    paragraphs.append({
                        "english": en_line,
                        "chinese": cn_line
                    })

    return paragraphs, images


def contains_chinese(text):
    """检查文本是否包含中文字符"""
    return bool(re.search('[\u4e00-\u9fff]', text))


def contains_mostly_english(text):
    """检查文本是否主要是英文"""
    # 计算英文字母的比例
    english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    total_chars = sum(1 for c in text if c.isalpha())

    # 如果文本长度很短，可能是标题等，也认为是英文
    if len(text) < 20:
        return True

    return total_chars > 0 and english_chars / total_chars > 0.5


# 更直接的方法：使用正则表达式直接匹配图片URL
def extract_images_directly(html_content):
    """
    直接使用正则表达式从HTML中提取图片URL
    """
    # 匹配图片URL的模式
    img_patterns = [
        r'data-src="([^"]+)"',  # data-src属性
        r'src="([^"]+)"',  # src属性
        r'data-url="([^"]+)"'  # data-url属性
    ]

    images = []
    for pattern in img_patterns:
        matches = re.findall(pattern, html_content)
        for match in matches:
            # 过滤掉base64编码的图片和空URL
            if match and not match.startswith('data:') and 'minecraft.net' in match:
                images.append({"url": match})

    return images


# 使用示例
if __name__ == "__main__":
    if posts:
        post = posts[0]  # 只获取最新的一篇
        content = request_with_header(post.get('url'))
    # 假设html_content是你的HTML内容
    # 方法1: 使用BeautifulSoup提取
    paragraphs, images = extract_content_and_images(content)

    print("段落信息:")
    for i, para in enumerate(paragraphs):
        print(f"\n段落 {i}:")
        if para['english']:
            print(f"  英文: {para['english'][:100]}{'...' if len(para['english']) > 100 else ''}")
        if para['chinese']:
            print(f"  中文: {para['chinese'][:100]}{'...' if len(para['chinese']) > 100 else ''}")

    print(f"\n图片信息 (方法1): {len(images)} 张")
    for img in images:
        print(f"  图片: {img['url']}")

    # 方法2: 直接使用正则表达式
    direct_images = extract_images_directly(content)
    print(f"\n图片信息 (方法2): {len(direct_images)} 张")
    for img in direct_images:
        print(f"  图片: {img['url']}")