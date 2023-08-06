# coding: utf8
from __future__ import absolute_import
import os, sys, re


line_char = u'\uffff'
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring


NAMED_WHITE_FONT_COLOR = "#ffffff"
NAMED_BLACK_FONT_COLOR = "#333333"
NAMED_COLORS_AND_BACKGROUND  =  {
    "darkgreen": NAMED_WHITE_FONT_COLOR,
    "lightcoral": NAMED_WHITE_FONT_COLOR,
    "darkslategray": NAMED_WHITE_FONT_COLOR,
    "chocolate": NAMED_WHITE_FONT_COLOR,
    "palevioletred": NAMED_WHITE_FONT_COLOR,
    "black": NAMED_WHITE_FONT_COLOR,
    "mediumpurple": NAMED_WHITE_FONT_COLOR,
    "magenta": NAMED_WHITE_FONT_COLOR,
    "mediumslateblue": NAMED_WHITE_FONT_COLOR,
    "lightpink": NAMED_WHITE_FONT_COLOR,
    "springgreen": NAMED_WHITE_FONT_COLOR,
    "orchid": NAMED_WHITE_FONT_COLOR,
    "lawngreen": NAMED_WHITE_FONT_COLOR,
    "firebrick": NAMED_WHITE_FONT_COLOR,
    "darkviolet": NAMED_WHITE_FONT_COLOR,
    "lightskyblue": NAMED_WHITE_FONT_COLOR,
    "greenyellow": NAMED_WHITE_FONT_COLOR,
    "midnightblue": NAMED_WHITE_FONT_COLOR,
    "darkmagenta": NAMED_WHITE_FONT_COLOR,
    "darkslateblue": NAMED_WHITE_FONT_COLOR,
    "sandybrown": NAMED_WHITE_FONT_COLOR,
    "plum": NAMED_WHITE_FONT_COLOR,
    "mediumorchid": NAMED_WHITE_FONT_COLOR,
    "lightgreen": NAMED_WHITE_FONT_COLOR,
    "goldenrod": NAMED_WHITE_FONT_COLOR,
    "salmon": NAMED_WHITE_FONT_COLOR,
    "darkseagreen": NAMED_WHITE_FONT_COLOR,
    "blueviolet": NAMED_WHITE_FONT_COLOR,
    "mediumvioletred": NAMED_WHITE_FONT_COLOR,
    "thistle": NAMED_WHITE_FONT_COLOR,
    "darkblue": NAMED_WHITE_FONT_COLOR,
    "sienna": NAMED_WHITE_FONT_COLOR,
    "mediumspringgreen": NAMED_WHITE_FONT_COLOR,
    "darkgray": NAMED_WHITE_FONT_COLOR,
    "violet": NAMED_WHITE_FONT_COLOR,
    "cadetblue": NAMED_WHITE_FONT_COLOR,
    "mediumturquoise": NAMED_WHITE_FONT_COLOR,
    "orangered": NAMED_WHITE_FONT_COLOR,
    "mediumaquamarine": NAMED_WHITE_FONT_COLOR,
    "lightslategray": NAMED_WHITE_FONT_COLOR,
    "navy": NAMED_WHITE_FONT_COLOR,
    "gray": NAMED_WHITE_FONT_COLOR,
    "powderblue": NAMED_WHITE_FONT_COLOR,
    "per": NAMED_WHITE_FONT_COLOR,
    "indigo": NAMED_WHITE_FONT_COLOR,
    "steelblue": NAMED_WHITE_FONT_COLOR,
    "blue": NAMED_WHITE_FONT_COLOR,
    "lightsalmon": NAMED_WHITE_FONT_COLOR,
    "hotpink": NAMED_WHITE_FONT_COLOR,
    "darkturquoise": NAMED_WHITE_FONT_COLOR,
    "skyblue": NAMED_WHITE_FONT_COLOR,
    "coral": NAMED_WHITE_FONT_COLOR,
    "lightseagreen": NAMED_WHITE_FONT_COLOR,
    "green": NAMED_WHITE_FONT_COLOR,
    "slateblue": NAMED_WHITE_FONT_COLOR,
    "saddlebrown": NAMED_WHITE_FONT_COLOR,
    "teal": NAMED_WHITE_FONT_COLOR,
    "limegreen": NAMED_WHITE_FONT_COLOR,
    "dodgerblue": NAMED_WHITE_FONT_COLOR,
    "lime": NAMED_WHITE_FONT_COLOR,
    "darkkhaki": NAMED_WHITE_FONT_COLOR,
    "indianred": NAMED_WHITE_FONT_COLOR,
    "darkcyan": NAMED_WHITE_FONT_COLOR,
    "deeppink": NAMED_WHITE_FONT_COLOR,
    "darkorange": NAMED_WHITE_FONT_COLOR,
    "lightsteelblue": NAMED_WHITE_FONT_COLOR,
    "maroon": NAMED_WHITE_FONT_COLOR,
    "slategray": NAMED_WHITE_FONT_COLOR,
    "tan": NAMED_WHITE_FONT_COLOR,
    "chartreuse": NAMED_WHITE_FONT_COLOR,
    "fuchsia": NAMED_WHITE_FONT_COLOR,
    "gold": NAMED_WHITE_FONT_COLOR,
    "tomato": NAMED_WHITE_FONT_COLOR,
    "red": NAMED_WHITE_FONT_COLOR,
    "royalblue": NAMED_WHITE_FONT_COLOR,
    "lightblue": NAMED_WHITE_FONT_COLOR,
    "dimgray": NAMED_WHITE_FONT_COLOR,
    "deepskyblue": NAMED_WHITE_FONT_COLOR,
    "mediumseagreen": NAMED_WHITE_FONT_COLOR,
    "forestgreen": NAMED_WHITE_FONT_COLOR,
    "yellowgreen": NAMED_WHITE_FONT_COLOR,
    "cyan": NAMED_WHITE_FONT_COLOR,
    "darkred": NAMED_WHITE_FONT_COLOR,
    "olivedrab": NAMED_WHITE_FONT_COLOR,
    "rosybrown": NAMED_WHITE_FONT_COLOR,
    "darkorchid": NAMED_WHITE_FONT_COLOR,
    "burlywood": NAMED_WHITE_FONT_COLOR,
    "darkgoldenrod": NAMED_WHITE_FONT_COLOR,
    "cornflowerblue": NAMED_WHITE_FONT_COLOR,
    "palegreen": NAMED_WHITE_FONT_COLOR,
    "pink": NAMED_WHITE_FONT_COLOR,
    "brown": NAMED_WHITE_FONT_COLOR,
    "seagreen": NAMED_WHITE_FONT_COLOR,
    "orange": NAMED_WHITE_FONT_COLOR,
    "mediumblue": NAMED_WHITE_FONT_COLOR,
    "darkolivegreen": NAMED_WHITE_FONT_COLOR,
    "purple": NAMED_WHITE_FONT_COLOR,
    "darksalmon": NAMED_WHITE_FONT_COLOR,
    "crimson": NAMED_WHITE_FONT_COLOR,
    "olive": NAMED_WHITE_FONT_COLOR,
    "wheat": NAMED_WHITE_FONT_COLOR,
    "turquoise": NAMED_WHITE_FONT_COLOR,
    "silver": NAMED_WHITE_FONT_COLOR,
    "yellow": NAMED_BLACK_FONT_COLOR,
    "white": NAMED_BLACK_FONT_COLOR,
    "ivory" : NAMED_BLACK_FONT_COLOR,
    "blanchedalmond" : NAMED_BLACK_FONT_COLOR,
    "beige" : NAMED_BLACK_FONT_COLOR,
    "aquamarine" : NAMED_BLACK_FONT_COLOR,
    "whitesmoke" : NAMED_BLACK_FONT_COLOR,
    "bisque" : NAMED_BLACK_FONT_COLOR,
    "linen" : NAMED_BLACK_FONT_COLOR,
    "aqua" : NAMED_BLACK_FONT_COLOR,
    "peachpuff" : NAMED_BLACK_FONT_COLOR,
    "moccasin" : NAMED_BLACK_FONT_COLOR,
    "paleturquoise" : NAMED_BLACK_FONT_COLOR,
    "mintcream" : NAMED_BLACK_FONT_COLOR,
    "lightgoldenrodyellow" : NAMED_BLACK_FONT_COLOR,
    "lightcyan" : NAMED_BLACK_FONT_COLOR,
    "mistyrose" : NAMED_BLACK_FONT_COLOR,
    "lemonchiffon" : NAMED_BLACK_FONT_COLOR,
    "gainsboro" : NAMED_BLACK_FONT_COLOR,
    "lavender" : NAMED_BLACK_FONT_COLOR,
    "oldlace" : NAMED_BLACK_FONT_COLOR,
    "palegoldenrod" : NAMED_BLACK_FONT_COLOR,
    "papayawhip" : NAMED_BLACK_FONT_COLOR,
    "ghostwhite" : NAMED_BLACK_FONT_COLOR,
    "navajowhite" : NAMED_BLACK_FONT_COLOR,
    "antiquewhite" : NAMED_BLACK_FONT_COLOR,
    "lightgray" : NAMED_BLACK_FONT_COLOR,
    "lightyellow" : NAMED_BLACK_FONT_COLOR,
    "azure" : NAMED_BLACK_FONT_COLOR,
    "cornsilk" : NAMED_BLACK_FONT_COLOR,
    "honeydew" : NAMED_BLACK_FONT_COLOR,
    "floralwhite" : NAMED_BLACK_FONT_COLOR,
    "khaki" : NAMED_BLACK_FONT_COLOR,
    "lavenderblush" : NAMED_BLACK_FONT_COLOR,
    "seashell" : NAMED_BLACK_FONT_COLOR,
    "snow" : NAMED_BLACK_FONT_COLOR,
    "aliceblue" : NAMED_BLACK_FONT_COLOR,
}


NAMED_COLOR_HEX_MAP = {
        "aliceblue": "#f0f8ff",
       "antiquewhite": "#faebd7",
       "aqua": "#00ffff",
       "aquamarine": "#7fffd4",
       "azure": "#f0ffff",
       "beige": "#f5f5dc",
       "bisque": "#ffe4c4",
       "black": "#000000",
       "blanchedalmond": "#ffebcd",
       "blue": "#0000ff",
       "blueviolet": "#8a2be2",
       "brown": "#a52a2a",
       "burlywood": "#deb887",
       "cadetblue": "#5f9ea0",
       "chartreuse": "#7fff00",
       "chocolate": "#d2691e",
       "coral": "#ff7f50",
       "cornflowerblue": "#6495ed",
       "cornsilk": "#fff8dc",
       "crimson": "#dc143c",
       "cyan": "#00ffff",
       "darkblue": "#00008b",
       "darkcyan": "#008b8b",
       "darkgoldenrod": "#b8860b",
       "darkgray": "#a9a9a9",
       "darkgrey": "#a9a9a9",
       "darkgreen": "#006400",
       "darkkhaki": "#bdb76b",
       "darkmagenta": "#8b008b",
       "darkolivegreen": "#556b2f",
       "darkorange": "#ff8c00",
       "darkorchid": "#9932cc",
       "darkred": "#8b0000",
       "darksalmon": "#e9967a",
       "darkseagreen": "#8fbc8f",
       "darkslateblue": "#483d8b",
       "darkslategray": "#2f4f4f",
       "darkslategrey": "#2f4f4f",
       "darkturquoise": "#00ced1",
       "darkviolet": "#9400d3",
       "deeppink": "#ff1493",
       "deepskyblue": "#00bfff",
       "dimgray": "#696969",
       "dimgrey": "#696969",
       "dodgerblue": "#1e90ff",
       "firebrick": "#b22222",
       "floralwhite": "#fffaf0",
       "forestgreen": "#228b22",
       "fuchsia": "#ff00ff",
       "gainsboro": "#dcdcdc",
       "ghostwhite": "#f8f8ff",
       "gold": "#ffd700",
       "goldenrod": "#daa520",
       "gray": "#808080",
       "grey": "#808080",
       "green": "#008000",
       "greenyellow": "#adff2f",
       "honeydew": "#f0fff0",
       "hotpink": "#ff69b4",
       "indianred": "#cd5c5c",
       "indigo": "#4b0082",
       "ivory": "#fffff0",
       "khaki": "#f0e68c",
       "lavender": "#e6e6fa",
       "lavenderblush": "#fff0f5",
       "lawngreen": "#7cfc00",
       "lemonchiffon": "#fffacd",
       "lightblue": "#add8e6",
       "lightcoral": "#f08080",
       "lightcyan": "#e0ffff",
       "lightgoldenrodyellow": "#fafad2",
       "lightgray": "#d3d3d3",
       "lightgrey": "#d3d3d3",
       "lightgreen": "#90ee90",
       "lightpink": "#ffb6c1",
       "lightsalmon": "#ffa07a",
       "lightseagreen": "#20b2aa",
       "lightskyblue": "#87cefa",
       "lightslategray": "#778899",
       "lightslategrey": "#778899",
       "lightsteelblue": "#b0c4de",
       "lightyellow": "#ffffe0",
       "lime": "#00ff00",
       "limegreen": "#32cd32",
       "linen": "#faf0e6",
       "magenta": "#ff00ff",
       "maroon": "#800000",
       "mediumaquamarine": "#66cdaa",
       "mediumblue": "#0000cd",
       "mediumorchid": "#ba55d3",
       "mediumpurple": "#9370db",
       "mediumseagreen": "#3cb371",
       "mediumslateblue": "#7b68ee",
       "mediumspringgreen": "#00fa9a",
       "mediumturquoise": "#48d1cc",
       "mediumvioletred": "#c71585",
       "midnightblue": "#191970",
       "mintcream": "#f5fffa",
       "mistyrose": "#ffe4e1",
       "moccasin": "#ffe4b5",
       "navajowhite": "#ffdead",
       "navy": "#000080",
       "oldlace": "#fdf5e6",
       "olive": "#808000",
       "olivedrab": "#6b8e23",
       "orange": "#ffa500",
       "orangered": "#ff4500",
       "orchid": "#da70d6",
       "palegoldenrod": "#eee8aa",
       "palegreen": "#98fb98",
       "paleturquoise": "#afeeee",
       "palevioletred": "#db7093",
       "papayawhip": "#ffefd5",
       "peachpuff": "#ffdab9",
       "peru": "#cd853f",
       "pink": "#ffc0cb",
       "plum": "#dda0dd",
       "powderblue": "#b0e0e6",
       "purple": "#800080",
       "red": "#ff0000",
       "rosybrown": "#bc8f8f",
       "royalblue": "#4169e1",
       "saddlebrown": "#8b4513",
       "salmon": "#fa8072",
       "sandybrown": "#f4a460",
       "seagreen": "#2e8b57",
       "seashell": "#fff5ee",
       "sienna": "#a0522d",
       "silver": "#c0c0c0",
       "skyblue": "#87ceeb",
       "slateblue": "#6a5acd",
       "slategray": "#708090",
       "slategrey": "#708090",
       "snow": "#fffafa",
       "springgreen": "#00ff7f",
       "steelblue": "#4682b4",
       "tan": "#d2b48c",
       "teal": "#008080",
       "thistle": "#d8bfd8",
       "tomato": "#ff6347",
       "turquoise": "#40e0d0",
       "violet": "#ee82ee",
       "wheat": "#f5deb3",
       "white": "#ffffff",
       "whitesmoke": "#f5f5f5",
       "yellow": "#ffff00",
       "yellowgreen": "#9acd32"
}


_COLOR_NAMES = ['ivory',
 'darkgreen',
 'lightcoral',
 'darkslategray',
 'blanchedalmond',
 'chocolate',
 'palevioletred',
 'black',
 'mediumpurple',
 'magenta',
 'mediumslateblue',
 'beige',
 'lightpink',
 'springgreen',
 'orchid',
 'lawngreen',
 'firebrick',
 'darkviolet',
 'lightskyblue',
 'aquamarine',
 'greenyellow',
 'whitesmoke',
 'midnightblue',
 'bisque',
 'darkmagenta',
 'darkslateblue',
 'sandybrown',
 'plum',
 'linen',
 'mediumorchid',
 'lightgreen',
 'goldenrod',
 'salmon',
 'aqua',
 'darkseagreen',
 'blueviolet',
 'peachpuff',
 'mediumvioletred',
 'moccasin',
 'thistle',
 'darkblue',
 'sienna',
 'mediumspringgreen',
 'paleturquoise',
 'darkgray',
 'violet',
 'cadetblue',
 'mediumturquoise',
 'orangered',
 'mediumaquamarine',
 'mintcream',
 'lightgoldenrodyellow',
 'lightslategray',
 'navy',
 'lightcyan',
 'mistyrose',
 'gray',
 'powderblue',
 'peru',
 'indigo',
 'steelblue',
 'blue',
 'lightsalmon',
 'lemonchiffon',
 'gainsboro',
 'hotpink',
 'darkturquoise',
 'lavender',
 'skyblue',
 'oldlace',
 'coral',
 'lightseagreen',
 'palegoldenrod',
 'green',
 'slateblue',
 'saddlebrown',
 'teal',
 'papayawhip',
 'limegreen',
 'dodgerblue',
 'lime',
 'white',
 'ghostwhite',
 'navajowhite',
 'darkkhaki',
 'indianred',
 'antiquewhite',
 'darkcyan',
 'deeppink',
 'darkorange',
 'lightsteelblue',
 'lightgray',
 'maroon',
 'slategray',
 'tan',
 'chartreuse',
 'lightyellow',
 'fuchsia',
 'azure',
 'gold',
 'tomato',
 'red',
 'royalblue',
 'cornsilk',
 'honeydew',
 'lightblue',
 'dimgray',
 'deepskyblue',
 'floralwhite',
 'mediumseagreen',
 'forestgreen',
 'yellowgreen',
 'cyan',
 'darkred',
 'khaki',
 'olivedrab',
 'rosybrown',
 'darkorchid',
 'burlywood',
 'darkgoldenrod',
 'lavenderblush',
 'cornflowerblue',
 'seashell',
 'palegreen',
 'pink',
 'brown',
 'yellow',
 'seagreen',
 'orange',
 'mediumblue',
 'darkolivegreen',
 'snow',
 'purple',
 'darksalmon',
 'aliceblue',
 'crimson',
 'olive',
 'wheat',
 'turquoise',
 'silver']

COLOR_NAMES = set(_COLOR_NAMES)


FONT_FAMILY_MAP = {
    u'华文细黑':'STXihei',
    u'华文黑体':'STHeiti',
    u'华文楷体':'STKaiti',
    u'华文宋体':'STSong',
    u'华文仿宋':'STFangsong',
    u'冬青黑体': 'Hiragino Sans GB',
    u'宋刻本秀': 'FZSongKeBenXiuKsiS-R-GB',
    u'儷黑':'LiHei Pro',
    u'丽黑':'LiHei Pro',
    u'儷宋':'LiSong Pro',
    u'丽宋':'LiSong Pro',
    u'標楷體':'BiauKai',
    u'标楷体':'BiauKai',
    u'兰亭黑': 'Lantinghei SC',
    u'隶变': 'Libian SC, Libian TC',
    u'报隶': 'Baoli SC, Baoli TC',
    u'翩翩体': 'HanziPen SC, HanziPen TC',
    u'娃娃体': 'Wawati, Wawati SC, Wawati TC',
    u'蘋果儷中黑':'Apple LiGothic Medium',
    u'苹果丽中黑':'Apple LiGothic Medium',
    u'蘋果儷細宋':'Apple LiSung Light',
    u'苹果丽细宋':'Apple LiSung Light',
    u'新細明體':'PMingLiU',
    u'新細明体':'PMingLiU',
    u'細明體':'MingLiU',
    u'細明体':'MingLiU',
    u'黑体':'SimHei, Heiti SC, Heiti TC',
    u'宋体':'Songti, SimSun, Songti SC, Songti TC',
    u'新宋体':'NSimSun',
    u'仿宋':'FangSong',
    u'楷体':'KaiTi, Kaiti SC, Kaiti TC',
    u'微軟正黑體':'Microsoft JhengHei',
    u'微軟正黑体':'Microsoft JhengHei',
    u'微软雅黑体':'Microsoft YaHei',
    u'隶书':'LiSu, Libian SC, Libian TC',
    u'幼圆':'YouYuan',
    u'华文中宋':'STZhongsong',
    u'方正舒体':'FZShuTi',
    u'方正姚体':'FZYaoti',
    u'华文彩云':'STCaiyun',
    u'华文琥珀':'STHupo',
    u'华文隶书':'STLiti',
    u'华文行楷':'STXingkai',
    u'华文新魏': 'STXinwei',
}


MARKDOWN_EXTS = ['.txt', '.md', '.markdown', '.mk']

def is_a_markdown_file(path):
    if not path:
        return False
    ext = os.path.splitext(path)[1].lower()
    return ext in MARKDOWN_EXTS




def is_color_value(value):
    if value in COLOR_NAMES or (value.startswith('#') and len(value)<=7) \
                or value.startswith('rgb(') or value.startswith('rgba('):
        return True
    else:
        return False


def smart_tag_style_for_block_html(block_html):
    # md_line & header, image 支持
    # [center, red, 17px, 120%]
    plain_text = re.sub(r'<[^<>]*>', '', block_html).replace(line_char, '') # line_char 可能存在的问题
    plain_text = plain_text.strip('\n').lstrip()
    tag_s = re.search(r'\[[^\^\[\]]+\]$', plain_text)
    if not tag_s:
        return block_html # ignore

    raw_tag_marker = tag_s.group()
    if '/' in raw_tag_marker: # / 是不允许出现的字符
        return block_html

    raw_tag = raw_tag_marker.strip('[]').strip().lower().replace(u'，', ',') # 全小写处理

    if ' ' in raw_tag and ',' not in raw_tag:
        # 没有 , 的情况下, 可以用空格进行对应
        raw_tag_list = raw_tag.split(' ')
    else:
        raw_tag_list = raw_tag.split(',')

    style_list = []
    font_family_tried = False
    for tag in raw_tag_list:
        tag = tag.strip()
        font_size_already_set = False
        if tag in ['middle']:
            tag = 'center'
        # style_type = None
        if is_color_value(tag):
            # style_type = 'color'
            style_list.append('color:%s'%tag)
        elif re.match("[+-]\\d", tag): # text-indent
            if re.search("\\d+$", tag): # 自动添加 em
                style_list.append("display:block; text-indent:%sem" % tag)
            else:
                style_list.append("display:block; text-indent:%s" % tag)
        elif tag.startswith('@') and is_color_value(tag[1:]):
            # @xxxx 是作为背景色
            style_list.append('background-color:%s'%tag[1:])
        elif re.match('\d+\.\d+$', tag):
            # 浮点, 认为是 line-height
            style_list.append('line-height:%s'%tag)
        elif re.match('\d+(px|pt|em)?$', tag, re.I): # 整数 font_size
            # style_type = 'font_size'
            if re.match(r'\d+$', tag):
                tag += 'px' # 自动补全 px 如果只是整数的话
            style_list.append('font-size:%s'%tag)
            font_size_already_set = True
        elif tag in ['center', 'left', 'right']:
            # alignment
            style_list.append('display:block; text-align:%s'%tag)
            if tag != 'left':
                # 居中、居右的 text-indent 是没有意义的
                style_list.append('text-indent:0')
        elif tag and not font_family_tried:
            # as font-family, 但是 font family 仅仅尝试一次, 这样可以过滤掉一些无效值
            font_family = FONT_FAMILY_MAP.get(tag) or tag
            style_list.append('font-family:%s'%font_family)
            font_family_tried = True
        elif tag:
            # 只有有一个规则是不匹配的, 就直接return block_html
            return block_html

        if tag.endswith('%') and not font_size_already_set:
            # zoom 的逻辑容易产生 offset 前端的错误
            style_list.append('font-size:%s' % tag)
            #style_list.append('zoom:%s' % tag)

    raw_css_style = (';'.join(style_list)).replace("'", "\'")
    if raw_css_style:
        css_style = "style='%s'" % raw_css_style
        css_style = css_style.replace('\\g', '') # 以防被注入
        block_html = ''.join(block_html.rsplit(raw_tag_marker, 1)) # 先去掉原始声明的部分
        block_html = re.sub(r'^(\s*<[a-z0-9]+)( |>)', '\g<1> %s \g<2>'%css_style, block_html, flags=re.I)

    return block_html # at last






