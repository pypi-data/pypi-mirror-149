# coding: utf8
from bs4 import BeautifulSoup, NavigableString
import re
from farbox_markdown.zrey_utils import smart_unicode, UnicodeWithAttrs



try:
    from urllib import parse as urllib_parse
except:
    urllib_parse = None
import urllib

def url_unquote(url):
    if urllib_parse:
        return urllib_parse.unquote(url)
    else:
        return urllib.unquote(url)

convert_heading_re = re.compile(r'convert_h(\d+)')
line_beginning_re = re.compile(r'^', re.MULTILINE)
whitespace_re = re.compile(r'[\r\n\s\t ]+')
FRAGMENT_ID = '__MARKDOWNIFY_WRAPPER__'
wrapped = '<div id="%s">%%s</div>' % FRAGMENT_ID


# Heading styles
ATX = 'atx'
ATX_CLOSED = 'atx_closed'
UNDERLINED = 'underlined'
SETEXT = UNDERLINED

PROTECTED_CODE_TAIL = 'av2KUXQWaRpBm5wX4mxRST'

def escape(text):
    if not text:
        return ''
    return text.replace('_', r'\_')


def _todict(obj):
    return dict((k, getattr(obj, k)) for k in dir(obj) if not k.startswith('_'))


class MarkdownConverter(object):
    class DefaultOptions:
        strip = None
        convert = None
        autolinks = True
        heading_style = UNDERLINED
        bullets = '-*+'  # An iterable of bullet types.

    class Options(DefaultOptions):
        pass

    def __init__(self, **options):
        # Create an options dictionary. Use DefaultOptions as a base so that
        # it doesn't have to be extended.
        self.options = _todict(self.DefaultOptions)
        self.options.update(_todict(self.Options))
        self.options.update(options)
        if self.options['strip'] is not None and self.options['convert'] is not None:
            raise ValueError('You may specify either tags to strip or tags to'
                             ' convert, but not both.')
        self.images_info = []
        self.foot_notes = []

    def convert(self, html):
        # We want to take advantage of the html5 parsing, but we don't actually
        # want a full document. Therefore, we'll mark our fragment with an id,
        # create the document, and extract the element with the id.

        codes = re.findall(r"<code[^<>]*>.*?</code>", html)
        for code in codes:
            new_code = re.sub(r'    ', PROTECTED_CODE_TAIL, code)
            html = html.replace(code, new_code, 1)

        html = wrapped % html
        try:
            soup = BeautifulSoup(html, "lxml")
        except:
            soup = BeautifulSoup(html)
        text = self.process_tag(soup.find(id=FRAGMENT_ID), children_only=True)
        text = re.sub('\n{2,}', '\n\n', text)


        if self.foot_notes:
            text += '\n\n%s' % ('\n'.join(self.foot_notes))

        return text

    def process_tag(self, node, children_only=False):
        try:
            text = ''
            # Convert the children first
            for el in node.children:
                if isinstance(el, NavigableString):
                    raw_text = unicode(el)
                    if node.name == 'pre' and  '\n' in raw_text and not raw_text.strip().strip('\n'):
                        text += raw_text
                        continue
                    result = self.process_text(raw_text)
                    if text.endswith('\n') or not text:
                        result = result.lstrip(" ")
                    text += result
                else:
                    result = self.process_tag(el)
                    if getattr(el, 'name', None) == 'span':
                        if re.search(r'display: *block', el.get('style') or '', re.I):
                            result += '\n'
                    text += result

            if not children_only:
                convert_fn = getattr(self, 'convert_%s' % node.name, None)
                if convert_fn and self.should_convert_tag(node.name):
                    text = convert_fn(node, text)
        except:
            # tag 解析失败，返回原始的 html
            text = self.convert_original(node, '')

        return text

    def process_text(self, text):
        return escape(whitespace_re.sub(' ', text or ''))

    def __getattr__(self, attr):
        # Handle headings
        m = convert_heading_re.match(attr)
        if m:
            n = int(m.group(1))

            def convert_tag(el, text):
                return self.convert_hn(n, el, text)

            convert_tag.__name__ = 'convert_h%s' % n
            setattr(self, convert_tag.__name__, convert_tag)
            return convert_tag

        raise AttributeError(attr)

    def should_convert_tag(self, tag):
        tag = tag.lower()
        strip = self.options['strip']
        convert = self.options['convert']
        if strip is not None:
            return tag not in strip
        elif convert is not None:
            return tag in convert
        else:
            return True

    def indent(self, text, level):
        return line_beginning_re.sub('\t' * level, text) if text else ''

    def underline(self, text, pad_char):
        text = (text or '').rstrip()
        return '%s\n%s\n\n' % (text, pad_char * len(text)) if text else ''

    def convert_a(self, el, text):
        rel = el.attrs.get('rel')
        if rel and isinstance(rel, (list, tuple)):
            rel = rel[0]
        if rel in ['footnote']:
            # footnote 中的 link 不解析
            return text
        href = el.get('href')
        title = el.get('title')
        if self.options['autolinks'] and text == href and not title:
            # Shortcut syntax
            return '<%s>' % href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        text = text.replace('\_', '_')
        if href:
            return '[%s](%s%s)' % (text or '', href, title_part)
        else:
            return text or ''

    def convert_b(self, el, text):
        return self.convert_strong(el, text)

    def convert_blockquote(self, el, text):
        content = line_beginning_re.sub('> ', text.strip()) if text else ''
        return '\n%s\n\n' % content

    def convert_br(self, el, text):
        return '\n'

    def convert_em(self, el, text):
        return '*%s*' % text if text else ''

    def convert_hn(self, n, el, text):
        style = self.options['heading_style']
        text = text.rstrip()
        hashes = '#' * n
        if style == ATX_CLOSED:
            return '\n%s %s %s\n\n' % (hashes, text, hashes)
        return '\n%s %s\n\n' % (hashes, text)

    def convert_hr(self, el, text):
        return '\n\n- - - - - - - - - - -\n\n'

    def convert_i(self, el, text):
        return self.convert_em(el, text)

    def convert_list(self, el, text):
        nested = False
        while el:
            if el.name == 'li':
                nested = True
                break
            el = el.parent
        if nested:
            text = '\n' + self.indent(text, 1)
        text = re.sub('\n+', '\n', text) + '\n'
        # text = re.sub('\n{2,}', '\n\n', text)
        return text


    def convert_sup(self, el, text): # 脚注
        text = text.strip()
        if re.match(r'\d+$', text):
            data = el.attrs.get('title') or el.attrs.get('data') or el.attrs.get('data-title')
            if data and '%' in data:
                data = url_unquote(data)
            if data:
                data = smart_unicode(data)
                key = el.attrs.get('data-key') or el.attrs.get('key') or text
                self.foot_notes.append('[^%s]: %s' % (key, data))
                return '[^%s]' % key
        return '' # at last


    convert_ul = convert_list
    convert_ol = convert_list

    def convert_li(self, el, text):
        node = el

        # todo_list 的支持
        todo = None # means no todos here
        try:
            i_dom = node.findChild('i')  # font-awesome
        except:
            i_dom = None
        if i_dom:
            i_dom_class = i_dom.attrs.get('class') or []
            if 'icon-check-empty' in i_dom_class:
                todo = False
            elif 'icon-check-sign' in i_dom_class:
                todo = True

        if todo is None:
            todo_s = ''
        else:
            todo_s = '[x] ' if todo else '[ ] '

        parent = el.parent
        if parent is not None and parent.name == 'ol':
            try:
                bullet = '%s.' % (parent.findAll('li').index(el) + 1)
            except:
                bullet = '%s.' % (parent.index(el) + 1)
        else:
            depth = -1
            while el:
                if el.name == 'ul':
                    depth += 1
                el = el.parent
            bullets = self.options['bullets']
            bullet = bullets[depth % len(bullets)]
        return '%s %s%s\n' % (bullet, todo_s, text or '')

    def convert_p(self, el, text):
        text = '%s\n\n' % text if text else ''
        #text = re.sub('\n{2,}', '\n\n', text)
        text = text.replace('&nbsp;', ' ') # 空格
        return text

    def convert_div(self, el, text):
        div_class = el.attrs.get('class') or []
        if div_class and isinstance(div_class, (list, tuple)):
            first_div_class = div_class[0]
            if first_div_class in ['footnotes', 'linenodiv']:
                return ''
        if text.strip():
            return self.convert_p(el, text)
        else:
            return ''


    def convert_pre(self, el, text):
        # 代码高亮
        # for pretty_print js
        lang = ''
        show_lines = False

        pre_class = el.attrs.get('class') or []

        for p_class in pre_class:
            if p_class.startswith('language-'):
                    lang = p_class.replace('language-', '', 1)
        if 'linenums' in pre_class:
            show_lines = True

        code_dom = el.findChild('code')
        if code_dom:
            code_class = code_dom.attrs.get('class') or []
            if 'linenums' in code_class or 'linenos' in code_class or 'with_lines' in code_class:
                show_lines = True
            for c_class in code_class:
                if c_class.startswith('language-'):
                    lang = c_class.replace('language-', '', 1)
                    break

        elif getattr(el, 'parent', None):
            parent_class = el.parent.attrs.get('class') or []
            if 'linenums' in parent_class or 'linenos' in parent_class or 'with_lines' in parent_class:
                show_lines = True
            for c_class in parent_class:
                if c_class.startswith('code_lang_'):
                    lang = c_class.replace('code_lang_', '', 1)
                    break

        if code_dom and '\n' not in text.strip() and '\n' in code_dom.text.strip(): # for stackedit
            text = code_dom.text
        text = text.replace('\\_', '_')
        text = text.replace(PROTECTED_CODE_TAIL, '    ')

        if show_lines:
            text = re.sub('^\d+\. ?', '', text, flags=re.M)

        if text and not text.endswith('\n'):
            text += '\n'

        if show_lines and lang:
            return '\n```%s:n\n%s```\n\n' % (lang, text)
        elif lang:
            return '\n```%s\n%s```\n\n' % (lang, text)
        else:
            return '\n```\n%s```\n\n' % text

    def convert_strong(self, el, text):
        return '**%s**' % text if text.strip() else ''

    def convert_img(self, el, text):
        alt = el.attrs.get('alt', None) or ''
        if alt in ['null']:
            alt = ''
        src = el.attrs.get('src', None) or ''
        lazy_keys = ['lazyload', 'src', 'lazy']
        for lazy_key in lazy_keys: # lazyload 或者 data-src 这种类型
            if not src.strip(): # maybe lazy load
                keys = el.attrs.keys()
                for key in keys:
                    if lazy_key in key.replace('_', '').replace('-', '').lower():
                        src = el.attrs.get(key)
                        if src:
                            break
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        if src:
            if '?' in src:
                if src.count('?') > 1:
                    src = src.rsplit('?', 1)[0]
            else: # 尝试从属性中获得 w=xxx 的逻辑
                w = el.attrs.get('width')
                if w:
                    try:
                        w = int(w)
                        src = '%s?w=%s' % (src, w)
                    except:
                        pass
        img_text = '![%s](%s%s)' % (alt, src, title_part)
        self.images_info.append([src, img_text])
        return img_text


    def convert_original(self, el, text):
        # 返回原始的 html 源码
        try:
            return unicode(el)
        except:
            try: return str(el)
            except: pass
        return ''


    def convert_figure(self, el, text):
        return '\n\n%s\n\n' % text

    def convert_figcaption(self, el, text):
        return '\n%s\n' % text


    def convert_table(self, el, text):
        if text.strip():
            if text.strip().startswith('```'):
                return text # 代码高亮, 待行数的
            else:
                return '\n```table\n%s```\n\n' % text
        else:
            return ''


    def convert_th(self, el, text):
        text = text.replace('\_', '_')
        return '%s |' % text

    def convert_td(self, el, text):
        td_class = el.attrs.get('class')
        if td_class and isinstance(td_class, (list, tuple)):
            td_class = td_class[0]
        if td_class in ['linenos']:
            return text
        text = text.replace('\_', '_')
        return '%s |' % text

    def convert_tr(self, el, text):
        return '%s\n' % text.strip().rstrip('|')


    def convert_script(self, el, text):
        dom_type = el.attrs.get('type')
        if dom_type and isinstance(dom_type, (list, tuple)):
            dom_type = dom_type[0]
        if dom_type and 'math/tex' in dom_type:
            text = '\n```mathjax\n%s\n```\n\n' % text
        else:
            if text.strip():
                text = '\n%s\n' % text
        return text


    def convert_code(self, el, text):
        if '\n' not in text:
            return '`%s`' % text
        else:
            return text

    def convert_del(self, el, text):
        if '\n' not in text:
            return '~~%s~~' % text
        else:
            return text


    def convert_style(self, el, text):
        # style 节点不解析
        return ''







    convert_embed = convert_original
    convert_iframe = convert_original


def markdownify(html, **options):
    html = smart_unicode(html) # 先处理为unicode
    html = re.sub(r'<!--[^<>]*?-->', '', html)
    c = re.search('<body>(.*?)</body>', html, re.S)
    if c:
        html = c.group(1)
    try:
        md_converter = MarkdownConverter(**options)
        result = md_converter.convert(html)
        images_info = md_converter.images_info
        result = re.sub(r'\n *<hr */?> *\n', '\n- - - - - - - - - - -\n\n', result)
        result = result.strip(' \n')
        result = UnicodeWithAttrs(result)
        result.images_info = images_info
    except: # 解析失败
        result = html
    return result