# coding: utf8
from __future__ import absolute_import
import re
import shortuuid, hashlib
import misaka as m
from .echarts import create_bar_table, create_pie_table, create_line_table
from .wiki_link_syntax import compile_markdown_wiki_link_syntax
# markdown for human


def md5(text):
    if isinstance(text, unicode):
        text = text.encode('utf8')
    return hashlib.md5(text).hexdigest()



line_char = u'\uffff'

def is_number(s):
    s = s.replace(line_char, '')
    s = s.strip()
    if re.match('\d+(\.\d+)?$', s): # like 1 or 2.1
        return True
    elif re.match('\.\d+$', s): # like  .35
        return True
    return False


basic_markdown_render = m.HtmlRenderer()
basic_markdown_compiler = m.Markdown(basic_markdown_render, extensions=m.EXT_STRIKETHROUGH)

def text_to_table(text, fix_str='', auto_markdown=True, just_table=False):
    # just table 的话，肯定会返回 table 的 html，而忽略 chart
    # 获得表格的类型
    if fix_str in ['bar', 'pie', 'line']:
        table_type = fix_str
        fix_str = ''
    else:
        table_type = 'default'
    lines = text.strip().split('\n')
    parts = []
    max_num = 0
    for line in lines:
        if not line.strip():
            continue
        columns = re.split('\|', line.strip('|').strip().rstrip('|'))
        if len(columns) > max_num:
            max_num = len(columns)
        parts.append(columns)
    if len(parts)<2:
        return ''

    # 补全列
    fixed_parts = []
    for columns in parts:
        if len(columns) != max_num:
            columns += [fix_str]*(max_num-len(columns))
        fixed_parts.append(columns)

    head = parts[0]
    aligns = {}
    head_body = ''
    for i, h in enumerate(head):
        h = h.replace(line_char, '').strip()
        hc = re.search(u'[(\uff08](left|right|center|[<\->])[)\uff09]$', h)
        if hc:
            align = hc.groups()[0]
            h = re.sub(u'[(\uff08](left|right|center|[<\->])[)\uff09]$', '', h)
        else:
            align = 'left'
        if align == '-': align = 'center'
        if align == '<': align = 'left'
        if align == '>': align = 'right'
        head_body += '<th style="text-align:%s">%s</th>\n' % (align, h)
        aligns[i] = align

    body_rows = parts[1:]
    t_head = "<tr>%s </tr>\n" % head_body
    t_body = ''
    row_objs = []
    for row in body_rows:
        row_obj = {'numbers': {}, 'strings': {}, 'blanks': {}, 'is_blank': False}
        row_body = ''
        for i, cell in enumerate(row):
            if not cell.strip():
                row_obj['blanks'][i] = cell
            else:
                if is_number(cell):
                    row_obj['numbers'][i] = cell.replace(' ', '').replace('\t', '')
                else:
                    row_obj['strings'][i] = cell.strip()

            align = aligns.get(i, 'left')
            cell_strip = cell.strip()
            if auto_markdown:
                cell = compile_markdown_wiki_link_syntax(cell)
            if auto_markdown and len(cell_strip)>1 and re.match(r'^[\[*,!~\-]', cell_strip): # 一些行内的 markdown 语法的支持
                cell = basic_markdown_compiler(cell).strip()
                if cell.startswith('<p>'): cell = cell[3:]
                if cell.endswith('</p>'): cell = cell[:-4]
            row_body += '<td style="text-align:%s">%s</td>\n' % (align, cell)

        # 判断是否是可图表化的数据模型
        append_obj = False
        if len(row_obj['strings']) == 1 and not row_obj['blanks']: # key, values 的模式
            append_obj = True
        elif not row_obj['blanks'] and not row_obj['strings']: # 全都是 num value
            append_obj = True
        elif not row_obj['strings'] and not row_obj['numbers']: # all blank 意味着 split
            row_obj['is_blank'] = True
            append_obj = True
        if append_obj:
            row_objs.append(row_obj)

        t_body += '<tr>%s</tr>\n' % row_body
    table_html = '<table>\n <thead>%s</thead>\n <tbody>%s</tbody> \n</table>' % (t_head, t_body)

    if just_table:
        return table_html

    # 分析row_objs
    x1 = head[0].strip() # 第一行的第一个元素
    xs = [s.strip() for s in head[1:]] # x 坐标的 names
    ys = [] # y 坐标的 names，也可能最终为空
    value_parts = []
    value_part = [] # just a container
    has_ys = True
    if re.match(r'\(/.*\)$', x1):
        # 如果 x1 由括号包裹，则认为有 y 轴的
        x1 = x1[1:-1]
        has_ys = True
    else:
        for row_obj in row_objs: # 先判断有没有 y 轴什么事情
            if len(row_obj.get('strings', []))!=1 and has_ys:
                # 如果有一个 strings 的 length 不为1，就认为 y 轴是没有的; 这个比较严格，就意味着左侧第一列如果要参与数据模型
                # 就不能有数字参与
                has_ys = False
                break

    if has_ys:
        ys.append(x1)
    else:
        xs.insert(0, x1) # 回收 x1 到xs 里面
    for row_obj in row_objs:
        if row_obj.get('is_blank'): # 这是元素的分割
            if value_part:
                value_parts.append(value_part)
            value_part = [] #
            continue
        numbers = list(row_obj['numbers'].values())
        if has_ys:
            ys.append(list(row_obj['strings'].values())[0])
            value_part.append(numbers)
        else:
            value_part.append(numbers)
    # at last
    if value_part:
        value_parts.append(value_part)

    chart_html = ''
    if value_parts: # numbers works
        if table_type == 'bar':
            chart_html = create_bar_table(xs, value_parts, ys)
        elif table_type == 'line':
            chart_html = create_line_table(xs, value_parts, ys)
        elif table_type == 'pie':
            chart_html = create_pie_table(xs, value_parts, ys)
    if chart_html:
        content_md5 = md5(text)
        chart_html = chart_html.replace('class="md_echarts"', 'class="md_echarts" content_id="%s"'%content_md5)
        return chart_html


    return table_html






def text_to_flow(text, is_raw=False):
    line_chars_count = text.count(line_char)
    text = text.replace(line_char, '')
    text = text.strip()+'\n'
    flow_text = text
    if not is_raw: # 校验当前格式严格符合我们的规则，不然不进行特别转义
        text = text.replace('\r\n', '\n')
        text = re.sub('\n{2,}', '\n', text)
        s = re.search(r'^((?:^\w+:.*?\n)+)(\s*)((?:^[\w\s\(\)>]+?\n)+)\Z', text, flags=re.M)
        if s:
            head, space, body = s.groups()
            head_parts = [part.strip().split(':', 1) for part in head.strip().split('\n')]
            if len(head_parts) >= 3: # head的最小数量要求
                # 变量声明
                start_key, start_value = head_parts[0]
                end_key, end_value = head_parts[-1]
                head_body = head_parts[1:-1]
                flow_text = '%s=>start: %s\n' % (start_key, start_value)
                for b_key, b_value in head_body:
                    kind = 'operation'
                    if re.search(u'(\uff1f|\?)\s*$', b_value.strip()):
                        kind = 'condition'
                    flow_text += '%s=>%s: %s\n' % (b_key, kind, b_value)
                flow_text += '%s=>end: %s\n\n' % (end_key, end_value)

                # 逻辑拼接
                body = body.replace('(y)', '(yes)').replace('(n)', '(no)')
                body = re.sub(r'([^\-])(>)', '\g<1>->', body)
                body = re.sub(r'\s*->\s*', '->', body)
                body = re.sub(r'\s+[\r\n]', '\n', body)
                flow_text += body


    # 组装成js脚本
    content_md5 = md5(text)
    dom_id = 'Z%s' % shortuuid.uuid()
    flow_text = flow_text.replace('\n', '\\n').replace("'", "\\'") #.replace("(", "\('").replace(")", "\)")
    script_text = u"""
    <div id="%s" class="flow-graphic" content_id="%s"> </div>
    <script>
    var diagram = flowchart.parse('%s');
    diagram.drawSVG('%s');
    </script> %s
    """ % (dom_id, content_md5, flow_text, dom_id, line_char*line_chars_count)

    return script_text
