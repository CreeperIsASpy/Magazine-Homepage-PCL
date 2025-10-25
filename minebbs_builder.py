from minebbs_washer import clean_extracted_text, extract_clean_text, extract_article_images
from minebbs_grabber import grab_post_lists, request_with_header

posts = grab_post_lists()


def convert_to_xaml(original_text, image_urls, author="Duncan Geere", source_date="2025-09-05",
                    last_updated="2025-09-05", original_url="https://www.minecraft.net/zh-hans/article/fern"):
    """
    将原始文本转换为XAML格式

    Args:
        original_text: 原始文本内容
        image_urls: 图片URL列表
        author: 作者
        source_date: 源日期
        last_updated: 最后更新日期
        original_url: 原文链接
    """

    # 解析文本内容
    lines = original_text.strip().split('\n')

    # 提取标题和副标题
    title_en = lines[0].replace('Taking Inventory: ', '')
    title_cn = lines[1].replace('背包盘点: ', '')
    subtitle_en = lines[2]
    subtitle_cn = lines[3]

    # 提取图片版权信息
    image_credits = []
    credit_en = ""
    credit_cn = ""

    # 提取正文内容和图片版权信息
    content_pairs = []
    current_en = ""
    current_cn = ""

    for i in range(4, len(lines)):
        line = lines[i].strip()
        if not line:
            continue

        # 提取图片版权信息
        if line.startswith('Image credit:'):
            credit_en = line.replace('Image credit: ', '')
            # 下一行应该是中文版权信息
            if i + 1 < len(lines) and lines[i + 1].startswith('图片来源：'):
                credit_cn = lines[i + 1].replace('图片来源： ', '')
                image_credits.append((credit_en, credit_cn))
            continue
        elif line.startswith('图片来源：'):
            continue  # 已经在上一行处理过了

        # 跳过特殊段落
        if line.startswith('注：') or line.startswith('Ferns in the real world'):
            continue

        # 判断是英文还是中文
        if all(ord(c) < 128 for c in line) and not any(char in line for char in ['：', '。', '，']):
            # 英文行
            if current_cn and current_en:
                content_pairs.append((current_en, current_cn))
                current_en = ""
                current_cn = ""
            current_en = line
        else:
            # 中文行
            current_cn = line
            if current_en:
                content_pairs.append((current_en, current_cn))
                current_en = ""
                current_cn = ""

    # 添加最后一对
    if current_en and current_cn:
        content_pairs.append((current_en, current_cn))

    # 构建XAML
    xaml_parts = []

    # 头部样式和警告卡片（保持不变）
    xaml_parts.append('''<StackPanel Margin="0,-10,0,0"
xmlns:sys="clr-namespace:System;assembly=mscorlib"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
xmlns:local="clr-namespace:PCL;assembly=Plain Craft Launcher 2">
<StackPanel.Resources>
<!--Styles Starts-->
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
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
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
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H2" >
<Setter Property="FontSize" Value="22"/>
<Setter Property="Margin" Value="0,10,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush3}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H3" >
<Setter Property="FontSize" Value="18"/>
<Setter Property="Margin" Value="0,5,0,5"/>
<Setter Property="FontWeight" Value="Bold"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H5" >
<Setter Property="FontSize" Value="15"/>
<Setter Property="Margin" Value="0,3,0,5"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
</Style>
<Style TargetType="Paragraph" x:Key="H7" >
<Setter Property="FontSize" Value="14"/>
<Setter Property="Margin" Value="0,2,0,2"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush4}"/>
</Style>
<Style TargetType="Border" x:Key="Quote" >
<Setter Property="BorderThickness" Value="5,0,0,0"/>
<Setter Property="BorderBrush" Value="{DynamicResource ColorBrush4}"/>
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
<Setter Property="BorderBrush" Value="{DynamicResource ColorBrush3}"/>
<Setter Property="CornerRadius" Value="7"/>
<Setter Property="MaxHeight" Value="140"/>
</Style><Style TargetType="Border" x:Key="TitleBorder" >
<Setter Property="Margin" Value="0,-20,-1,10"/>
<Setter Property="Background" Value="{DynamicResource ColorBrush3}"/>
<Setter Property="Width" Value="170"/>
<Setter Property="Height" Value="30"/>
<Setter Property="CornerRadius" Value="7"/>
<Setter Property="BorderThickness" Value="0,0,0,2"/>
<Setter Property="BorderBrush" Value="{DynamicResource ColorBrush2}"/>
</Style><Style TargetType="TextBlock" x:Key="TitleBlock" >
<Setter Property="HorizontalAlignment" Value="Center"/>
<Setter Property="TextAlignment" Value="Center"/>
<Setter Property="VerticalAlignment" Value="Center"/>
<Setter Property="Foreground" Value="{DynamicResource ColorBrush7}"/>
<Setter Property="Width" Value="180"/>
<Setter Property="TextWrapping" Value="Wrap"/>
<Setter Property="FontSize" Value="18"/>
</Style>
</StackPanel.Resources>
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,0,0,6">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="{DynamicResource ColorBrush5}" CornerRadius="5" VerticalAlignment="Top" BorderBrush="{DynamicResource ColorBrush3}" Opacity="0.7">
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
</local:MyCard>''')

    # 主内容卡片
    xaml_parts.append(f'''<local:MyCard>
<StackPanel Style="{{StaticResource ContentStack}}">
<Border Style="{{StaticResource HeadImageBorder}}">
<Border.Background>
<ImageBrush ImageSource="{image_urls[1] if len(image_urls) > 1 else image_urls[0]}" Stretch="UniformToFill" />
</Border.Background>
<Image Source="{image_urls[1] if len(image_urls) > 1 else image_urls[0]}" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{{StaticResource TitleBorder}}">
<TextBlock Style="{{StaticResource TitleBlock}}" Text="{title_cn}" />
</Border><FlowDocumentScrollViewer>
<FlowDocument>
<Paragraph Style="{{StaticResource H7}}">Taking Inventory: {title_en}</Paragraph>
<Paragraph Style="{{StaticResource H2}}">背包盘点：{title_cn}</Paragraph>
<Paragraph Style="{{StaticResource H7}}">{subtitle_en}</Paragraph>
<Paragraph Style="{{StaticResource H5}}">{subtitle_cn}</Paragraph>''')

    # 添加正文内容
    credit_inserted = False
    for i, (en_text, cn_text) in enumerate(content_pairs):
        # 在版权信息前插入图片
        if not credit_inserted and "Image credit:" in en_text:
            # 插入第一张图片（如果有版权信息）
            if image_credits and len(image_urls) > 0:
                credit_en, credit_cn = image_credits[0]
                xaml_parts.append(f'''<BlockUIContainer>
<StackPanel>
<Image Style="{{StaticResource InnerImage}}" Source="{image_urls[0]}"/>
<TextBlock Text="{credit_cn}" Style="{{StaticResource imgTitle}}" />
</StackPanel>
</BlockUIContainer>''')
            credit_inserted = True

        xaml_parts.append(f'''<Paragraph Margin="0,0" FontSize="12" Foreground="silver">{en_text}</Paragraph>
<Paragraph Margin="0,0" Foreground="black">{cn_text}</Paragraph>''')

    # 如果没有找到版权信息的位置，在内容中间插入图片
    if not credit_inserted and len(image_urls) > 0:
        # 在内容的大约1/3处插入第一张图片
        insert_position = max(1, len(content_pairs) // 3)
        for i, (en_text, cn_text) in enumerate(content_pairs):
            if i == insert_position and image_credits:
                credit_en, credit_cn = image_credits[0]
                xaml_parts.append(f'''<BlockUIContainer>
<StackPanel>
<Image Style="{{StaticResource InnerImage}}" Source="{image_urls[0]}"/>
<TextBlock Text="{credit_cn}" Style="{{StaticResource imgTitle}}" />
</StackPanel>
</BlockUIContainer>''')

            xaml_parts.append(f'''<Paragraph Margin="0,0" FontSize="12" Foreground="silver">{en_text}</Paragraph>
<Paragraph Margin="0,0" Foreground="black">{cn_text}</Paragraph>''')

    # 页脚信息
    xaml_parts.append(f'''</FlowDocument>
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
                    Data="{{StaticResource TranslateIcon}}"/>
<TextBlock Grid.Column="1" Text="(MineBBS)Glorydark" FontSize="14" HorizontalAlignment="Right" VerticalAlignment="Center" Foreground="{{DynamicResource ColorBrush4}}"/>
<Path Grid.Column="2" Margin="8,0" Height="28" Fill="{{DynamicResource ColorBrush4}}"
                    Stretch="Uniform" HorizontalAlignment="Right"
                    Data="M14 21v-3.075l5.525-5.5q.225-.225.5-.325t.55-.1q.3 0 .575.113t.5.337l.925.925q.2.225.313.5t.112.55t-.1.563t-.325.512l-5.5 5.5zM4 20v-2.8q0-.85.438-1.562T5.6 14.55q1.55-.775 3.15-1.162T12 13q.925 0 1.825.113t1.8.362L12 17.1V20zm16.575-4.6l.925-.975l-.925-.925l-.95.95zM12 12q-1.65 0-2.825-1.175T8 8t1.175-2.825T12 4t2.825 1.175T16 8t-1.175 2.825T12 12"/>
<TextBlock HorizontalAlignment="Right" Grid.Column="3" Text="{author}" FontSize="14" VerticalAlignment="Center" Foreground="{{DynamicResource ColorBrush4}}"/>
<TextBlock Margin="0,2" Grid.Row="1" Grid.Column="1" Grid.ColumnSpan="2" HorizontalAlignment="Left" Text="最后更新: {last_updated}" FontSize="12" Foreground="{{DynamicResource ColorBrush4}}"/>
<TextBlock Margin="0,2" Grid.Row="1" Grid.Column="3" Grid.ColumnSpan="2" HorizontalAlignment="Left" Text="源日期: {source_date}" FontSize="12" Foreground="{{DynamicResource ColorBrush4}}"/>
</Grid>
<local:MyIconTextButton Text="访问原址" ToolTip="在 Minecraft 官网上查看该页面原文" EventType="打开网页" Margin="8"
    EventData="{original_url}" LogoScale="1.05" Logo="{{StaticResource CreeperIcon}}" HorizontalAlignment="Left"/>
</StackPanel>
</StackPanel>
</local:MyCard>
</StackPanel>''')

    return '\n'.join(xaml_parts)


# 使用示例
if __name__ == "__main__":
    xaml_output = None
    if posts:
        post = posts[0]  # 只获取最新的一篇
        content = request_with_header(post.get('url'))
        original_text = clean_extracted_text(extract_clean_text(content))
        image_urls = extract_article_images(content)
        xaml_output = convert_to_xaml(original_text, image_urls)
    print(xaml_output)