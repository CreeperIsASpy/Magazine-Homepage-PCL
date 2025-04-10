import datetime
import hashlib
import re
import time
import struct

import requests
from bs4 import BeautifulSoup

def get_origin():
    response = requests.get("https://zh.minecraft.wiki").text
    obj = BeautifulSoup(response, 'html.parser')
    while not response or not obj:
        time.sleep(20)
        response = requests.get("https://zh.minecraft.wiki").text
        obj = BeautifulSoup(response, 'html.parser')

get_origin()


def while_delete(del_txts, txt, replacement=''):
    for del_txt in del_txts:
        while del_txt in txt:
            txt = txt.replace(del_txt, replacement)
    return txt


def get_news_card():
    resp = str(requests.get("https://news.bugjump.net/apis/versions/latest-card").text)
    return resp


def gr():
    origin = obj.find('div', class_="weekly-content").text
    result = origin.strip().split("。")
    result = [i.strip("\n") for i in result]
    result = [f"<ListItem><Paragraph>{i}。</Paragraph></ListItem>" for i in result]
    links = get_link_txt(str(obj.find('div', class_="weekly-content")))
    for k, v in links.items():
        result = [i.replace(k, link_to_xaml((k, v))) if k in i else i for i in result]
    result.pop()
    result[-1] = while_delete((' Margin="0,0,0,-8"',), result[-1])
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


def gs():
    img_src = 'https://zh.minecraft.wiki' + obj.find('div', class_='weekly-image').find('img')['src']
    img_src = re.sub(r'&', '&amp;', img_src)
    return img_src


def get_version():
    dt = datetime.datetime.now().strftime("%y%m%d")
    hsh = hashlib.md5(struct.pack('<f', time.time())).hexdigest()
    vid = f"{dt}:{hsh[:7]}"
    with open("Custom.xaml.ini", 'w') as f:
        f.write(f"{dt}:{hsh}")
    return vid


def get_img_alt():
    return gr()[-1].replace("<ListItem>", '').replace("</ListItem>", '')


def get_wiki_page():
    return list(get_link_txt(str(obj.find('div', class_="weekly-content"))).values())[0]


def get_topic():
    return list(get_link_txt(str(obj.find('div', class_="weekly-content"))).keys())[0]


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
    content_text = '''<!-- "The Magazine Homepage for PCL2" made by CreeperIsASpy. Copyright 2025 CreeperIsASpy, all rights reserved. (CC BY-NC-SA 4.0).-->
<!-- 由 仿生猫梦见苦力怕 制作该 "PCL2 杂志主页"。@仿生猫梦见苦力怕 / CreeperIsASpy 版权所有，保留所有权利。（使用CC BY-NC-SA 4.0 授权代码部分内容）。-->

<StackPanel Margin="0,-10,0,0"
xmlns:sys="clr-namespace:System;assembly=mscorlib"
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
xmlns:local="clr-namespace:PCL;assembly=Plain Craft Launcher 2">
<StackPanel.Resources>
<!--Styles Starts-->
<Style x:Key="TabControlStyle" TargetType="{x:Type TabControl}">
    <Setter Property="Padding" Value="2"/>
    <Setter Property="HorizontalContentAlignment" Value="Center"/>
    <Setter Property="VerticalContentAlignment" Value="Center"/>
    <Setter Property="Background" Value="Transparent"/>
    <Setter Property="BorderBrush" Value="#FFACACAC"/>
    <Setter Property="BorderThickness" Value="0"/>
    <Setter Property="Foreground" Value="{DynamicResource {x:Static SystemColors.ControlTextBrushKey}}"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="{x:Type TabControl}">
                    <Grid x:Name="templateRoot" ClipToBounds="True" SnapsToDevicePixels="True" KeyboardNavigation.TabNavigation="Local">
                        <Grid.ColumnDefinitions>
                            <ColumnDefinition x:Name="ColumnDefinition0"/>
                            <ColumnDefinition x:Name="ColumnDefinition1" Width="0"/>
                        </Grid.ColumnDefinitions>
                        <Grid.RowDefinitions>
                            <RowDefinition x:Name="RowDefinition0" Height="Auto"/>
                            <RowDefinition x:Name="RowDefinition1" Height="*"/>
                        </Grid.RowDefinitions>
                    <UniformGrid x:Name="HeaderPanel" Rows="1" Background="Transparent" Grid.Column="0" IsItemsHost="True" Margin="0" Grid.Row="0" KeyboardNavigation.TabIndex="1" Panel.ZIndex="1"/>
                    <Line X1="0" X2="{Binding ActualWidth, RelativeSource={RelativeSource Self}}" Stroke="White" StrokeThickness="0.1" VerticalAlignment="Bottom" Margin="0 0 0 1" SnapsToDevicePixels="True"/>
                    <Border x:Name="ContentPanel" BorderBrush="{DynamicResource ColorBrush2}" BorderThickness="0" Background="Transparent" Grid.Column="0" KeyboardNavigation.DirectionalNavigation="Contained" Grid.Row="1" KeyboardNavigation.TabIndex="2" KeyboardNavigation.TabNavigation="Local" CornerRadius="7">
                        <ContentPresenter x:Name="PART_SelectedContentHost" ContentTemplate="{TemplateBinding SelectedContentTemplate}" Content="{TemplateBinding SelectedContent}" ContentStringFormat="{TemplateBinding SelectedContentStringFormat}" ContentSource="SelectedContent" Margin="0" SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}"/>
                    </Border>
                </Grid>
                <ControlTemplate.Triggers>
                    <Trigger Property="TabStripPlacement" Value="Bottom">
                        <Setter Property="Grid.Row" TargetName="HeaderPanel" Value="1"/>
                        <Setter Property="Grid.Row" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Height" TargetName="RowDefinition0" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition1" Value="Auto"/>
                    </Trigger>
                    <Trigger Property="TabStripPlacement" Value="Left">
                        <Setter Property="Grid.Row" TargetName="HeaderPanel" Value="0"/>
                        <Setter Property="Grid.Row" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Grid.Column" TargetName="HeaderPanel" Value="0"/>
                        <Setter Property="Grid.Column" TargetName="ContentPanel" Value="1"/>
                        <Setter Property="Width" TargetName="ColumnDefinition0" Value="Auto"/>
                        <Setter Property="Width" TargetName="ColumnDefinition1" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition0" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition1" Value="0"/>
                    </Trigger>
                    <Trigger Property="TabStripPlacement" Value="Right">
                        <Setter Property="Grid.Row" TargetName="HeaderPanel" Value="0"/>
                        <Setter Property="Grid.Row" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Grid.Column" TargetName="HeaderPanel" Value="1"/>
                        <Setter Property="Grid.Column" TargetName="ContentPanel" Value="0"/>
                        <Setter Property="Width" TargetName="ColumnDefinition0" Value="*"/>
                        <Setter Property="Width" TargetName="ColumnDefinition1" Value="Auto"/>
                        <Setter Property="Height" TargetName="RowDefinition0" Value="*"/>
                        <Setter Property="Height" TargetName="RowDefinition1" Value="0"/>
                    </Trigger>
                    <Trigger Property="IsEnabled" Value="False">
                        <Setter Property="TextElement.Foreground" TargetName="templateRoot" Value="{DynamicResource {x:Static SystemColors.GrayTextBrushKey}}"/>
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
<Style x:Key="TabItemStyle" TargetType="{x:Type TabItem}">
    <Setter Property="Foreground" Value="Black"/>
    <Setter Property="Background" Value="Transparent"/>
    <Setter Property="BorderBrush" Value="#fff"/>
    <Setter Property="Margin" Value="0,0,0,8"/>
    <Setter Property="HorizontalContentAlignment" Value="Stretch"/>
    <Setter Property="VerticalContentAlignment" Value="Stretch"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="{x:Type TabItem}">
                <Grid x:Name="templateRoot"  SnapsToDevicePixels="True" Background="Transparent">
                    <Grid.ColumnDefinitions>
                        <ColumnDefinition Width="*"/>
                    </Grid.ColumnDefinitions>
                    <Border x:Name="ContentPanel" BorderBrush="{DynamicResource ColorBrush2}" BorderThickness="0,0,0,2" Background="White" Grid.Column="0" KeyboardNavigation.DirectionalNavigation="Contained"
                        Grid.Row="0" KeyboardNavigation.TabIndex="2" KeyboardNavigation.TabNavigation="Local" CornerRadius="7" Height="30" Margin="2,0,2,0"/>
                    <TextBlock x:Name="txt" Visibility="Visible" VerticalAlignment="Center" HorizontalAlignment="Center"
                    Text="{TemplateBinding Header}" ToolTip="{TemplateBinding Header}" Foreground="{TemplateBinding Foreground}" TextTrimming="CharacterEllipsis"/>
                </Grid>
                <ControlTemplate.Triggers>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsMouseOver, RelativeSource={RelativeSource Self}}" Value="true"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Top"/>
                        </MultiDataTrigger.Conditions>

                        <Setter Property="Foreground" TargetName="txt" Value="Blue"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Left"/>
                        </MultiDataTrigger.Conditions>
                            <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Bottom"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Right"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>
                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsEnabled, RelativeSource={RelativeSource Self}}" Value="false"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Top"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Opacity" TargetName="templateRoot" Value="0.56"/>
                    </MultiDataTrigger>

                    <MultiDataTrigger>
                        <MultiDataTrigger.Conditions>
                            <Condition Binding="{Binding IsSelected, RelativeSource={RelativeSource Self}}" Value="true"/>
                            <Condition Binding="{Binding TabStripPlacement, RelativeSource={RelativeSource FindAncestor, AncestorLevel=1, AncestorType={x:Type TabControl}}}" Value="Top"/>
                        </MultiDataTrigger.Conditions>
                        <Setter Property="Panel.ZIndex" Value="1"/>
                        <Setter Property="Foreground" TargetName="txt" Value="Green"/>
                    </MultiDataTrigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
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
<sys:String x:Key="WikiIcon">
M172.61,196.65h31a7.69,7.69,0,0,1,7.62,6.65l11.19,80.95c2.58,20.09,5.16,40.18,7.73,60.79h1c3.61-20.61,7.47-41,11.34-60.79l18.23-81.58a7.7,7.7,0,0,1,7.52-6h26.58a7.7,7.7,0,0,1,7.51,6l18.48,81.6c3.86,19.57,7.21,40.18,11.07,60.79h1.29c2.32-20.61,4.9-41,7.22-60.79l11.67-81a7.7,7.7,0,0,1,7.62-6.6h27.72a7.7,7.7,0,0,1,7.59,9L364.41,382.2a7.69,7.69,0,0,1-7.58,6.38H311.61a7.7,7.7,0,0,1-7.54-6.14l-16-77.33c-3.09-14.68-5.67-30.14-7.47-44.57h-1c-2.58,14.43-4.9,29.89-7.73,44.57L256.34,382.4a7.7,7.7,0,0,1-7.54,6.18H204.6a7.69,7.69,0,0,1-7.58-6.32L165,205.72A7.71,7.71,0,0,1,172.61,196.65ZM286.87,507.39,159.71,455.25v22.82L97.54,451.18v-23.3l-89-2,9.54-119.29H44.78V291.24L31.45,280.81V247l14.09-4.23L45,227.13,63.33,220V207.1l5.51-2v-16.2l15.65-4.93V167.63l24.06-11.81,1.65-21.95,4.94-1.72-2-1V95.6h13V89.45l27.56-14.79L169,84.43,185.79,76l21.47,15.34,8.1,1v7.91h6.51l60.65-30.56,8,3.49,17-12.08L324,71l.12-2.19,39.15-22,18.06,12.53h26.37l3.79-1.62,36.38,27.4v28.77l16.81,8.15V149l6.08,3V164l10.15,5.51v11.32h9v11.52l1,0c1.54,0,3.44.08,5.91,0l15.13-.13V212.7h9.28v49.71h-5.8v36.1l-16,9h56l6.78,119.85-116.84-1.4Zm-157.16-85.7h27.23l128.51,52.7,152.82-78.54,92.15,1.1-3.36-59.47H456.67V325.89h-5.8v-40l22.37,1.81L485.36,281v-.86h-7.24V268.5h-7V236.33l-11.31,8.61V210.82h-9V187.35l-10.15-5.51V170.59l-11.59-5.79V138.2l-38.25-18.53,26.95-17.27v-2.29l-10.59-8-24.49,10.41V89.37H371.9l-10.35-7.18-8.38,4.7-.6,11.32-22.31,11.61-21.4-12.9L294,107.45l-10.58-4.63L192,148.87V130.24h-6.67V119l-1-.12V121l-28.12,4v.58h-7.1L151.49,150l-5.17-.37.11,3.38-1.27.44,14.7,10.59-45.37,22.26V206l-15.65,4.93V226l-5.51,2v12.57l-17.6,6.81.61,17.43-12,3.61,10.46,8.18v1.59h11.6v24l43.44,34.42h-84l-4.8,60,86.54,1.93v32.93l2.17.94ZM476.3,232.41h5.58v-4.25Z
</sys:String>
<sys:String x:Key="TranslateIcon">
M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z
</sys:String>
<sys:String x:Key="CreeperIcon">
M213.333333 128a85.333333 85.333333 0 0 0-85.333333 85.333333v597.333334a85.333333 85.333333 0 0 0 85.333333 85.333333h597.333334a85.333333 85.333333 0 0 0 85.333333-85.333333V213.333333a85.333333 85.333333 0 0 0-85.333333-85.333333H213.333333z m0 64h597.333334c11.754667 0 21.333333 9.578667 21.333333 21.333333v597.333334c0 11.754667-9.578667 21.333333-21.333333 21.333333H213.333333c-11.754667 0-21.333333-9.578667-21.333333-21.333333V213.333333c0-11.754667 9.578667-21.333333 21.333333-21.333333z m64 106.666667a21.333333 21.333333 0 0 0-21.333333 21.333333v128a21.333333 21.333333 0 0 0 21.333333 21.333333h149.333334v-149.333333a21.333333 21.333333 0 0 0-21.333334-21.333333h-128z m149.333334 170.666666v85.333334h-64a21.333333 21.333333 0 0 0-21.333334 21.333333v160a32 32 0 1 0 64 0V704h213.333334v32a32 32 0 1 0 64 0V576a21.333333 21.333333 0 0 0-21.333334-21.333333h-64v-85.333334h-170.666666z m170.666666 0h149.333334a21.333333 21.333333 0 0 0 21.333333-21.333333v-128a21.333333 21.333333 0 0 0-21.333333-21.333333h-128a21.333333 21.333333 0 0 0-21.333334 21.333333v149.333333z
</sys:String>
<sys:String x:Key="thanks" xml:space="preserve">鸣谢|一些对主页开发有帮助的人:
土星仙鹤                                     @ QQ(2480379448) 主页初版的首个测试者!
ess的大清要活了 ~喵                   @ QQ(1837750594) 带我接触了自定义主页,没有他我可能到现在还不知道主页是什么!
最亮的信标                                  @ Github(Nattiden) 提供主页模板,本主页使用他的NewsHomepage为基础开发!
Mfn233                                       @ Github(Mfn233) 为主页提供最开始的技术支持支持和鼓励!
主页群的各位                               @ QQ群(828081791等) 为主页的开发提供持续的精神力量,快来一起咕咕咕!
凌云                                            @ Github(JingHai-Lingyun) 提供挂载主页的oss,真的真的非常感激!
排列没啥顺序，个个我都非常非常非常谢谢你们!</sys:String>
<sys:String x:Key="WikiPage">%(WikiPage)s</sys:String>
<sys:String x:Key="VersionID">%(version)s</sys:String>
<BitmapImage x:Key="Img" UriSource="%(img)s"/>
<sys:String x:Key="Topic">%(topic)s</sys:String>
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
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,-2,0,5">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="{DynamicResource ColorBrush5}" CornerRadius="5" VerticalAlignment="Top" BorderBrush="{DynamicResource ColorBrush3}" Opacity="0.7">
    <Grid Margin="10,0,0,0">
        <TextBlock FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#FF000000">
                📚 欢迎使用杂志主页
    </TextBlock>
        <TextBlock FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#00000000">
                📚 欢迎使用杂志主页
    </TextBlock>
    </Grid>
</Border>
</local:MyCard>

<TabControl Style="{StaticResource TabControlStyle}" FontFamily="Microsoft YaHei UI" FontSize="17">
    <TabItem Header="中文 Minecraft Wiki 摘录 - 本周页面" Style="{StaticResource TabItemStyle}">
<local:MyCard>
<StackPanel Style="{StaticResource ContentStack}">
<Border Style="{StaticResource HeadImageBorder}">
<Border.Background>
<ImageBrush ImageSource="{StaticResource Img}" Stretch="UniformToFill" />
</Border.Background>
<Image Source="{StaticResource Img}" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{StaticResource TitleBorder}">
<TextBlock Style="{StaticResource TitleBlock}" Text="{StaticResource Topic}" />
</Border><FlowDocumentScrollViewer >
<FlowDocument>
    <Paragraph Style="{StaticResource H2}">
        <Run FontSize="22" FontWeight="Bold" Foreground="{DynamicResource ColorBrush3}" Text="{StaticResource Topic}"/>
    </Paragraph>
<List>
<!-- intro -->
%(intro)s
<!-- end_intro -->

</List><Paragraph Style="{StaticResource H3}">合成 &amp; 生成</Paragraph><List><!-- intro_2 -->
%(intro_2)s
<!-- end_intro_2 -->
</List>
<Paragraph Style="{StaticResource H3}">特性 &amp; 用途</Paragraph><List>
%(body)s
</List>


%(alt)s
</FlowDocument>
</FlowDocumentScrollViewer>
<Grid VerticalAlignment="Center" Margin="6,10,0,0" HorizontalAlignment="Right">
<Grid.ColumnDefinitions >
<ColumnDefinition Width="45"/>
<ColumnDefinition />
</Grid.ColumnDefinitions>
<Path Grid.Column="0" Margin="8,0" Height="28" Fill="{DynamicResource ColorBrush4}"
                    Stretch="Uniform"
                    Data="M4 2H2v12h2V4h10V2zm2 4h12v2H8v10H6zm4 4h12v12H10zm10 10v-8h-8v8z"/>
<TextBlock HorizontalAlignment="Right" Grid.Column="1" Text="仿生猫梦见苦力怕" FontSize="14" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}"/>
</Grid>
<TextBlock Margin="0,2" Grid.Column="1" HorizontalAlignment="Right" Text="%(datetime)s" FontSize="12" Foreground="{DynamicResource ColorBrush4}"/>
<local:MyIconTextButton Text="WIKI" ToolTip="在 Minecraft Wiki 上查看该页面" EventType="打开网页"
    EventData="{StaticResource WikiPage}" LogoScale="1.05" Logo="{StaticResource WikiIcon}" HorizontalAlignment="Left"/>
</StackPanel>
</local:MyCard>
    </TabItem>
<TabItem Header="Minecraft官方博文 - 识海漫谈" Style="{StaticResource TabItemStyle}">
<local:MyCard>
<StackPanel Style="{StaticResource ContentStack}">
<Border Style="{StaticResource HeadImageBorder}">
<Border.Background>
<ImageBrush ImageSource="https://www.helloimg.com/i/2025/01/23/67920e6cec001.png" Stretch="UniformToFill" />
</Border.Background>
<Image Source="https://www.helloimg.com/i/2025/01/23/67920e6cec001.png" Opacity="0" Stretch="Fill"/>
</Border>
<Border Style="{StaticResource TitleBorder}">
<TextBlock Style="{StaticResource TitleBlock}" Text="望远镜" />
</Border><FlowDocumentScrollViewer>
<FlowDocument>
<Paragraph Style="{StaticResource H7}">Taking Inventory: Spyglass</Paragraph>
<Paragraph Style="{StaticResource H2}">背包盘点：望远镜</Paragraph>
<Paragraph Style="{StaticResource H7}">What's on the horizon?</Paragraph>
<Paragraph Style="{StaticResource H5}">地平线上的是什么？</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Some things in Minecraft, like seeds, are very small. Other things just look small because they’re far away. Until recently it was literally impossible to tell the difference.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">Minecraft 中有一些物品本身就十分细小，比如种子；还有一些物体只是因为距离较远才看起来小。在不久前，你是无法确切看出这类物体的具体分别的。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Luckily, in the first part of the Caves and Cliffs update, we added an item that can help. It’s the spyglass, and it’s our item of the week.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">好在，《洞穴与山崖》第一部分的更新带来了一样新鲜玩意，大大改变了这种情况。它就是望远镜，我们的本周物品。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Spyglasses make far-away things larger so you can see them more clearly. You can zoom in on anything, allowing you to see if that green blob on the horizon is a birch tree or a rapidly-approaching creeper. Useful!</Paragraph>
<Paragraph Margin="0,0" Foreground="black">望远镜可以让远在天边的物体看起来更大更清晰。你可以透过它看向任何物体，这样就可以看清地平线上的一个绿色小点是何方神圣了——也许不过是一棵白桦，也许会是一只拔腿向你跑来的苦力怕。非常有用！</Paragraph>
<BlockUIContainer>
<StackPanel Margin="0,4,0,4">
<Image Style="{StaticResource InnerImage}" Source="https://www.helloimg.com/i/2025/01/23/67920e6c4cbbe.png"/>
</StackPanel>
</BlockUIContainer>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">You’re probably wondering how to get one. Well, you’re going to need to make it. Get yourself some copper ingots, by smelting raw copper, and then vertically combine two of them in a crafting bench with a shard of amethyst to act as a lens. If you get the recipe right, a spyglass will be yours.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">你可能会好奇这宝贝该上哪找呢？嗨，自己动手丰衣足食嘛。首先你需要烧炼粗铜来获得一些铜锭，然后在工作台中把它们垂直摆放，最后添上一块紫水晶碎片作镜片。配方弄对了，你的专属望远镜就诞生啦。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Interestingly, the spyglass actually has a slightly different effect depending on what field-of-view (FOV) your game is set to on the options screen. By default, Java edition has a FOV of 70° and Bedrock edition has a slightly-more-zoomed-in FOV of 60°, but that can be changed to whatever you want. Whatever it’s set to, a spyglass will give you a tenth of it, creating a zoom effect.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">有趣的是，望远镜的实际效果依选项屏幕中设定的游戏视场角（FOV）会有所不同。默认情况下，Java 版的视场角为 70°；基岩版则窄一些，为 60°，这个数值可自行更改。但无论如何，望远镜总是会提供十分之一视场角的缩放效果。</Paragraph>
<BlockUIContainer>
<StackPanel Margin="0,4,0,4">
<Image Style="{StaticResource InnerImage}" Source="https://www.helloimg.com/i/2025/01/23/67920e6cca513.png"/>
</StackPanel>
</BlockUIContainer>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">In the real world, no-one’s exactly sure who invented the spyglass.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">现实世界中的望远镜是谁发明的？答案无人知晓。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver"> The earliest written record we have is from a patent application filed by spectacle-maker Hans Lippershey in the Netherlands in 1608, which wasn’t granted because another inventor filed a similar patent a few weeks later, and so the judge figured that everyone knew about it already.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">现存最早的文字记载是荷兰眼镜商 Hans Lippershey 于 1608 年提交的专利申请，但由于几星期后有发明者也提交了相似的专利申请<Run Text="[1]" FontSize="10" BaselineAlignment="Superscript"/>，Hans Lippershey 因此没有获得专利权。最后法官决定消除事端一视同仁，裁定望远镜的制作方法已经人尽皆知了。<Run Text="[2]" FontSize="10" BaselineAlignment="Superscript"/></Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Nonetheless, word of Lippershey’s patent application spread across Europe and reached astronomer Galileo Galilei, who refined the design substantially in the next few years – taking it from 3x magnification to 8x, and then an impressive 23x. With this 23x telescope, he discovered the moons of Jupiter, the phases of Venus, and the rotation of the Sun.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">尽管如此，Lippershey 的专利申请还是传遍了欧洲，也传到了天文学家伽利略的耳朵里。他在几年间大幅改进了望远镜的设计，从 3 倍变焦增加到 8 倍变焦，而后又增加到惊人的 23 倍。靠着这架望远镜，他发现了木星的卫星、金星的相位以及太阳的自转。</Paragraph>
<BlockUIContainer>
<StackPanel Margin="0,4,0,4">
<Image Style="{StaticResource InnerImage}" Source="https://www.helloimg.com/i/2025/01/23/67921077812df.png"/>
</StackPanel>
</BlockUIContainer>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Why did we name it “spyglass”? Because Minecraft dev Felix Jones wanted to be a pirate!</Paragraph>
<Paragraph Margin="0,0" Foreground="black">为什么我们要叫它&quot;spyglass&quot;<Run Text="[3]" FontSize="10" BaselineAlignment="Superscript"/>？因为 Minecraft 开发者 Felix Jones 就想着当个海盗！</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Above: an example of how stained glass caused rendering issues when looking through the spyglass. Poor sheep!</Paragraph>
<Paragraph Margin="0,0" Foreground="black">上图：透过望远镜看向染色玻璃时引发渲染漏洞的例子。好惨一只羊！</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">Today, our telescopes are much more powerful. So powerful, in fact, that we need to blast them into space because our dusty atmosphere limits what we can see. </Paragraph>
<Paragraph Margin="0,0" Foreground="black">如今的望远镜则更强大了。强到什么程度呢？我们要把它发射进太空来执行观测了，因为我们星球的大气满是尘埃，限制了能获取到的信息。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">On 25 December 2021, the most advanced space telescope ever built was launched aboard a rocket from French Guiana.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">2021 年 12 月 25 日，有史以来最先进的望远镜在法属圭亚那搭乘火箭升空。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">The <Underline><local:MyTextButton EventData="https://www.jwst.nasa.gov/" EventType="打开网页" FontSize="10" Foreground="silver" Text="James Webb Space Telescope"/></Underline>, as it’s known, will send back images of stars up to 13.3 billion light-years from Earth – right on the edge of the visible Universe.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">据了解，<Underline><local:MyTextButton EventData="https://www.jwst.nasa.gov/" EventType="打开网页" Text="詹姆斯·韦布太空望远镜"/></Underline>（James Webb Space Telescope）将传回距离地球最远可达 133 亿光年的恒星图像——这已经是我们能看到的最深的宇宙了。</Paragraph>
<Paragraph Margin="0,0" FontSize="12" Foreground="silver">No one’s ever explored what’s beyond the atmosphere of the Overworld in Minecraft. So point your spyglass upward when night falls, and let us know what you see.</Paragraph>
<Paragraph Margin="0,0" Foreground="black">还没人探索过 Minecraft 主世界的大气层外有些什么。那么，试着在夜幕降临时把望远镜对准那片星辰大海吧，也请告诉我们你的发现。</Paragraph>
<Paragraph Style="{StaticResource H5}" Foreground="silver">译注：</Paragraph>
<Paragraph Margin="0,0" Foreground="silver">[1]：这里应该是指荷兰人 Jacob Metius（1571 后 - 1628）。</Paragraph>
<Paragraph Margin="0,0" Foreground="silver">[2]：当时主张专利权的可能有多个科学家或制造商，最后并没有个人或组织获得望远镜的专利权。</Paragraph>
<Paragraph Margin="0,0" Foreground="silver">[3]：&quot;spyglass&quot;一般指海盗用的单筒望远镜。</Paragraph>
<Paragraph Margin="0,0" Foreground="silver">[4]：此处使用了“光行程”作为空间距离衡量方式，但由于宇宙的时空弯曲，这种衡量方式并不准确，其<Underline><local:MyTextButton EventData="https://zh.m.wikipedia.org/wiki%2F%25E5%2590%258C%25E7%25A7%25BB%25E8%25B7%259D%25E9%259B%25A2" EventType="打开网页" FontSize="10" Foreground="silver" Text="同移距离"/></Underline>应为约32 × 10^9光年。</Paragraph>
<Paragraph Style="{StaticResource H5}" Foreground="Red">！提请注意：本文涉及天文学专业知识。鉴于本文原作者及译者均非天文学专业人士，因此无法为文章内容的准确性作任何担保，敬请广大读者在阅读时自行辨别文中信息的准确性，望有识之士不吝指正为感。</Paragraph>
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
<Path Grid.Column="0" Margin="0,0" Height="28" Fill="{DynamicResource ColorBrush4}"
                    Stretch="Uniform"
                    Data="M640 416h256c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H480c-35.36 0-64-28.48-64-64V640h128c53.312 0 96-42.976 96-96V416zM64 128c0-35.36 28.48-64 64-64h416c35.36 0 64 28.48 64 64v416c0 35.36-28.48 64-64 64H128c-35.36 0-64-28.48-64-64V128z m128 276.256h46.72v-24.768h67.392V497.76h49.504V379.488h68.768v20.64h50.88V243.36H355.616v-34.368c0-10.08 1.376-18.784 4.16-26.112a10.56 10.56 0 0 0 1.344-4.16c0-0.896-3.2-1.792-9.6-2.72h-46.816v67.36H192v160.896z m46.72-122.368h67.392v60.48h-67.36V281.92z m185.664 60.48h-68.768V281.92h68.768v60.48z m203.84 488l19.264-53.632h100.384l19.264 53.632h54.976L732.736 576h-64.64L576 830.4h52.256z m33.024-96.256l37.12-108.608h1.376l34.368 108.608h-72.864zM896 320h-64a128 128 0 0 0-128-128v-64a192 192 0 0 1 192 192zM128 704h64a128 128 0 0 0 128 128v64a192 192 0 0 1-192-192z"/>
<TextBlock Grid.Column="1" Text="(MCBBS)橄榄Chan" FontSize="14" HorizontalAlignment="Right" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}"/>
<Path Grid.Column="2" Margin="8,0" Height="28" Fill="{DynamicResource ColorBrush4}"
                    Stretch="Uniform" HorizontalAlignment="Right"
                    Data="M14 21v-3.075l5.525-5.5q.225-.225.5-.325t.55-.1q.3 0 .575.113t.5.337l.925.925q.2.225.313.5t.112.55t-.1.563t-.325.512l-5.5 5.5zM4 20v-2.8q0-.85.438-1.562T5.6 14.55q1.55-.775 3.15-1.162T12 13q.925 0 1.825.113t1.8.362L12 17.1V20zm16.575-4.6l.925-.975l-.925-.925l-.95.95zM12 12q-1.65 0-2.825-1.175T8 8t1.175-2.825T12 4t2.825 1.175T16 8t-1.175 2.825T12 12"/>
<TextBlock HorizontalAlignment="Right" Grid.Column="3" Text="Duncan Geere" FontSize="14" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}"/>
<TextBlock Margin="0,2" Grid.Row="1" Grid.Column="1" Grid.ColumnSpan="2" HorizontalAlignment="Left" Text="最后更新: 2024-11-23" FontSize="12" Foreground="{DynamicResource ColorBrush4}"/>
<TextBlock Margin="0,2" Grid.Row="1" Grid.Column="3" Grid.ColumnSpan="2" HorizontalAlignment="Left" Text="源日期: 2022-2-17" FontSize="12" Foreground="{DynamicResource ColorBrush4}"/>
</Grid>
<local:MyIconTextButton Text="访问原址" ToolTip="在 Minecraft 官网上查看该页面原文" EventType="打开网页" Margin="8"
    EventData="https://www.minecraft.net/zh-hans/article/taking-inventory--spyglass" LogoScale="1.05" Logo="{StaticResource CreeperIcon}" HorizontalAlignment="Left"/>
</StackPanel>

<StackPanel Margin="16,0,23,20" VerticalAlignment="bottom">
    <Grid>
      <Grid.ColumnDefinitions>
        <ColumnDefinition Width="1*"/>
        <ColumnDefinition Width="120"/>
      </Grid.ColumnDefinitions>
      <local:MyComboBox x:Name="jumpbox" Height="30" SelectedIndex="0">
        <local:MyComboBoxItem Content="古迹废墟"/>
        <local:MyComboBoxItem Content="废弃矿井"/>
      </local:MyComboBox>
        <local:MyButton HorizontalAlignment="Center" Width="92"
            Grid.Column="1" Text="打开→" EventType="打开帮助"
            EventData="{Binding Path=Text,ElementName=jumpbox,StringFormat=http://pclhomeplazaoss.lingyunawa.top:26995/d/Homepages/Ext1nguisher/h{0}.json}"/>
    </Grid>
</StackPanel>
</StackPanel>
</local:MyCard>
</TabItem>
<TabItem Header="其他" Style="{StaticResource TabItemStyle}">
<StackPanel>
<local:MyCard CanSwap="False" IsSwaped="false" Margin="0,0,0,10">
<Border Margin="0,0,0,0" Padding="2,8" BorderThickness="1" Background="{DynamicResource ColorBrush5}" CornerRadius="5" VerticalAlignment="Top" BorderBrush="{DynamicResource ColorBrush3}" Opacity="0.7">
    <Grid Margin="10,0,0,0">
        <TextBlock FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#FF000000">
                ⚠️ &quot;最新版本&quot; 板块为每周更新时同步，并不一定为最新！
    </TextBlock>
        <TextBlock FontWeight="Bold" FontSize="12" VerticalAlignment="Center" Foreground="#00000000">
                ⚠️ &quot;最新版本&quot; 板块为每周更新时同步，并不一定为最新！
    </TextBlock>
    </Grid>
</Border>
</local:MyCard>
<!-- NewsCard -->
%(NewsCard)s
<!-- end_NewsCard -->
</StackPanel>
</TabItem>
</TabControl>
<local:MyCard Margin="0,10,0,14">
<Border BorderBrush="{DynamicResource ColorBrush2}" Margin="-0.6" CornerRadius="5" BorderThickness="0,0,0,10">
<StackPanel>
  <Grid Margin="26,20,20,2">
    <StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="0,0,0,4">
    <TextBlock FontSize="18" Foreground="{DynamicResource ColorBrush2}"><Bold>PCL2 杂志主页</Bold></TextBlock>
    <local:MyIconTextButton ColorType="Highlight" Margin="4,0" Text="{StaticResource VersionID}" ToolTip="当前版本号(非git), 点击复制" EventType="复制文本" EventData="{StaticResource VersionID}"
    LogoScale="1.1" Logo="M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z" />
    </StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="0,0,0,10">
    <TextBlock HorizontalAlignment="Left" Grid.Column="0" FontSize="13" VerticalAlignment="Center" Foreground="{DynamicResource ColorBrush4}">
        <Run>主页制作: 仿生猫梦见苦力怕 / CreeperIsASpy</Run>
        <LineBreak/>
        <Run>更新时间: 周一下午到周二下午（本人初中生学业紧张理解一下）</Run>
        <LineBreak/>
        <Run>内容取自</Run><Underline><local:MyTextButton EventType="打开网页" EventData="https://zh.minecraft.wiki">中文 Minecraft Wiki</local:MyTextButton></Underline>
        <Run>中“本周页面”板块以及 </Run><Underline><local:MyTextButton EventType="打开网页" EventData="https://minecraft.net">MC 官网</local:MyTextButton></Underline>。
    </TextBlock>
    </StackPanel>
    <StackPanel Orientation="Horizontal" VerticalAlignment="Center" Margin="-8,0,0,10">
    <local:MyIconTextButton HorizontalAlignment="Left" Text="Gitee" ToolTip="前往杂志主页 Gitee 页面" EventType="打开网页"
    EventData="https://gitee.com/planet_of_daniel/pcl2-homepage-fhg"
    LogoScale="1" Logo="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12a12 12 0 0 0 12-12A12 12 0 0 0 12 0zm6.09 5.333c.328 0 .593.266.592.593v1.482a.594.594 0 0 1-.593.592H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h5.63c.982 0 1.778-.796 1.778-1.778v-.296a.593.593 0 0 0-.592-.593h-4.15a.59.59 0 0 1-.592-.592v-1.482a.593.593 0 0 1 .593-.592h6.815c.327 0 .593.265.593.592v3.408a4 4 0 0 1-4 4H5.926a.593.593 0 0 1-.593-.593V9.778a4.444 4.444 0 0 1 4.445-4.444h8.296Z"/>
    <local:MyIconTextButton Text="CC BY-NC-SA 4.0" ToolTip="无特殊声明本主页文字内容使用该授权协议" EventType="打开网页"
    EventData="https://creativecommons.org/licenses/by-nc-sa/4.0/"
    LogoScale="1" Logo="M8.75.75V2h.985c.304 0 .603.08.867.231l1.29.736c.038.022.08.033.124.033h2.234a.75.75 0 0 1 0 1.5h-.427l2.111 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.006.005-.01.01-.045.04c-.21.176-.441.327-.686.45C14.556 10.78 13.88 11 13 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L12.178 4.5h-.162c-.305 0-.604-.079-.868-.231l-1.29-.736a.245.245 0 0 0-.124-.033H8.75V13h2.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.5V3.5h-.984a.245.245 0 0 0-.124.033l-1.289.737c-.265.15-.564.23-.869.23h-.162l2.112 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.016.015-.045.04c-.21.176-.441.327-.686.45C4.556 10.78 3.88 11 3 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L2.178 4.5H1.75a.75.75 0 0 1 0-1.5h2.234a.249.249 0 0 0 .125-.033l1.288-.737c.265-.15.564-.23.869-.23h.984V.75a.75.75 0 0 1 1.5 0Zm2.945 8.477c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L13 6.327Zm-10 0c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L3 6.327Z" />
    </StackPanel>
    </StackPanel>
    <StackPanel HorizontalAlignment="Right" >
    <local:MyIconTextButton HorizontalAlignment="Left" Text="反馈" ToolTip="反馈主页问题" EventType="打开网页"
    EventData="https://gitee.com/planet_of_daniel/pcl2-homepage-fhg/issues/new"
    LogoScale="1" Logo="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0z M1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0z"/>
    <local:MyIconTextButton HorizontalAlignment="Left" Text="刷新" ToolTip="刷新主页" EventType="刷新主页"
    LogoScale="0.9" Logo="M960 416V192l-73.056 73.056a447.712 447.712 0 0 0-373.6-201.088C265.92 63.968 65.312 264.544 65.312 512S265.92 960.032 513.344 960.032a448.064 448.064 0 0 0 415.232-279.488 38.368 38.368 0 1 0-71.136-28.896 371.36 371.36 0 0 1-344.096 231.584C308.32 883.232 142.112 717.024 142.112 512S308.32 140.768 513.344 140.768c132.448 0 251.936 70.08 318.016 179.84L736 416h224z"/>
    <local:MyIconTextButton HorizontalAlignment="Left" Text="鸣谢" ToolTip="鸣谢人员名单及其联系方式" EventType="弹出窗口" EventData="{StaticResource thanks}"
    LogoScale="0.9" Logo="M6.26 21.388H6c-.943 0-1.414 0-1.707-.293C4 20.804 4 20.332 4 19.389v-1.112c0-.518 0-.777.133-1.009s.334-.348.736-.582c2.646-1.539 6.403-2.405 8.91-.91q.253.151.45.368a1.49 1.49 0 0 1-.126 2.134a1 1 0 0 1-.427.24q.18-.021.345-.047c.911-.145 1.676-.633 2.376-1.162l1.808-1.365a1.89 1.89 0 0 1 2.22 0c.573.433.749 1.146.386 1.728c-.423.678-1.019 1.545-1.591 2.075s-1.426 1.004-2.122 1.34c-.772.373-1.624.587-2.491.728c-1.758.284-3.59.24-5.33-.118a15 15 0 0 0-3.017-.308m4.601-18.026C11.368 2.454 11.621 2 12 2s.632.454 1.139 1.363l.13.235c.145.259.217.388.329.473s.252.117.532.18l.254.058c.984.222 1.476.334 1.593.71s-.218.769-.889 1.553l-.174.203c-.19.223-.285.334-.328.472s-.029.287 0 .584l.026.27c.102 1.047.152 1.57-.154 1.803s-.767.02-1.688-.404l-.239-.11c-.261-.12-.392-.18-.531-.18s-.27.06-.531.18l-.239.11c-.92.425-1.382.637-1.688.404s-.256-.756-.154-1.802l.026-.271c.029-.297.043-.446 0-.584s-.138-.25-.328-.472l-.174-.203c-.67-.784-1.006-1.177-.889-1.553s.609-.488 1.593-.71l.254-.058c.28-.063.42-.095.532-.18s.184-.214.328-.473zm8.569 4.319c.254-.455.38-.682.57-.682s.316.227.57.682l.065.117c.072.13.108.194.164.237s.126.058.266.09l.127.028c.492.112.738.167.796.356s-.109.384-.444.776l-.087.101c-.095.112-.143.168-.164.237s-.014.143 0 .292l.013.135c.05.523.076.785-.077.901s-.383.01-.844-.202l-.12-.055c-.13-.06-.196-.09-.265-.09c-.07 0-.135.03-.266.09l-.119.055c-.46.212-.69.318-.844.202c-.153-.116-.128-.378-.077-.901l.013-.135c.014-.15.022-.224 0-.292c-.021-.07-.069-.125-.164-.237l-.087-.101c-.335-.392-.503-.588-.444-.776s.304-.244.796-.356l.127-.028c.14-.032.21-.048.266-.09c.056-.043.092-.108.164-.237zm-16 0C3.685 7.227 3.81 7 4 7s.316.227.57.682l.065.117c.072.13.108.194.164.237s.126.058.266.09l.127.028c.492.112.738.167.797.356c.058.188-.11.384-.445.776l-.087.101c-.095.112-.143.168-.164.237s-.014.143 0 .292l.013.135c.05.523.076.785-.077.901s-.384.01-.844-.202l-.12-.055c-.13-.06-.196-.09-.265-.09c-.07 0-.135.03-.266.09l-.119.055c-.46.212-.69.318-.844.202c-.153-.116-.128-.378-.077-.901l.013-.135c.014-.15.022-.224 0-.292c-.021-.07-.069-.125-.164-.237l-.087-.101c-.335-.392-.503-.588-.445-.776c.059-.189.305-.244.797-.356l.127-.028c.14-.032.21-.048.266-.09c.056-.043.092-.108.164-.237z"/>
    </StackPanel>
  </Grid>
</StackPanel>
</Border>
</local:MyCard>
</StackPanel>'''
    validate_template(content_text)
    content_text = re.sub(r"(?<!%)%(?!\()", "%%", content_text)
    test = "{%(datetime)s} \n %(WikiPage)s \n %(topic)s \n %(intro)s \n %(intro_2)s \n %(body)s \n %(alt)s \n %(img)s \n %(NewsCard)s \n %(version)s"
    meta = {
        'WikiPage': get_wiki_page(),
        'version': get_version(),
        'img': gs(),
        'topic': get_topic(),
        'intro': gr()[0],
        'intro_2': gr()[1],
        'body': '\n'.join(gr()[2:-1]),
        'alt': get_img_alt(),
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


update()
