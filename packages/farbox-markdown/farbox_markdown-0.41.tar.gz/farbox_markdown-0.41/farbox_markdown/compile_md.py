#coding:utf8
import sys,re, os, misaka as m
from farbox_markdown.zrey_utils import UnicodeWithAttrs, smart_unicode, smart_str
from pygments.lexers.web import PhpLexer
from pygments.lexers import get_lexer_by_name as _get_lexer_by_name, ClassNotFound
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from .meta import safe_yaml, extract_metadata
from .md_h import text_to_table, text_to_flow
from .lexers import JadeLexer
from .util import string_types, smart_tag_style_for_block_html, NAMED_COLORS_AND_BACKGROUND
from .fix import fix_images_in_markdown, fix_relative_image_path

from .more.auto_fix import fix_content_before_compile
from .more.md_block import get_md_blocks_info, collect_sub_html_blocks, get_wrap_html_for_markdown_render
from .wiki_link_syntax import compile_markdown_wiki_link_syntax

import shortuuid
import hashlib
from collections import OrderedDict


# for backup
HOEDOWN_BLOCK_TYPES = {
    0: 'atxheader',
    1: 'htmlblock',
    2: 'empty',
    3: 'hrule',
    4: 'fencedcode',
    5: 'table',
    6: 'blockquote',
    7: 'blockcode',
    8: 'list',
    9: 'ordered_list',
    10: 'paragraph',
}

def pick_int(value, default_if_fail=0):
    # 从字符串中, 获得一个整数值, 如果其中有包含的还
    if isinstance(value, string_types):
        s = re.search(r'-?\d+', value)
        if s:
            return int(s.group())
    return default_if_fail

# for both 2.x & 3.x
try: # python2.x
    from urlparse import urlparse, parse_qs
except: # python3.x
    from urllib.parse import urlparse, parse_qs
try: # python2.x
    from urllib import quote_plus
except: # python3.x
    from urllib.parse import quote_plus
try: # 2.x
    import HTMLParser
    html_parse = HTMLParser.HTMLParser()
    html_unescape = html_parse.unescape
    import cgi
    html_escape = cgi.escape
except:
    from html.parser import HTMLParser
    import html
    html_parse = HTMLParser()
    html_unescape = html.unescape
    html_escape = html.escape


def md5(text):
    text = smart_str(text)
    return hashlib.md5(text).hexdigest()


def rreplace(s, old, new):
    try:
        place = s.rindex(old)
        return ''.join((s[:place],new,s[place+len(old):]))
    except ValueError:
        return s


domain_re = re.compile(r'^([a-z0-9][a-z0-9-_]+[a-z0-9]\.|[a-z0-9]+\.)+([a-z]{2,3}\.)?[a-z]{2,9}$', flags=re.I)

is_win = sys.platform == 'win32'

TOC_MARKER = '<!--MD_TOC-->'


def get_lexer_by_name(lang, **options):
    if lang in ['jade']:
        return JadeLexer()
    return _get_lexer_by_name(lang, **options)




def get_value_from_get_qs(qs, key):
    value = qs.get(key)
    if isinstance(value, (list, tuple)) and len(value)==1:
        return value[0]
    else:
        return value


def get_get_var(url, key):
    u = urlparse(url)
    query = u.query
    if not query:
        if isinstance(key, (list, tuple)):
            return [None] * len(key)
        else:
            return
    else:
        qs = parse_qs(query)
        if isinstance(key, (list, tuple)): # key 实际上一个 list
            values = []
            for k in key:
                value = get_value_from_get_qs(qs, k)
                values.append(value)
            return values
        else:
            return get_value_from_get_qs(qs, key)




# patch pygments
default_php_init = PhpLexer.__init__
def patched_php_lexer_init(self, **options):
    options['startinline'] = True
    default_php_init(self, **options)
PhpLexer.__init__ = patched_php_lexer_init


# misaka utils
BASIC_MISAKA_EXTENSIONS = m.EXT_TABLES | m.EXT_FENCED_CODE | m.EXT_STRIKETHROUGH | m.EXT_MATH

# 禁用缩进产生的代码块 &  __xx__ 这个语法
BETTER_MISAKA_EXTENSIONS = BASIC_MISAKA_EXTENSIONS | m.EXT_NO_INTRA_EMPHASIS | m.EXT_DISABLE_INDENTED_CODE

# https://github.com/hoedown/node-hoedown/blob/master/doc/document.markdown

line_char = u'\uffff'

def can_find_code_lang(lang):
    if lang in ['flow', 'flow-r', 'table', 'mathjax']:
        return True
    else:
        try:
            get_lexer_by_name(lang)
            return True
        except:
            return  False


def make_line_chars_as_position_points(html_content, force=False):
    # 比如数学公式、echart、流程图 等, 实际上是更改了文本的最终内容
    # 那么其上的 line_char 本身会破坏视觉内容, 将其全部提取出来, 作为一个 layout 上的 absolute 处理, 从而作为一个位置的参考坐标
    # 主要的用户是 scroller 同步滚动的时候可以用到
    if line_char not in html_content:
        return html_content # 不处理
    if not force  and '<script' not in html_content and '<!--js_run_it-->' not in html_content:
        # 目前有个特征, 都是最终转为 js script 的
        return html_content
    line_chars_count = html_content.count(line_char)
    line_chars_positions_html = ''
    height_percent = round(1/float(line_chars_count) * 100)
    for i in range(line_chars_count):
        line_chars_positions_html += """<div style="height:%s%%; position:relative;">
            <span style="position:absolute; bottom:0; height:1px;">%s</span>
        </div>\n"""%(height_percent, line_char)
    html_content = html_content.replace(line_char, '')
    marked_html_content = """
    <div class="mark_for_line_chars" style="position:relative">
        <div class="mark_for_line_chars_body">%s</div>
        <div class="mark_for_line_chars_positions" style="position:absolute; height:100%%;width:2px;left:0;top:0;">
            %s
        </div>
    </div>
    """ % (html_content, line_chars_positions_html)
    return marked_html_content


class FarBoxRenderer(m.HtmlRenderer):
    def __init__(self, flags=0, nesting_level=0, is_code_file=False,
                 raw_content='', compute_md_blocks=False, root_path='', filepath='',
                 for_local=False, fix_image_paths=True, metadata=None):
        m.HtmlRenderer.__init__(self, flags, nesting_level)
        self.is_code_file = is_code_file

        self.metadata = metadata or {} # 头部 metadata 的声明
        self.root_path = root_path
        self.filepath = filepath
        self.for_local = for_local
        self.should_fix_image_paths = fix_image_paths

        self.raw_content = raw_content

        # 存储编译的meta信息的相关字段
        self.raw_blocks_info = {}
        self.raw_bytes = ''
        self.html_blocks = OrderedDict() # id: [html_content_1, html_content_2, ]
        self.used_block_length = 0 # for bytes
        self.block_length = 0 # for unicode
        self.html_length = 0 # 已经获得的  html length

        self.toc_i = 0

        self.toc_html_parts = []

        # every block is dict type Data, dict(text, html, text_end_position, html_end_position)
        self.blocks = []

        self.should_compute_md_blocks = compute_md_blocks

        self.is_first_part = True
        self.is_first_header = True

    def header(self, content, level):
        hash_name = ""
        hash_name_c = re.search("[^#]+(#[0-9\w]+$)", content, flags=re.I)
        if hash_name_c:
            hash_name = hash_name_c.group(1).lstrip("#")
            content = re.sub("(#[0-9\w]+$)", "", content, flags=re.I)
        h_class_name = 'h16'
        if self.is_first_header:
            h_class_name += ' md_first_h'
            self.is_first_header = False
            if self.is_first_part:
                h_class_name += ' md_first_part'
        if re.search('<.*?>', content) and not re.search('</.*?>', content):  # header 中有  <??> 但是没有  </xxx> 的进行 escape 的处理
            content = html_escape(content)
        header_html = '<h%s id="toc_%s" class="%s"><span class="span_for_h">%s</span></h%s>\n' % (level, self.toc_i, h_class_name, content, level)
        header_html = smart_tag_style_for_block_html(header_html)
        header_html = line_patch(header_html)
        self.toc_i += 1
        self.toc_html_parts.append(header_html)
        if hash_name:
            header_html += '<a name="%s" class="md_hash_name md_header_hash_name"></a>'%hash_name
        return header_html


    def blockcode(self, text, lang):
        result = self._blockcode(text, lang)
        return result + '\n<!--block_code_end-->'

    def double_emphasis(self, text):
        return '<strong class="md_compiled md_compiled_strong">%s</strong>' % text

    def emphasis(self, text):
        return '<em class="md_compiled md_compiled_em">%s</em>' % text

    def codespan(self, text):
        text = text.strip()
        if '\n' in text:
            # 无 lang，则是 \n 开头
            lang, code_content = text.split('\n', 1)
            lang = lang.strip()
            if not re.search('\s', lang):
                blockcode_result = self._blockcode(code_content,  lang)
                return blockcode_result
        text = html_escape(text)
        text = text.replace('*', '&#42;') # 转义 * 号

        # inline style 的直接处理
        if self.metadata:
            maybe_inline_style_name = re.split(u'[:\uff1a]',text, 1)[0]
            if maybe_inline_style_name:
                try:
                    maybe_inline_style_name = 'style_%s' % maybe_inline_style_name.strip()
                    if maybe_inline_style_name in self.metadata:
                        inline_style = self.metadata.get(maybe_inline_style_name)
                        if isinstance(inline_style, string_types):
                            text = re.split(u'[:\uff1a]',text, 1)[-1].strip()
                            result = '<span class="inline_style_by_code md_compiled" style="%s">%s</span>' % (inline_style, text)
                            return result
                except:
                    pass

        # 默认用颜色直接构建的 inline style 的处理
        if re.search(u"[:\uff1a]", text):
            maybe_inline_text_parts = re.split(u"[:\uff1a]", text, 1)
            color_key = maybe_inline_text_parts[0].strip().lower()
            text_to_be_colored = maybe_inline_text_parts[1]
            font_color = NAMED_COLORS_AND_BACKGROUND.get(color_key)
            if text_to_be_colored and  font_color:
                inline_style = "display:inline;color:%s; background:%s; border-radius:5px; padding:5px 12px; margin-right:5px" % (font_color, color_key)
                result = "<span class=\"inline_style_by_code md_compiled\" style=\"%s\">%s</span>" % (inline_style, text_to_be_colored)
                return result

        result = '<code>%s</code>' % text
        return result


    def _blockcode(self, text, lang):
        raw_lang = lang = lang.replace(u'\uff1a', ':')
        text = text.strip('\r\n')

        if lang:
            if lang.lower() in ['oc', 'objective-c', 'objective_c', 'objectivec']:
                lang = 'objc'
            elif lang.lower() in ['node', 'nodejs']:
                lang = 'javascript'

        if not lang:
            return '\n<pre><code>%s</code></pre>\n' %  html_escape(text)

        # special syntax starts
        elif lang in ['mathjax', 'math']: # 处理数学公式 # <!--random_uuid-->
            content_md5 = md5(text.strip())
            block_html = '\n<section class="mathjax_script" id="Math%s" content_id="%s">$$\n%s$$\n</section>\n' % (shortuuid.uuid(), content_md5, text)
            return make_line_chars_as_position_points(block_html, force=True)

        elif lang in ['mermaid']: # 处理 mermaid 流程图 # <!--random_uuid-->
            content_md5 = md5(text.strip())
            block_html = '\n<!--js_run_it--><div class="mermaid" id="mermaid_%s" content_id="%s">%s</div>\n'%(shortuuid.uuid(), content_md5, text)
            return make_line_chars_as_position_points(block_html)

        elif lang in ['table'] or lang.startswith('table:'): # 对table语法的特殊处理
            fix_str= lang.split(':', 1)[-1] or '' if lang.startswith('table:') else ''
            block_html = text_to_table(text, fix_str)
            return make_line_chars_as_position_points(block_html)
        elif lang == 'flow':
            block_html = text_to_flow(text, is_raw=False)
            return make_line_chars_as_position_points(block_html)
        elif lang == 'flow-r':
            block_html = text_to_flow(text, is_raw=True)
            return make_line_chars_as_position_points(block_html)


        else:
            with_lines = lang.endswith(':n')
            lang = lang.split(':n')[0].lower().strip()
            try:
                # 匹配lang
                lexer = get_lexer_by_name(lang)
                css_class = 'codehilite is_code_file ' if self.is_code_file else 'codehilite '
                css_class += 'code_lang_%s ' % lang
                if with_lines:
                    css_class += 'with_lines '
                css_class += ' highlight'  # 会叠加成 highlighttable 这样的 class
                formatter = HtmlFormatter(linenos=with_lines, cssclass=css_class)
                return highlight(text, lexer, formatter)
            except: # ClassNotFound
                # lang 不存在, 但保留lang到pre的class中
                return '\n<pre class="lang_%s"><code>%s</code></pre>\n' %  (lang, html_escape(text))


    def is_repeated_n_html(self, html):
        if re.match('<span class="md_repeated_n md_repeated_n_\d+"></span>', html):
            return True
        else:
            return False

    def is_wrapped_paragraph(self, html):
        if re.search('class=[\'"]__is_wrapped_paragraph[\'"]', html):
            return True
        else:
            return False

    def paragraph(self, text):
        if self.is_repeated_n_html(text): # 纯占位的
            return text
        elif self.is_wrapped_paragraph(text):
            return text

        text = re.sub(r'&lt;!--(.*?)--&gt;(\n|$)', '<!--\g<1>-->\n', text) # HTML 注释的对应，反解析
        pre_text = re.sub(r'</?strong>|</?code>|</?del>|</?em>|</?a>|<a [^<>]*?>', '', text) # 避免 HTML 的误判
        if re.match(r'\s*<[\s\S]*>\s*$', pre_text) and 'md_compiled' not in text:
            # html 本身
            # 被当做 paragraph 的时候，会提前转义了
            text = html_unescape(text)
            text = '<p class="md_compiled md_paragraph_html">%s</p>' % text
            return text
        compiled_html = ''
        lines = re.split(r'\r?\n', text)
        line_length = len(lines)
        has_contents = False
        class_name_by_pre_line = '' # 从上一行的 dom 性质, 而继承下来的
        inner_p_class_name = ''

        pre_line_html = ''
        pre_line_class_names = ''

        comment_at_start = '' # avoid to break the P tag if we analytic comment for structure.
        comment_at_end = ''
        lines_count = len(lines)
        should_wrap_lines = True

        if lines and lines_count>=2 and lines[0].strip()==lines[-1].strip()=='$$':
            # mathjax $$ 的处理
            should_wrap_lines = False
            inner_p_class_name += ' mathjax_p'

        if not should_wrap_lines and lines_count:
            has_contents = True
            inner_p_class_name += ' p_without_wrap'

        for i, line in enumerate(lines):
            if not line.startswith('<img ') and re.match('\s*<.*?>\s*$', line) and 'class="md_compiled' not in line:
                # 纯 HTML & 图片另外处理，增加标识
                if i == lines_count - 1: # 尾行
                    compiled_html += line
                else:
                    compiled_html += line + '\n'
                continue
            line_class_names = 'md_line'
            line_split_str = '' if i+1==line_length else '<br />'
            if not should_wrap_lines: # line 不做任何的包裹
                class_name_by_pre_line = ''
                compiled_html += '%s%s\n' % (line, line_split_str)
            elif line.startswith('// ') or re.match('//?<', line): # 注释
                class_name_by_pre_line = ''
                line_core_content = line[3:]
                comment_content = '\n<!-- %s -->\n'% html_escape(line_core_content)
                if i == 0:
                    comment_at_start = comment_content
                elif i == line_length-1:
                    comment_at_end = comment_content
                else:
                    compiled_html += comment_content
            elif line.startswith('/// '): # 不会显示在源码中的注释
                class_name_by_pre_line = ''
                pass
            else:
                has_contents = True

                # 单行 [xxxx] 的处理
                if re.match(r'^\[.*?\]\s*%s?$'%line_char, line):
                    if '[toc]' in line.lower(): # TOC
                        line = line.lower().replace('[toc]', TOC_MARKER)
                        compiled_html += line
                        if line_length == 1:
                            return '<div class="toc_container">%s</div>' % compiled_html # 避免 TOC 被 P 影响
                        else:
                            # 已经处理好了
                            continue

                # 正常解析 line
                if line.startswith('<') and line.replace(line_char, '').endswith('>'):
                    line_class_names += ' md_line_dom_embed'
                if line.startswith('<img '): # 当前 line 有图片
                    line_class_names += ' md_line_with_image'
                if class_name_by_pre_line:
                    line_class_names += ' %s' % class_name_by_pre_line
                if i == 0:
                    line_class_names += ' md_line_start'
                if i == lines_count-1:
                    line_class_names += ' md_line_end'

                line = line_patch(line, compile_wiki_link=True)

                # 高度修饰
                if re.match("\[-?\d+\]\s*$", line.replace(line_char, "")):
                    int_value = pick_int(line)
                    if int_value >= 0:
                        line = re.sub("\[-?\d+\]", "<div class=\"height\" style=\"height:%spx\"></div>" % int_value, line)
                    else:
                        line = re.sub("\[-?\d+\]", "<div class=\"height\" style=\"height:1px;margin-top:%spx\"></div>" % int_value, line)
                    line_class_names += " md_line_height"

                space_before_line_m = re.match(' +', line)
                if space_before_line_m: # 保留空格的逻辑
                    space_chars = space_before_line_m.group()
                    line = line.lstrip(' ')
                    space_chars_count = len(space_chars)
                    space_chars_class = 'md_line_space_chars md_line_space_chars_%s' % space_chars_count
                    if space_chars_count > 200:
                        space_chars_class += ' md_line_space_chars_200 md_line_space_chars_200p'
                    line = '<span class="%s">%s</span>' % (space_chars_class, space_chars) + line
                line_html = '    <span class="%s">%s%s</span>\n'%(line_class_names, line, line_split_str)
                line_html = smart_tag_style_for_block_html(line_html)


                if line.startswith('<img '):
                    class_name_by_pre_line = 'img_before'
                    if 'md_line_dom_embed' in line_class_names:
                        # 这行前面, 仅仅一张图片为一行
                        class_name_by_pre_line += ' only_img_before'
                elif ' only_img_before' in class_name_by_pre_line: #  图片后面一行跟图片建立了关系, 同时让图片也知道后面存在这个逻辑
                    if compiled_html.endswith(pre_line_html):
                        related_class_names = ' '.join(['next_%s'%name for name in re.split(r'\s+', line_class_names)])
                        new_class_names = pre_line_class_names + ' ' + related_class_names
                        new_pre_line_html = pre_line_html.replace(pre_line_class_names, new_class_names)
                        compiled_html = compiled_html[:-len(pre_line_html)] + new_pre_line_html
                    class_name_by_pre_line = ''
                else:
                    class_name_by_pre_line = ''

                pre_line_html = line_html
                pre_line_class_names = line_class_names

                compiled_html += line_html



        if has_contents: # 如果全是注释内容功能，不会占用 dom 节点
            p_class_name = "md_block"
            if lines_count == 1:
                pure_text = re.sub(r'</?[^<]+?>', '', text).replace(line_char, "")
                if re.search("\\[[^\\^\\[\\]]+\\]$", pure_text): # 清掉 xx [xxx] 的修饰
                    pure_text = re.sub(u"\\[[^\\^\\[\\]]+\\]$", u"", pure_text).strip()
                if pure_text and pure_text[-1] in [":", u"："]:
                    # 约定，单独一行的 p 解析，最后是 ：结尾的，有 md_block_as_opening 这个 class
                    p_class_name += " md_block_as_opening"
            if inner_p_class_name:
                compiled_html = '<p class="%s">\n<section class="%s">\n%s</section>\n</p>' % ( p_class_name, inner_p_class_name, compiled_html)
            else:
                compiled_html = '<p class="%s">\n%s</p>' % (p_class_name, compiled_html)
            compiled_html = '%s\n%s\n%s\n' % (comment_at_start, compiled_html, comment_at_end)
        else:
            compiled_html = comment_at_start + compiled_html + comment_at_end

        compiled_html = re.sub(r'\*\*([^*]+)\*\*', '<strong>\g<1></strong>', compiled_html)
        compiled_html = patch_em(compiled_html)

        return compiled_html

    def math(self, text, displaymode):
        # Parse TeX $$math$$ syntax, Kramdown style
        return '$$%s$$' % text

    def blockquote(self, text):
        md_lines_count = text.count('class="md_line')
        if md_lines_count:
            blockquote_class_name = 'blockquote_lines_%s' % md_lines_count
        else:
            blockquote_class_name = ''
        #text = re.sub(r'\n{3,}', '\n</blockquote><blockquote>\n', text)
        if '<img ' in text:
            blockquote_class_name += ' blockquote_with_image'
        else:
            blockquote_class_name += ' blockquote_without_image'
        if blockquote_class_name:
            result = '\n<blockquote class="%s">%s</blockquote>\n' % (blockquote_class_name, text)
        else:
            result = '\n<blockquote>%s</blockquote>\n' % text
        return result

    def list(self, text, is_ordered, *args):
        is_ordered_list = is_ordered
        pure_content = re.sub("^<!--.*?-->", "", text)
        if is_ordered_list:
            prefix_info_match = re.match("<!--.*?-->", text)
            if prefix_info_match:
                prefix_info = prefix_info_match.group()
                position_search = re.search("\d+", prefix_info)
                if position_search:
                    position = position_search.group()
                    return "<ol class=\"md_list md_ol\" start=\"%s\">\n%s</ol>\n" % (position, pure_content)
            return "<ol class=\"md_list md_ol\">\n%s</ol>\n" % pure_content
        else:
            return "<ul class=\"md_list md_ul\">\n%s</ul>\n" % pure_content

    def listitem(self, text, *args):  #hoedown_list_flags
        # is_ordered, is_block
        #text_strip = text.strip()
        if text.startswith('&nbsp;') and re.search('class=[\'"]__is_wrapped_paragraph[\'"]', text): # 空占位
            return ''

        text = line_patch(text, compile_wiki_link=True)
        p_line_match = re.match(r'\n*<p class="md_block">\s*<span class="md_line.*?">(.*?)</span>\s*</p>', text)
        if p_line_match: # 嵌套性质的, 所以第一行会被解析为一个 p 元素, 尝试拆掉 第一个 p & span
            span_body = p_line_match.group(1)
            if '<span' not in span_body:
                text = text[:p_line_match.start()] + span_body + text[p_line_match.end():]

        # 空 item 产生的 h1~h6 语法的冲突
        text = re.sub(r'<h[1-6][^<>]*?></h[1-6]>\s*$', '', text)

        if re.match('^\[ ?\] ', text): # undo
            text = re.sub(r'\[ ?\] ', '', text, 1)
            listitem_html = '<li class="md_li todo_item todo_undone_item"><input type="checkbox"> %s</li>\n' % text
        elif re.match('^\[x\] ', text):
            text = re.sub(r'\[x\] ', '', text, 1)
            listitem_html = '<li class="md_li todo_item todo_done_item"><input type="checkbox" checked="checked" > %s</li>\n' % text
        else:
            listitem_html = '<li class="md_li"><span class="md_li_span">%s</span></li>\n' % text
        listitem_html = smart_tag_style_for_block_html(listitem_html)
        return listitem_html


    def link(self, text, link, title):
        if link and '://' not in link and not link.startswith('/') and domain_re.match(link):
            # 自动补全 http 协议，如果只是一个域名的话
            ext = os.path.splitext(link)[-1] or ''
            if ext.lower() in ['.html', '.htm', '.txt', '.md', '.mk', '.markdown'] and link.count('.') ==1:
                #一个具体的 page url，不补全协议
                pass
            else:
                link = 'http://%s' % link
        if '://' not in link: # 非协议式的，quote 一次
            link = link.replace(' ', '%20')
            link = quote_plus(smart_str(link), safe='?#& =/\\[]~+-_:%')

        if '://' not in link and '?path=' in link and '&' not in link:
            # ME 中的文档跳转, compile 的时候, 不输出 path
            ext = link.split('.')[-1].lower()
            if ext in ['md', 'mk', 'txt', 'markdown']:
                link = link.split('?')[0]

        s = re.search(r'(^.*?)\((.*?=.*?)\)$', text)
        if s:
            text, properties = s.groups()
            text = text.rstrip()
        else:
            properties = ''

        a_class = 'md_compiled'

        ext = os.path.splitext(link)[-1].lower()
        if ext in ['.mp4']: # 视频
            a_class += ' md_video'
        elif ext in ['.mp3']: # 音乐
            a_class += ' md_audio'

        if title:
            compiled_html = '<a class="%s" href="%s" title="%s">%s</a>' % (a_class, link, title, text)
        else:
            compiled_html = '<a class="%s" href="%s">%s</a>' % (a_class, link, text)
        if properties: # a 标签的额外属性
            compiled_html = '%s %s %s'% (compiled_html[:2], properties, compiled_html[2:])
        return compiled_html


    def image(self, link, title, alt ):
        extra = ''

        # 确保 image url 是有效的
        link = link.replace('#', '%23')

        rt = '' # 图片的自动旋转角度
        float_style = 0 # 左右浮动
        if "?" in link: # r w h 转为style
            styles = ''
            w, h, r, rt, float_style, is_align_center = get_get_var(link, ['w', 'h', 'r', 'rt', 'f', 'c'])
            if w: styles += "max-width:%spx;" % w
            if h: styles += "max-height:%spx;" % h
            if r: styles += "width:%s%%;" % r
            if is_align_center: styles += 'display:block; margin:0 auto;text-align:center'
            if float_style:
                if float_style == '1': # left
                    styles += 'display:block;float:left;margin:16px 16px 0 0;'
                elif float_style == '2':
                    styles += 'display:block;float:right;margin:16px 0 0 16px;'
            if styles:
                extra += 'style="%s"'%styles

            if w and not h and not r:
                extra += ' width="%s"' % w

        image_class = 'md_compiled '
        filename = os.path.split(link)[-1]
        if '@2x.' in filename:
            image_class = 'x2_image'
        elif '@3x.' in filename:
            image_class = 'x3_image'
        elif '@4x.' in filename:
            image_class = 'x4_image'

        if rt:
            image_class += ' img_rt_%s'%rt
        if float_style == "1":
            image_class += ' img_float_left'
        elif float_style == "2":
            image_class += ' img_float_right'

        # src 用的是 " 而不是单引号
        compiled_html = '<img class="%s" src="%s" alt="%s" title="%s" %s>' % (image_class, link, alt, title, extra)
        compiled_html = smart_tag_style_for_block_html(compiled_html)

        if self.should_fix_image_paths: # 可以确保图片的地址都是 / 开始的
            compiled_html = fix_images_in_markdown(self.filepath, compiled_html, self.root_path, for_local=self.for_local)

        if alt:
            compiled_html = '<figure class="md_figure md_image_figure">%s<figcaption>%s</figcaption></figure>' % (compiled_html, alt)

        return compiled_html


    def blockhtml(self, html):
        # div block 实质上不是逐行的, 跟 ME 的兼容有问题...
        html_strip = html.strip()
        if html_strip == '<!--blockquote-->':
            return ''
        if html_strip in ['<!--/-->']:
            html = '\n</div></div><!--md_div_block_ends-->\n'
        else:
            if html.startswith('<!--/'): # block starts
                block_search = re.search(r'^<\!--/(.*?)/-->\r?\n?$', html)
                if block_search:
                    properties_s = block_search.groups()[0]
                    html = '\n<div class="md_div_block"><div %s>\n' % properties_s
        return html


    def meta_info(self, block_type, block_length, ob):
        if ( (isinstance(block_type, int) and block_type > 0) or block_type) and self.is_first_part:
            self.is_first_part = False

        if not self.should_compute_md_blocks: # ignore
            return

        if block_type and isinstance(block_type, int) and block_type<0:
            if block_type == -2: # -2, 是补全后的 text, 解析的时候仅执行一次
                self.raw_bytes = m.utils.ffi.string(ob.data, ob.size)
                #with open('/Users/hepochen/Dev/QuanDuan/MacMarkEditor/tmp.txt', 'wb') as f:
                #    f.write(self.raw_bytes)
                self.raw_blocks_info = get_md_blocks_info(self.raw_bytes)
                #print(smart_unicode(self.raw_bytes), self.raw_content)
        else:
            new_used_block_length = self.used_block_length + block_length
            current_bytes = self.raw_bytes[self.used_block_length:new_used_block_length]
            current_html = m.utils.to_string(ob) # 当前 & 前文最终的 HTML 内容

            should_collect = True
            if block_type in ['empty']:
                should_collect = False
            if block_type == 'htmlblock':
                current_html_strip = current_html.strip()
                if current_html_strip == '<!--blockquote-->':
                    should_collect = False

            html_content = current_html[self.html_length:]

            current_text =  smart_unicode(current_bytes)
            unicode_block_length = len(current_text)

            block_range = [self.block_length, unicode_block_length]

            if should_collect:
                collect_sub_html_blocks(
                    data_obj=self.html_blocks,
                    blocks_info=self.raw_blocks_info,
                    block_range=block_range,
                    html_content = html_content,
                )

            self.used_block_length = new_used_block_length # for bytes
            self.block_length += unicode_block_length # for unicode
            self.html_length = len(current_html)



def _md_to_html(text, extensions, flags=None, is_toc=False, is_code_file=False,
                compute_md_blocks=False, wrap_md_blocks=False, keep_lines_between_paragraphs=False,
                filepath='', root_path='', for_local=False, fix_image_paths=True, metadata=None):
    # {%gist 7132248 %} --> <script src='https://gist.github.com/7132175.js'></script>
    # `gist 7132248` works too.
    text = re.sub(r'(?:^|\n)(?:\{%|`) *gist (\w+) *(?:%\}|`)\s*(?:\n|$)', "\n<script src='https://gist.github.com/\g<1>.js'></script>\n", text)
    if not is_toc:
        renderer = FarBoxRenderer(flags, nesting_level=6, is_code_file=is_code_file,
                                  raw_content=text, compute_md_blocks=compute_md_blocks,
                                  filepath=filepath, root_path=root_path,
                                  for_local=for_local, fix_image_paths=fix_image_paths, metadata=metadata)
    else:
        renderer = m.HtmlTocRenderer(nesting_level=6) # 没有flags
    markdown = m.Markdown(renderer, extensions)
    html_content = markdown(text)

    html_blocks = getattr(renderer, 'html_blocks', {})
    blocks_info = getattr(renderer, 'raw_blocks_info', {})

    if wrap_md_blocks:
        wrapped_html = get_wrap_html_for_markdown_render(html_blocks)
    else:
        wrapped_html = ''

    if is_toc and html_content == '</li>\n</ul>\n':
        html_content = ''

    # 尾段
    html_content = rreplace(html_content, '<p class="md_block">', '<p class="md_block last_md_block_in_page">')
    wrapped_html = rreplace(wrapped_html, '<p class="md_block">', '<p class="md_block last_md_block_in_page">')

    html_content = UnicodeWithAttrs(html_content)
    html_content.blocks_info = blocks_info
    html_content.html_blocks = html_blocks
    html_content.wrapped_html = wrapped_html

    return html_content



def line_patch(line, compile_wiki_link=False):
    # 由于 cjk 的关系, 比如** * ~~ 在没有空格的时候,未必有准确的对应
    # 但是前提是前、后不能跟英文、数字
    if compile_wiki_link:
        line = compile_markdown_wiki_link_syntax(line)
    line = re.sub('([^a-z0-9~]|\A)~~([^~<>]*?)~~([^a-z0-9~]|\Z)','\g<1><del>\g<2></del>\g<3>', line, flags=re.I) # 删除符的支持
    line = re.sub('(?<!\*)\*\*([^\*<>]*?)?\*\*(?!\*)','<strong>\g<1></strong>', line, flags=re.I) # 加粗
    line = patch_em(line)
    #line = re.sub('([^a-z0-9\*]|\A)\*([^\*<>]+?)\*([^a-z0-9\*]|\Z)','\g<1><em>\g<2></em>\g<3>', line, flags=re.I) # 斜体
    return line



def patch_em_replacer(match):
    em_inner_text = match.group(1)
    all_text = match.group()
    if re.match('[a-z0-9 \t]$', em_inner_text, flags=re.I):
        return all_text
    else:
        if re.search(r'</?.*?>', em_inner_text):
            return all_text
        else:
            return '<em class="md_patched_em">%s</em>' % em_inner_text

def patch_em(text):
    # em 标记符， 在 html 片段之内， 直接返回
    if re.search('<\w+>.*?\*.*?\*.*?</\w+>', text):
        return text
    new_text = re.sub('(?<!\*)\*(.*?)\*(?!\*)', patch_em_replacer, text)
    return new_text



def get_markdown_toc_html_content(content, old_markdown=False):
    extensions = BASIC_MISAKA_EXTENSIONS if old_markdown else BETTER_MISAKA_EXTENSIONS
    raw_content_for_toc = content.strip()
    toc_content = _md_to_html(raw_content_for_toc, extensions=extensions, is_toc=True)

    # toc_content 可以 html tag 不转义
    toc_content = re.sub(r'([^>])&lt;(.*?)&gt;', '\g<1><\g<2>>', toc_content) # <code>&lt;(.*?)&gt;</code> 这种则不处理
    toc_content = re.sub(r'&quot;(.*?)&quot;', '"\g<1>"', toc_content)
    toc_content = toc_content.replace(line_char, '') # 作为特定 line 的标记, 不能保留

    # TOC 中 去掉 [xxx] 的样式补全逻辑
    toc_content = re.sub(r'\[.*?\]</a>', '</a>', toc_content)

    toc_lines = toc_content.strip().split('\n')
    if len(toc_lines) >=7: # 仅仅一个层级，去掉，免得太难看
        if toc_lines[1].strip('</> \t') == toc_lines[-2].strip('</> \t') == 'li' and toc_content.count('</ul>')==2: # li
            if toc_lines[3].strip('</> \t') == toc_lines[-3].strip('</> \t') == 'ul':
                if toc_lines[2].strip().startswith('<a '):
                    toc_content = '\n'.join(toc_lines[3:-2])

    return toc_content


# begins

def blockquote_fix_man(match, code_block_positions):
    # '\g<1>>&nbsp;\n',
    start_position = match.start()
    part_one = match.group(1)
    for code_block_start, code_block_end in code_block_positions:
        if code_block_start <= start_position <= code_block_end:
            # 在代码片段内 不处理
            return match.group()
    joiner = match.group(2)
    return '%s%s' % (part_one, joiner.replace('>', '>&nbsp;'))

def markdown_to_html(content, old_markdown=False, no_html=False, toc=True, footnotes=True, is_code_file=False,
                     compute_md_blocks=False, wrap_md_blocks=False, filepath='', root_path='',
                     for_local=False, fix_image_paths=True, metadata=None):

    # 内容的预处理
    content = content.replace('\r\n', '\n').replace('\t', '    ')

    #flags = MISAKA_FLAGS
    flags = 0
    extensions = BASIC_MISAKA_EXTENSIONS if old_markdown else BETTER_MISAKA_EXTENSIONS

    if no_html:
        flags = m.HTML_SKIP_HTML | m.HTML_ESCAPE

    #if footnotes:
        #extensions |= m.EXT_FOOTNOTES


    if not old_markdown:
        # 性能降低 20% 左右
        content = fix_content_before_compile(content)
        #pass

    # 对需要compile的content的预处理
    # [url]: \t\t url 会解析错误
    #content = re.sub(r'(\n\[\S+\]:)(\t+)', '\g<1> ', content)

    # 尾部links&footernote的兼容(有些会有前面的空格)
    #content = re.sub(r'[ \t]*(\[.*?\]:.*?(\n|$))', '\g<1>', content)


    raw_content = content




    content = _md_to_html(raw_content, extensions=extensions, flags=flags, is_code_file=is_code_file,
                          compute_md_blocks=compute_md_blocks, wrap_md_blocks=wrap_md_blocks,
                          filepath=filepath, root_path=root_path, for_local=for_local, fix_image_paths=fix_image_paths,
                          metadata = metadata
                          )
    blocks_info = getattr(content, 'blocks_info', {})
    html_blocks = getattr(content, 'html_blocks', {})
    wrapped_html = getattr(content, 'wrapped_html', '')


    if toc:
        raw_content_for_toc = raw_content.strip()
        toc_content = get_markdown_toc_html_content(raw_content_for_toc, old_markdown=True)
    else:
        toc_content = ''

    if not old_markdown:
        block_tag_names = ['p']
        for tag in block_tag_names:
            for part in re.findall(r'<%s>.*?</%s>' %(tag, tag), content, re.S):
                _part = re.sub(r'[\r\n]+', '<br />', part)
                content = content.replace(part, _part, 1)

    content = UnicodeWithAttrs(content)
    content.html_blocks = html_blocks
    content.wrapped_html = wrapped_html
    content.blocks_info = blocks_info

    if toc:
        return content, toc_content
    else:
        return content


def get_cover(content):
    #提取图片作为封面
    cover = re.search("""<\s*img.*?src=['"]([^'"]+).*?>""", content, flags=re.I)
    if cover:
        cover = cover.groups()[0]
        if cover.startswith('/'):  # farbox本地的
            cover = cover.split('?', 1)[0]
    else:
        cover = None
    return cover




def p_bellow_block_replacer(match):
    # '<p class="md_block md_has_block_below md_has_block_below_\g<3>">\g<2>'
    groups = match.groups()

    p_inner_text = re.sub(r'<[^>]*?>', '', groups[1]).strip()
    opening_class_name = ''
    if p_inner_text and '\n' not in p_inner_text and p_inner_text[-1] in [':', u'：']:
        opening_class_name = 'md_block_as_opening'

    inner_part = groups[1]
    tail_part = groups[2]
    next_tag_name = groups[3]
    if 'codehilite' in next_tag_name:
        next_tag_name = 'code_block'

    new_html_part = '<p class="md_block %s md_has_block_below md_has_block_below_%s">%s%s' % (opening_class_name, next_tag_name, inner_part, tail_part)

    return new_html_part


def replace_toc_marker(content, toc_content):
    if TOC_MARKER not in content:
        return content
    content = content.replace(TOC_MARKER, '\n<div class="toc">'+toc_content+'</div>\n')
    return content


# 对外调用的主函数
def compile_markdown(content, path='/', remove_h1=True, toc=False, root=None,
                     compute_md_blocks=False, wrap_md_blocks=False, for_local=False,
                     compile_metadata=True, do_after_job=True, fix_image_paths=True, metadata=None):
    # 约0.008s处理一篇普通大小的文档, replace 基本上没有太大性能损耗，主要是正则处理比较复杂的时候性能会有损耗
    # 去除了markdown文档头部信息, 必须保证是头部...
    # path是指文档的路径，有些相对路径，特别是web类的应用，其它情况下则是文档的绝对路径
    # path是指相对site_path的相对路径，不以/开头，site_path下的直接文件不处理

    # root 是指post_path(path)的根目录，需要解析一套在本地&web端都可用的，所以会用到

    path = smart_unicode(path)
    if root:
        root = smart_unicode(root)

    content = smart_unicode(content)

    raw_content = content

    if compile_metadata:
        content, metadata = extract_metadata(content)  # 先做jekyll的兼容
    else:
        # 也有可能不做 metadata 的处置逻辑, 比如局部更新
        metadata = metadata or {}
        if not isinstance(metadata, dict):
            metadata = {}

    clean_raw_content = content  # 这个content是没有metadata内容了的

    ext = os.path.splitext(path)[1]

    # 是否使用老的引擎 （所谓的 native）
    old_markdown= (ext == '.mk')
    if not old_markdown and metadata.get('old_markdown') in ['True', True, 'true', 'yes']:
        old_markdown = True

    # 输出PDF用的, 强制分页
    content = re.sub(r'[\r\n]+\[page\][\r\n]+',
                     '\n\n<div class="page_break" style="page-break-after:always;border:none;height:0"></div>\n\n', content, flags=re.I)


    # 可以将整个markdown视为代码文件，比如hello.python.md， 但同时也支持metadata的声明
    is_code_file = False
    if path:
        filename = os.path.split(path)[-1]
        parts = filename.split('.')
        if len(parts)>=3:
            lang = parts[-2]
            if can_find_code_lang(lang):
                if metadata.get('lines', False): # 带代码行显示
                    content = '```%s:n\n%s\n```' % (lang, content)
                else:
                    content = '```%s\n%s\n```' % (lang, content)
                is_code_file = True


    content, toc_content = markdown_to_html(content, old_markdown, is_code_file=is_code_file,
                                            compute_md_blocks=compute_md_blocks, wrap_md_blocks=wrap_md_blocks,
                                            filepath=path, root_path=root, for_local=for_local,
                                            fix_image_paths=fix_image_paths, metadata=metadata
                                            )

    if not do_after_job:
        # 比如说局部的 compile, 这个时候, 直接返回内容就可以了; 不需要进行善后的逻辑
        return content


    html_blocks = getattr(content, 'html_blocks', {})
    wrapped_html = getattr(content, 'wrapped_html', '')

    if wrap_md_blocks:
        content = wrapped_html or content


    #content = fix_images_in_markdown(path, content, root=root) # /~/ 替换为 /_image/xxxxx/ .etc的处理

    title_from_post = False # title 的产生, 实质来自于 post 本身的内容

    cover = get_cover(content)
    h1_removed = False
    content = content.strip()
    h1s = re.findall(r'(<h1[^<]*?>(.*?)</h1>)', content, re.I)
    title_from_h1 = False
    if metadata.get('title'):
        title = metadata.get('title')
        title_from_post = True
    elif len(h1s) == 1:  # 如果仅有一个H1
        title = h1s[0][1]
        title = re.sub(r'<.*?>', '', title).strip() # 可能包含 html 源码, html to text
        if remove_h1: # 去除H1的内容
            content = content.replace(h1s[0][0], '', 1).strip()
            h1_removed = True
        title_from_post = True
        title_from_h1 = True
    else:
        title = os.path.split(path)[1].rsplit('.', 1)[0]
        title = re.sub(r'^\d+(\.\d+)? ', '', title) # 去掉可能的序号

    # ul/ol 上层 p 的 class 锚定
    # for p_item in re.findall(r'(<p class="md_block">)(.*?</p>\s*<(\w+)[> ])', content, re.M|re.S):
    #content = re.sub(r'(<p class="md_block">)((?:(?!</p>).*\n)+?)(</p>[\s\r\n]*<(ul|ol|blockquote|img|div class="codehilite)[> ])',
    #                 p_bellow_block_replacer, content)

    # toc
    if toc:
        content = replace_toc_marker(content, toc_content)

    if remove_h1 and h1_removed:
        # 避免 h1 被删除后，留出多余的hr
        content = content.lstrip()
        if content.startswith('<hr>'):
            content = content[4:]

    if metadata.get('cover') and isinstance(metadata.get('cover'), string_types):
        # 以 metadata 的cover 为优先
        cover = metadata.get('cover')

    if content.strip() == '<p></p>':
        content = ''

    #if metadata.get('css'):
        #css_content = metadata.get('css')
        #if isinstance(css_content, string_types):
            #content = '<style>%s</style>\n%s' % (css_content, content)

    metadata['title_from_post'] = title_from_post
    metadata['title_from_h1'] = title_from_h1

    content = UnicodeWithAttrs(content)
    content.clean = clean_raw_content
    content.metadata = metadata
    content.cover = cover
    content.toc = toc_content
    content.title = title
    content.title_from_post = title_from_post
    content.title_from_h1 = title_from_h1
    content.html_blocks = html_blocks
    content.wrapped_html = wrapped_html

    # the raw_head
    head_index = raw_content.find(clean_raw_content)
    if head_index != -1:
        content._head = raw_content[:head_index]
    return content
