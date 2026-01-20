from pathlib import Path

from src.modules.wiki.builder import WikiXamlGenerator
from src.modules.minebbs.grabber import grab_all
from src.modules.minebbs.builder import run
from src.utils.get_template import get_template

HistoryOutput = Path(__file__).parent / "output" / "history"

if __name__ == "__main__":
    HistoryOutput.mkdir(parents=True, exist_ok=True)

    latest_post = ""
    previous_post = ""

    all_posts = grab_all()

    first_post: int = -1  # 标记第一个成功处理的博文

    for index, post in enumerate(all_posts):
        filename = (
            post.get("url").split("/")[-2].replace(".", "-")
            or "minecraft-net-deep-dives-unknown"
        )
        xaml_path = HistoryOutput / (filename + ".xaml")
        
        is_successful = False
        
        if xaml_path.exists():
            print(f"文件 {filename}.xaml 已存在，跳过抓取。")
            is_successful = True
        else:
            print(f"文件 {filename}.xaml 不存在，正在抓取和构建...")
            built_content = run(post)
            if built_content:
                # 保存为 XAML 和 JSON 文件
                with open(xaml_path, "w", encoding="utf-8") as xamlFile:
                    xamlFile.write(built_content)
                with open(
                    HistoryOutput / (filename + ".json"), "w", encoding="utf-8"
                ) as jsonFile:
                    jsonFile.write("{\"Title\": \"官方博文\"}")
                print(f"文件 {filename}.xaml 已成功保存。")
                is_successful = True
            else:
                print(f"构建 {filename}.xaml 失败。")

        if not is_successful:
            continue

        if first_post == -1:
            first_post = index

        # 制作主页入口点
        template = get_template("deepdives_link.fstring.xaml")
        is_latest = first_post == index
        
        title = (
            post.get("title").strip()
            + f"（{'最新' if is_latest else '历史'}博文）"
            .split("]")[-1]
            .replace(":", "：")
            .replace(": ", "：")
            .strip()
        )
        _date = post.get("publish_time_display")
        _author = post.get("author")

        built_template = template.format(
            lamp_status="On" if is_latest else "Off",
            title=title,
            info=f"更新于 {_date}，由 {_author} 翻译。",
            json_name=filename,
        )

        if is_latest:
            latest_post = built_template
        else:
            previous_post += built_template + "\n"

    generator = WikiXamlGenerator()
    generator.run(latest_post, previous_post)
