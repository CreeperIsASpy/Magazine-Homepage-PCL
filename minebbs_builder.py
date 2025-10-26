import re
from datetime import datetime
from minebbs_grabber import grab_post_lists, request_with_header
from minebbs_washer import extract_clean_text, clean_extracted_text

posts = [
    {'title': '[Minecraft.net | DEEP DIVES] 本月方块：陷阱箱', 'author': 'glorydark', 'publish_time_display': '2025/08/29',
     'url': 'https://www.minebbs.com/threads/minecraft-net-deep-dives.40420', 'labels': ['块讯']}]


def convert_text_to_xaml(content_part, image_map) -> str:
    """
    将特定格式的 Minecraft 文章文本转换为 PCL 使用的 XAML 格式。

    Args:
        content_part: 包含文章内容的字符串。
        image_map: 包含图片映射的字典。

    Returns:
        转换后的 XAML 格式字符串。
    """

    # --- 1. 分离内容与元数据 ---
    try:
        content_lines = content_part.strip().split('\n')
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"无法解析输入文本的结构或图片映射: {e}")

    for image_key, image_url in image_map.copy().items():
        if "mojavatar" in image_url.lower():
            del image_map[image_key]
            for line in content_lines[:]:
                if image_key in line:
                    content_lines.remove(line)

    # --- 2. 解析元数据 ---
    # 通常元数据在文章内容的最后一行
    author, source_date_str, eng_title, ch_title = "", "", "", ""
    if content_lines:
        meta_line = content_lines[-1]
        # 匹配 "作者 日期 英文标题"
        meta_match = re.match(
            r'^\s*(?P<author>.*?)\s+(?P<date>\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)\s+(?P<title>.*)', meta_line)
        if meta_match:
            author = meta_match.group('author').strip()
            # 格式化日期
            date_obj = datetime.strptime(meta_match.group('date').replace(' ', ''), '%Y年%m月%d日')
            source_date_str = date_obj.strftime('%Y-%m-%d')
            # 英文标题可能在同一行，也可能在文章开头
            if not eng_title:
                eng_title = meta_match.group('title').strip()
            content_lines = content_lines[:-1]  # 从内容中移除元数据行

    # --- 3. 构建 XAML 主体 ---
    xaml_parts = []

    # 查找文章的各级标题
    # 跳过开头的图片占位符和空行
    first_content_line_index = 0
    for i, line in enumerate(content_lines):
        if line.strip() and not line.strip().startswith('[%('):
            first_content_line_index = i
            break

    # 提取标题
    try:
        sub_title_eng = content_lines[first_content_line_index].strip()
        main_title_eng = content_lines[first_content_line_index + 1].strip()
        main_title_ch = content_lines[first_content_line_index + 2].strip()
        sub_title_eng_2 = content_lines[first_content_line_index + 3].strip()
        sub_title_ch_2 = content_lines[first_content_line_index + 4].strip()

        if not eng_title: eng_title = main_title_eng
        if not ch_title: ch_title = main_title_ch

        # 添加标题段落
        xaml_parts.append(f'<Paragraph Style="{{StaticResource H7}}">{sub_title_eng}</Paragraph>')
        xaml_parts.append(f'<Paragraph Style="{{StaticResource H2}}">{main_title_eng}</Paragraph>')
        xaml_parts.append(f'<Paragraph Style="{{StaticResource H2}}">{main_title_ch}</Paragraph>')
        xaml_parts.append(f'<Paragraph Style="{{StaticResource H7}}">{sub_title_eng_2}</Paragraph>')
        xaml_parts.append(f'<Paragraph Style="{{StaticResource H5}}">{sub_title_ch_2}</Paragraph>')

        # 更新循环起始位置
        content_start_index = first_content_line_index + 5
    except IndexError:
        # 如果标题结构不匹配，则正常处理
        content_start_index = first_content_line_index
        ch_title = "未知标题"  # 设置一个默认值

    # --- 4. 迭代处理文章内容 ---
    i = content_start_index
    while i < len(content_lines):
        line = content_lines[i].strip()
        if not line:
            i += 1
            continue

        # 处理图片
        if line.startswith('[%(') and line.endswith(')s]'):
            img_key = line[1:-1]  # 去掉首尾的中括号
            img_url = image_map.get(img_key, '')

            # 检查下一行是否为版权信息
            caption = ""
            if i + 1 < len(content_lines):
                next_line = content_lines[i + 1].strip()
                if next_line.lower().startswith('image credit:') or next_line.startswith('图片来源：'):
                    # 优先使用中文格式
                    caption_text = next_line.replace('Image credit:', '图片来源：').replace('//', '/').strip()
                    caption = f'<TextBlock Text="{caption_text}" Style="{{StaticResource imgTitle}}" />'
                    i += 1  # 跳过版权行
                    # 再检查下一行是否是中文版权
                    if i + 1 < len(content_lines):
                        next_next_line = content_lines[i + 1].strip()
                        if next_next_line.startswith('图片来源：'):
                            i += 1

            xaml_parts.append(f'''<BlockUIContainer>
<StackPanel Margin="0,4,0,4">
<Image Style="{{StaticResource InnerImage}}" Source="{img_url}"/>{caption}
</StackPanel> 
</BlockUIContainer>''')
            i += 1
        # 处理成对的中英文段落
        else:
            eng_para = line
            ch_para = ""
            if i + 1 < len(content_lines):
                ch_para = content_lines[i + 1].strip()
                # 假设中文段落不以'['开头，也不是常见的英文句子开头
                if ch_para and not ch_para.startswith('[') and not re.match(r'^[A-Z]', ch_para):
                    xaml_parts.append(
                        f'<Paragraph Margin="0,0" FontSize="12" Foreground="silver">{eng_para}</Paragraph>')
                    xaml_parts.append(f'<Paragraph Margin="0,0" Foreground="black">{ch_para}</Paragraph>')
                    i += 2
                else:
                    # 只有单行英文
                    xaml_parts.append(
                        f'<Paragraph Margin="0,0" FontSize="12" Foreground="silver">{eng_para}</Paragraph>')
                    i += 1
            else:
                # 只有最后一行英文
                xaml_parts.append(f'<Paragraph Margin="0,0" FontSize="12" Foreground="silver">{eng_para}</Paragraph>')
                i += 1

    flow_document_content = "\n".join(xaml_parts)

    # --- 5. 准备最终的 XAML 模板并填充 ---
    # 获取图片
    header_img_url = image_map.get('%(img1)s', '')

    # 获取当前日期
    last_update_str = datetime.now().strftime('%Y-%m-%d')

    # 构造原文链接
    original_url = f"https://www.minecraft.net/zh-hans/article/{eng_title.lower().replace(':', '').replace(' ', '-')}"

    final_xaml = f'''<StackPanel Margin="0,-10,0,0"
xmlns:sys="clr-namespace:System;assembly=mscorlib"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
xmlns:local="clr-namespace:PCL;assembly=Plain Craft Launcher 2">
<StackPanel.Resources>
<Style TargetType="FlowDocumentScrollViewer">
<Setter Property="IsSelectionEnabled" Value="False"/>
<Setter Property="VerticalScrollBarVisibility" Value="Hidden"/>
<Setter Property="Margin" Value="0"/>
</Style>
<Style TargetType="FlowDocument" >
<Setter Property="FontFamily" Value="Microsoft YaHei UI"/>
<Setter Property="FontSize" Value="14"/>
<Setter Property="TextAlignment" Value="Left"/>
</Style>
<Style TargetType="StackPanel" x:Key="ContentStack" >
<Setter Property="Margin" Value="20,20,20,20"/>
</Style>
<Style TargetType="local:MyCard" x:Key="Card" >
<Setter Property="Margin" Value="0,5"/>
</Style>
<Style TargetType="Image" x:Key="InnerImage" >
<Setter Property="MaxHeight" Value="500"/>
<Setter Property="HorizontalAlignment" Value="Center"/>
</Style>
<Style TargetType="TextBlock" >
<Setter Property="TextWrapping" Value="Wrap"/>
<Setter Property="HorizontalAlignment" Value="Left"/>
<Setter Property="FontSize" Value="14"/>
<Setter Property="Foreground" Value="Black"/>
</Style>
<Style TargetType="List" >
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush3}}"/>
<Setter Property="Margin" Value="20,0,0,0"/>
<Setter Property="MarkerStyle" Value="1"/>
<Setter Property="Padding" Value="0"/>
</Style>
<Style TargetType="ListItem" >
<Setter Property="Foreground" Value="Black"/>
<Setter Property="LineHeight" Value="22"/>
</Style
><Style TargetType="Paragraph" x:Key="H1" >
<Setter Property="FontSize" Value="24"/>
<Setter Property="Margin" Value="0,10,0,10"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush3}}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H2" >
<Setter Property="FontSize" Value="22"/>
<Setter Property="Margin" Value="0,10,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush3}}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H3" >
<Setter Property="FontSize" Value="18"/>
<Setter Property="Margin" Value="0,5,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush4}}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H5" >
<Setter Property="FontSize" Value="15"/>
<Setter Property="Margin" Value="0,3,0,5"/>
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush4}}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H7" >
<Setter Property="FontSize" Value="14"/>
<Setter Property="Margin" Value="0,2,0,2"/>
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush4}}"/>
</Style>
<Style TargetType="Border" x:Key="Quote" >
<Setter Property="BorderThickness" Value="5,0,0,0"/>
<Setter Property="BorderBrush" Value="{{DynamicResource ColorBrush4}}"/>
<Setter Property="Padding" Value="10,5"/>
<Setter Property="Margin" Value="0,5"/>
</Style>
<Style x:Key="imgTitle" TargetType="TextBlock">
  <Setter Property="FontSize" Value="14" />
  <Setter Property="Foreground" Value="#FF777777" />
  <Setter Property="HorizontalAlignment" Value="Center" />
  <Setter Property="Margin" Value="0,0,0,15" />
</Style>
<sys:String x:Key="TranslateIcon">
M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z
</sys:String>
<sys:String x:Key="CreeperIcon">
M213.333333 128a85.333333 85.333333 0 0 0-85.333333 85.333333v597.333334a85.333333 85.333333 0 0 0 85.333333 85.333333h597.333334a85.333333 85.333333 0 0 0 85.333333-85.333333V213.333333a85.333333 85.333333 0 0 0-85.333333-85.333333H213.333333z m0 64h597.333334c11.754667 0 21.333333 9.578667 21.333333 21.333333v597.333334c0 11.754667-9.578667 21.333333-21.333333 21.333333H213.333333c-11.754667 0-21.333333-9.578667-21.333333-21.333333V213.333333c0-11.754667 9.578667-21.333333 21.333333-21.333333z m64 106.666667a21.333333 21.333333 0 0 0-21.333333 21.333333v128a21.333333 21.333333 0 0 0 21.333333 21.333333h149.333334v-149.333333a21.333333 21.333333 0 0 0-21.333334-21.333333h-128z m149.333334 170.666666v85.333334h-64a21.333333 21.333333 0 0 0-21.333334 21.333333v160a32 32 0 1 0 64 0V704h213.333334v32a32 32 0 1 0 64 0V576a21.333333 21.333333 0 0 0-21.333334-21.333333h-64v-85.333334h-170.666666z m170.666666 0h149.333334a21.333333 21.333333 0 0 0 21.333333-21.333333v-128a21.333333 21.333333 0 0 0-21.333333-21.333333h-128a21.333333 21.333333 0 0 0-21.333334 21.333333v149.333333z
</sys:String>
<Style TargetType="Border" x:Key="HeadImageBorder" >
<Setter Property="HorizontalAlignment" Value="Center"/>
<Setter Property="BorderThickness" Value="4"/>
<Setter Property="VerticalAlignment" Value="Top"/>
<Setter Property="BorderBrush" Value="{{DynamicResource ColorBrush3}}"/>
<Setter Property="CornerRadius" Value="7"/>
<Setter Property="MaxHeight" Value="140"/>
</Style><Style TargetType="Border" x:Key="TitleBorder" >
<Setter Property="Margin" Value="0,-20,-1,10"/>
<Setter Property="Background" Value="{{DynamicResource ColorBrush3}}"/>
<Setter Property="Width" Value="170"/>
<Setter Property="Height" Value="30"/>
<Setter Property="CornerRadius" Value="7"/>
<Setter Property="BorderThickness" Value="0,0,0,2"/>
<Setter Property="BorderBrush" Value="{{DynamicResource ColorBrush2}}"/>
</Style><Style TargetType="TextBlock" x:Key="TitleBlock" >
<Setter Property="HorizontalAlignment" Value="Center"/>
<Setter Property="TextAlignment" Value="Center"/>
<Setter Property="VerticalAlignment" Value="Center"/>
<Setter Property="Foreground" Value="{{DynamicResource ColorBrush7}}"/>
<Setter Property="Width" Value="180"/>
<Setter Property="TextWrapping" Value="Wrap"/>
<Setter Property="FontSize" Value="18"/>
</Style>
</StackPanel.Resources>
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,0,0,6">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="{{DynamicResource ColorBrush5}}" CornerRadius="5" VerticalAlignment="Top" BorderBrush="{{DynamicResource ColorBrush3}}" Opacity="0.7">
    <Grid Margin="10,0,0,0">
        <TextBlock x:Name="NewsHint" FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#FF000000">
                🖼️ 欢迎使用杂志主页
    </TextBlock>
        <TextBlock x:Name="Hint2" FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#00000000">
                🖼️ 欢迎使用杂志主页
    </TextBlock>
    </Grid>
</Border>
</local:MyCard>
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,4,0,6">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="#FF797A" CornerRadius="5" VerticalAlignment="Top" BorderBrush="#D20103" Opacity="0.7">
    <Grid Margin="10,0,0,0">
        <TextBlock FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#FF000000">
                ⚠️ 此为杂志主页博文板块的历史留档文件，使用请遵循 CC-BY-NC-SA 4.0 !
    </TextBlock>
        <TextBlock FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#00000000">
                ⚠️ 此为杂志主页博文板块的历史留档文件，使用请遵循 CC-BY-NC-SA 4.0 !
    </TextBlock>
    </Grid>
</Border>
</local:MyCard>
<local:MyCard>
<StackPanel Style="{{StaticResource ContentStack}}">
<Border Style="{{StaticResource HeadImageBorder}}">
<Border.Background>
<ImageBrush ImageSource="{header_img_url}" Stretch="UniformToFill" />
</Border.Background>
<Image Source="{header_img_url}" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{{StaticResource TitleBorder}}">
<TextBlock Style="{{StaticResource TitleBlock}}" Text="{ch_title}" />
</Border><FlowDocumentScrollViewer>
<FlowDocument>
{flow_document_content}
</FlowDocument>
</FlowDocumentScrollViewer>
<StackPanel Margin="0,0,0,20">
<Grid VerticalAlignment="Center" Margin="0,10,20,0" HorizontalAlignment="Right">
<Grid.ColumnDefinitions>
<ColumnDefinition Width="64"/>
<ColumnDefinition Width="*"/>
<ColumnDefinition Width="64"/>
<ColumnDefinition Width="*"/>
</Grid.ColumnDefinitions>
<Grid.RowDefinitions>
<RowDefinition Height="42"/>
<RowDefinition />
</Grid.RowDefinitions>
<Path Grid.Column="0" Margin="0,0" Height="28" Fill="{{DynamicResource ColorBrush4}}"
                    Stretch="Uniform"
                    Data="M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z"/>
<TextBlock Grid.Column="1" Text="(MineBBS)Glorydark" FontSize="14" HorizontalAlignment="Right" VerticalAlignment="Center" Foreground="{{DynamicResource ColorBrush4}}"/>
<Path Grid.Column="2" Margin="8,0" Height="28" Fill="{{DynamicResource ColorBrush4}}"
                    Stretch="Uniform" HorizontalAlignment="Right"
                    Data="M14 21v-3.075l5.525-5.5q.225-.225.5-.325t.55-.1q.3 0 .575.113t.5.337l.925.925q.2.225.313.5t.112.55t-.1.563t-.325.512l-5.5 5.5zM4 20v-2.8q0-.85.438-1.562T5.6 14.55q1.55-.775 3.15-1.162T12 13q.925 0 1.825.113t1.8.362L12 17.1V20zm16.575-4.6l.925-.975l-.925-.925l-.95.95zM12 12q-1.65 0-2.825-1.175T8 8t1.175-2.825T12 4t2.825 1.175T16 8t-1.175 2.825T12 12"/>
<TextBlock HorizontalAlignment="Right" Grid.Column="3" Text="{author}" FontSize="14" VerticalAlignment="Center" Foreground="{{DynamicResource ColorBrush4}}"/>
<TextBlock Margin="0,2" Grid.Row="1" Grid.Column="1" Grid.ColumnSpan="2" HorizontalAlignment="Left" Text="最后更新: {last_update_str}" FontSize="12" Foreground="{{DynamicResource ColorBrush4}}"/>
<TextBlock Margin="0,2" Grid.Row="1" Grid.Column="3" Grid.ColumnSpan="2" HorizontalAlignment="Left" Text="源日期: {source_date_str}" FontSize="12" Foreground="{{DynamicResource ColorBrush4}}"/>
</Grid>
<local:MyIconTextButton Text="访问原址" ToolTip="在 Minecraft 官网上查看该页面原文" EventType="打开网页" Margin="8"
    EventData="{original_url}" LogoScale="1.05" Logo="{{StaticResource CreeperIcon}}" HorizontalAlignment="Left"/>
</StackPanel>
</StackPanel>
</local:MyCard>
</StackPanel>'''

    return final_xaml


if __name__ == "__main__":
    if posts:
        post = posts[0]  # （重要）只获取最新的一篇
        content = request_with_header(post.get('url'))
        clean_text, image_dict = extract_clean_text(content)
        print(convert_text_to_xaml(clean_extracted_text(clean_text), image_dict))
