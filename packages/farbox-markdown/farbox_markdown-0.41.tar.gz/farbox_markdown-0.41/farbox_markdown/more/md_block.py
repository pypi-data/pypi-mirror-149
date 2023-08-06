#coding: utf8
from __future__ import absolute_import
import hashlib
import re
from .blocks_line_by_line import smart_unicode, smart_str, compute_markdown_blocks_line_by_line_and_split_normal


line_char = u'\uffff'

def md5(text):
    text = smart_str(text)
    return hashlib.md5(text).hexdigest()


def rreplace(s, old, new):
    try:
        place = s.rindex(old)
        return ''.join((s[:place],new,s[place+len(old):]))
    except ValueError:
        return s


def get_md_blocks_info(content):
    block_ids_map = {}
    block_ids = []
    content = smart_unicode(content)
    blocks = compute_markdown_blocks_line_by_line_and_split_normal(content)
    block_type_counter = {}
    block_text_md5_counter = {}
    for block in blocks:
        block_range, block_type, block_text = block
        block_type_index = block_type_counter.get(block_type, 0)


        block_text_md5 = md5(block_text.strip('\n'))
        old_md5_counter = block_text_md5_counter.get(block_text_md5, 0)
        new_md5_counter = old_md5_counter + 1
        block_text_md5_counter[block_text_md5] = new_md5_counter

        dom_id = '%s_%s_%s' % (block_text_md5, block_type, new_md5_counter)
        #dom_id = md5(dom_id)

        # at last
        block_type_counter[block_type] = block_type_index+1

        block.append(dom_id) # block_range, block_type, block_text, block_id
        block_ids_map[dom_id] = block
        block_ids.append(dom_id)

    # block_range, block_type, block_text, block_id

    info = dict(
        blocks = blocks,
        block_ids_map = block_ids_map,
        block_ids = block_ids,
    )

    return info




def wrap_normal_block_html_with_context(block_id,  html_content, blocks_info):
    block_ids = blocks_info['block_ids']
    block_ids_map = blocks_info['block_ids_map']
    block = block_ids_map[block_id] # # block_range, block_type, block_text, block_id
    block_type = block[1]
    block_text = block[2]
    next_block_id = None
    if block_type == 'normal':
        try:
            block_index = block_ids.index(block_id)
            next_block_index = block_index+1
            next_block_id = block_ids[next_block_index]
        except:
            pass

    if next_block_id is not None:
        next_block = block_ids_map[next_block_id]
        next_block_type = next_block[1]
        next_block_text = next_block[2]
        if next_block_type in ['list', 'blockquote', 'code_block']:
            if block_text.replace(line_char, '').strip()[-1] in [':', u'：']:
                opening_class_name = 'md_block_as_opening'
            else:
                opening_class_name = ''
            if next_block_type == 'list':
                if re.match(r'\s*\d', next_block_text):
                    next_dom_name = 'ol'
                else:
                    next_dom_name = 'ul'
            else:
                next_dom_name = next_block_type
            new_p_head = '<p class="md_block %s md_has_block_below md_has_block_below_%s">' % (opening_class_name, next_dom_name)
            html_content = rreplace(html_content, '<p class="md_block">', new_p_head)
    return html_content


def collect_sub_html_blocks(data_obj, blocks_info, block_range, html_content):
    if not isinstance(data_obj, dict):
        return
    if not html_content:
        return
    blocks = blocks_info['blocks']
    start_position, block_length = block_range
    hit_block = match_in_ranges(blocks, value=start_position, hit_range_first_item=True, is_rng_length=True)
    if not hit_block:
        return
    block_id = hit_block[-1]

    html_content = wrap_normal_block_html_with_context(block_id, html_content, blocks_info=blocks_info)

    data_obj.setdefault(block_id, []).append(html_content)

    return block_id





def get_md_block_section_css_class_name(inner_html):
    inner_html = inner_html.strip()
    class_name = 'md_block_section'
    if inner_html.startswith('<'):
        class_name_c = re.search(r'^<([a-z0-9]+)', inner_html, re.I)
        if class_name_c:
            class_name_for = class_name_c.groups()[0]
            class_name += ' md_block_section_for_%s' % class_name_for
        if 'class="flow-graphic"' in inner_html:
            class_name += ' md_block_section_for_flow_graphic'
    return class_name


def get_wrap_html_for_section(dom_id, inner_html):
    wrap_html = '<section id="%s" class="%s">%s</section>' % (dom_id, get_md_block_section_css_class_name(inner_html), inner_html)
    return wrap_html



def get_wrap_html_for_markdown_render(html_blocks):
    if not isinstance(html_blocks, dict):
        return ''
    wrap_html_list = []
    for dom_id, html_content_list in html_blocks.items():
        inner_html = '\n'.join(html_content_list)
        wrap_html = get_wrap_html_for_section(dom_id, inner_html)
        wrap_html_list.append(wrap_html)
    final_wrap_html = '\n\n'.join(wrap_html_list)
    return final_wrap_html







# copy from macpy.utils.lazy
def match_in_ranges(ranges, value, hit_range_first_item=False, return_index=False, is_rng_length=False):
    # 利用二分法, 在一个 ([1, 2], [7,19], .etc) 中命中一个 指定的 value, 比如 [18]
    # end 是不包括的
    if not ranges:
        if return_index:
            return None, None
        else:
            return None
    low = 0
    high = len(ranges)-1
    tried = 0

    while low < high:
        tried += 1
        mid = int((low+high)/2)
        mid_obj = ranges[mid]
        if hit_range_first_item:
            start, end = mid_obj[0]
        else:
            start, end = mid_obj
        if is_rng_length:
            end = start+end-1
        if end >= value >= start:
            #print tried
            if return_index:
                return mid, mid_obj
            else:
                return mid_obj
        elif value > end:
            low = mid + 1
        else: # ip < start
            high = mid - 1

    # 还剩最后一次的匹配可能
    if low == high and ranges:
        mid_obj = ranges[high]
        if hit_range_first_item:
            start, end = mid_obj[0]
        else:
            start, end = mid_obj
        if is_rng_length:
            end = start+end-1
        if end >= value >= start:
            if return_index:
                return high, mid_obj
            else:
                return mid_obj

    #print tried
    if return_index:
        return None, None
    else:
        return None