#coding: utf8
from __future__ import absolute_import
from .blocks_line_by_line import smart_unicode, compute_markdown_blocks_line_by_line, is_pure_list_text, is_list_item_line
from .md_block import md5
import re
from collections import OrderedDict

import misaka as m
basic_markdown_render = m.HtmlRenderer()
basic_markdown_compiler = m.Markdown(basic_markdown_render, extensions=m.EXT_STRIKETHROUGH)
line_char = u'\uffff'


def curry(_curried_func, *args, **kwargs):
    def _curried(*moreargs, **morekwargs):
        return _curried_func(*(args+moreargs), **dict(kwargs, **morekwargs))
    return _curried



def footnote_replacer(match, footnote_refs=None, ref_counter=None, block_text=None):
    if ref_counter is None:
        ref_counter = {}
    if footnote_refs is None:
        footnote_refs = {}
    block_text = block_text or ''
    start_position = match.start()
    footnote_ref_text = match.group(1)
    footnote_key = match.group(2)
    all_text = footnote_ref_text

    footnote_key = footnote_key.strip()
    if footnote_key not in footnote_refs:
        return all_text

    # 可能被 ** ` ~ * 包裹的
    pre_2_chars = block_text[start_position-2:start_position]
    pre_char = block_text[start_position-1:start_position]
    if pre_2_chars == '**':
        pre_line_text = block_text[:start_position].split('\n')[-1]
        if pre_line_text.count(pre_2_chars)%2!=0:
            return all_text
    elif pre_char in ['*', '~', '`']:
        pre_line_text = block_text[:start_position].split('\n')[-1]
        if pre_line_text.count(pre_char)%2!=0:
            return all_text

    if footnote_key in ref_counter:
        footnote_index = ref_counter[footnote_key]
    else:
        ref_index = ref_counter.get('__') or 1
        footnote_index = ref_index
        ref_counter[footnote_key] = footnote_index
        ref_index += 1
        ref_counter['__'] = ref_index
    href_key = u'fn_%s' % md5(footnote_key)
    sup_key = u'sup_%s' % href_key
    note_content = footnote_refs.get(footnote_key) or ''
    note_content = note_content.replace('\n', ' ').replace('"', '') # 避免破坏 html
    footnote_ref_html = u'<sup id="%s" data-key="%s" data-title="%s"><a href="#%s" rel="footnote">%s</a></sup>' % (sup_key, footnote_key, note_content, href_key, footnote_index)
    return footnote_ref_html



def pre_compile_footnotes(footnote_refs, content):
    if not footnote_refs:
        return content

    content_list = []
    ref_counter = OrderedDict()
    new_blocks = compute_markdown_blocks_line_by_line(content)
    for block_range, block_type in new_blocks:
        start, length = block_range
        block_text = content[start: start+length]
        if block_type == 'normal':
            # 将其中 footnote 的 ref 进行 HTML 化
            replacer_func = curry(footnote_replacer, footnote_refs=footnote_refs, ref_counter=ref_counter, block_text=block_text)
            block_text = re.sub(r'(\[\^([^\[\]]+)\])', replacer_func, block_text) # , flags=re.M
        content_list.append(block_text)

    # 将所有 hit 到的 footnote_refs 进行对应
    if ref_counter:
        footnote_html_list = []
        for footnote_key in ref_counter.keys():
            if footnote_key == '__':
                continue
            footnote_value = footnote_refs.get(footnote_key) or ''
            href_key = u'fn_%s' % md5(footnote_key)
            sup_key = u'sup_%s' % href_key
            footnote_value_html = basic_markdown_compiler(footnote_value).strip()
            footnote_value_html = footnote_value_html.replace('<p>', '', 1).replace('</p>', '', 1)
            li_html = u'<li id="%s">\n<span>%s</span>\n<a href="#%s" rev="footnote">↩</a>\n</li>' % (href_key, footnote_value_html, sup_key)
            footnote_html_list.append(li_html)

        footnotes_inner_html = u'\n'.join(footnote_html_list)

        footnotes_html = u'\n\n<div class="footnotes">\n<hr>\n<ol>\n%s\n</ol>\n</div>' % footnotes_inner_html
        content_list.append(footnotes_html)


    new_content = ''.join(content_list)

    return new_content





def repeated_n_replacer(match):
    ns = match.group()
    n_count = len(ns)
    repeated_count = n_count - 2
    return '\n\n<span class="md_repeated_n md_repeated_n_%s"></span>\n\n' % repeated_count


def mathjax_replacer(match):
    head, body, tail = match.groups()
    head = head or ''
    tail = tail or ''
    mathjax_content = '%s\n```mathjax\n%s\n```%s' % (head, body, tail)
    return mathjax_content



def fix_complex_list(list_text):
    # 复杂 list， 每个 item 上增加一个空行，以进行复杂些的渲染逻辑
    raw_lines = list_text.split('\n')
    lines = []
    for i, line in enumerate(raw_lines):
        if not i:
            lines.append(line)
            continue
        pre_line = raw_lines[i-1]
        pre_line_strip = pre_line.strip()
        if pre_line_strip and is_list_item_line(line):
            line = '\n%s' % line
        lines.append(line)
    return '\n'.join(lines)


def fix_content_before_compile(content):
    content = smart_unicode(content)
    content = content.replace('\r\n', '\n').replace('\t', '    ') # 不使用 Tab 键 & \r\n

    footnote_refs = OrderedDict()

    blocks = compute_markdown_blocks_line_by_line(content)
    content_list = []
    pre_block_text = ''
    pre_block_type = None
    link_ref_list = []
    for block_range, block_type in blocks:
        start, length = block_range
        block_text = content[start: start+length]
        pre_block_has_empty_line = pre_block_text.endswith('\n\n')


        if block_type == 'normal':
            # 将多个 \n 进行替换成其它有意义的 dom 元素

            block_text=  re.sub(r'(\n|^)\$\$ *\n(.*?)\n\$\$ *($|\n)', mathjax_replacer, block_text, flags=re.S) # 数学公式, 转成 code block 的模式

            block_text = re.sub('\n{3,}', repeated_n_replacer, block_text)

            # 提取 footnotes 的逻辑, 以及保存其次序, 这样, 即使 part 的解析, 也可以保持一致
            # [^xxx]  & [^xxxx]: xxx
            for footnote_line, footnote_key, footnote_value in re.findall(r'(^\s*\[\^([^\[\]]+)?\]:\s*(.*?(?:\n|$)))', block_text, flags=re.I|re.M):
                footnote_value = footnote_value.strip()
                footnote_key = footnote_key.strip()
                footnote_refs[footnote_key] = footnote_value
                block_text = block_text.replace(footnote_line, '')

            # [xxx]: xxx
            for link_ref_pre_char, link_ref_line, link_ref_line_next_char in re.findall('(^|\n)( *\[[^\[\]]+\]:[^\n]*)(\n|$)', block_text):
                link_ref_pre_char = link_ref_pre_char or ''
                link_ref_line_next_char = link_ref_line_next_char or ''
                link_ref_list.append(link_ref_line.strip())
                original_line = u'%s%s%s' % (link_ref_pre_char, link_ref_line, link_ref_line_next_char)
                new_line = u'%s%s' % (link_ref_pre_char, link_ref_line_next_char)
                block_text = block_text.replace(original_line, new_line)

            if pre_block_type and pre_block_type in ['list', 'blockquote']:
                # 在 normal 紧跟 list & blockquote 的情况下, 去掉前面的空字符, 避免格式错误
                blank_header_r = re.search(r'^ +', block_text)
                if blank_header_r:
                    blank_header = blank_header_r.group()
                    new_blank_header = blank_header.replace(' ', '&nbsp;')
                    block_text = block_text.replace(blank_header, new_blank_header, 1)

        if block_type == 'code_block':
            # code block 的自动补全
            if not re.search('\n```\s*\n?$', block_text):
                block_text = block_text.rstrip()+'\n```\n'

        if block_type == 'blockquote':
            # blockquote 中间连接的补全
            block_text = re.sub(r'(^|\n)(>)\s*(\n|$)', '\g<1>\g<2> &nbsp;\g<3>', block_text)
            block_text += '\n<!--blockquote-->\n\n' # 确保 blockquote 的分段, 如果连续的存在

        if block_type == 'list':
            block_text = fix_complex_list(block_text)
        if block_type == 'list' and not block_text.startswith(' ') and not is_pure_list_text(block_text):
            # 可能是有嵌套的 list， 末尾补全一个占位, 这样即使一个 item，也能用复杂逻辑渲染
            block_text = block_text.rstrip() + '\n\n- &nbsp;<span class="__is_wrapped_paragraph"></span>\n'


        if block_type in ['code_block', 'blockquote', 'list']:
            # fenced code & blockquote 头尾补全一个\n, 如有必要
            if not pre_block_has_empty_line:
                block_text = '\n\n'+block_text
            block_text += '\n\n'


        content_list.append(block_text)

        pre_block_text = block_text
        pre_block_type = block_type


    # [xx]: xx link 模式的
    if link_ref_list:
        link_refs_text = '\n\n\n%s\n\n' % '\n'.join(link_ref_list)
        content_list.append(link_refs_text)

    fixed_content = ''.join(content_list)

    # footnote 的处理, 因为需要有个全局的 refs
    if footnote_refs:
        fixed_content = pre_compile_footnotes(footnote_refs, fixed_content)


    # div block的行补全
    fixed_content = re.sub(r'([^\n])(\n<\!--/.*?/-->\n)', '\g<1>\n\g<2>', fixed_content)
    fixed_content = re.sub(r'([^\n])(\n<\!--/-->\n)', '\g<1>\n\g<2>', fixed_content)

    # 处理more
    fixed_content = re.sub(r'[^\n]<!-- *more *-->[\r\n]', '\n<!--more-->\n', fixed_content, 1)

    return fixed_content