#coding: utf8
from __future__ import absolute_import
from farbox_markdown.zrey_utils import smart_unicode, smart_str
from ..meta import yaml_pat as re_yaml_pat, meta_pat as re_simple_meta_pat
import re


def get_indent_in_text(text):
    # 一个 line text 上的左侧空格、\t 转为 indent(整数)
    if text.startswith(' ') or text.startswith('\t'):
        indents = len(re.search('^[ \t]+', text).group())
        indents += text.count('\t') * 3
    else:
        indents = 0
    return indents


k_v_re_pat = re.compile(u'^(\w+)[:\uff1a](.*?)$', re.M)


def is_list_item_line(line):
    if re.match('[\t ]*(\* |- |\d+\. )', line):
        if line.startswith('- -'): # 分割线的语法
            return False
        return True
    else:
        return False


def is_pure_list_text(text):
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line and not is_list_item_line(line):
            return False
    return True # by default

def is_blockquote_line(line):
    if re.match('[ \t]*>', line):
        return True
    else:
        return False

def is_header_line(line): # h1 ~ h6
    if re.match(r'#+.*?$', line):
        return True
    else:
        return False


def is_code_block_border_line(line):
    # code block 的头尾都进行匹配的逻辑
    #if re.match('```([^`]|$)', line):
    if re.match(r'```([a-z0-9\-+_:#]+\s*$|$)', line, flags=re.I):
        return True
    else:
        return False



def is_split_line(line):
    if not line:
        return False
    if line.endswith('\n'):
        line = line[:-1]
    if '\n' in line:
        return False
    matched = re.match(r'\s*-?(- ){2,}-[- ]*\s*$', line) or re.match(r'\s*(\* ){2,}\*[* ]*\s*$', line)\
                or re.match(r'\s*\*{3}[* ]*\s*$', line) or re.match(r'\s*\-{6}[- ]*\s*$', line)
    if matched:
        return True
    else:
        return False


def is_yaml_header(header_content):
    # 一个内容, 是否是严格符合 yaml header 的头部声明的
    if re.match('---\n.*?\n---\n?$', header_content, flags=re.S):
        return True
    else:
        return False


def is_simple_kv_line(line, is_first_line=False):
    if k_v_re_pat.match(line):
        if is_first_line:
            if re.match('https?://', line, flags=re.I): # just url
                return False
        return True
    else:
        return False


def get_line_type_for_normal_like_line(line, auto_remove_n=True):
    # 非 block 声明的, 也没有 position 的要求, 从单 line 推断出当前的类型
    if auto_remove_n and line.endswith('\n'):
        line = line[:-1]
    if is_list_item_line(line):
        return 'list'
    if is_blockquote_line(line):
        return 'blockquote'
    if is_header_line(line):
        return 'header'
    return 'normal'




def get_yaml_header(raw_content, return_range=False):
    raw_content = smart_unicode(raw_content)
    match = re_yaml_pat.match(raw_content)
    if match:
        header_content = match.group(1)
        if return_range:
            return [0, len(header_content)]
        else:
            return header_content
    else:
        return None


def get_simple_header(raw_content, return_range=False):
    raw_content = smart_unicode(raw_content)
    match = re_simple_meta_pat.match(raw_content)
    if match:
        header_content = match.group(1)
        if re.match(r'https?://', header_content, flags=re.I):
            return None
        if return_range:
            return [0, len(header_content)]
        else:
            return header_content
    else:
        return None



class MarkdownBlocksComputer(object):
    def __init__(self, raw_content, position_offset=0, try_header=True, for_gui=False):
        self.for_gui = for_gui
        self.raw_content = smart_unicode(raw_content)
        self.lines = self.raw_content.split('\n')
        self.last_i = len(self.lines) - 1
        self.start_position = position_offset
        self.pre_position_length = 0
        self.position_length = 0 # 表示尝试 block 计算的时候，当前 0 position 开始， 多少长度使用了；如果一个全新的 block，其必然 == 0
        self.blocks_result = [] # element is like (rng, status)
        self.status = 'normal'
        self.try_header = try_header

        self.has_auto_last_block = False

        self.current_indent = 0
        self.block_indent = 0


    def reset(self):
        self.status = 'normal'
        self.pre_position_length = 0
        self.position_length = 0


    def set_status_by_current_line(self, status):
        # 因为当前行的原因, 而获得了一个 status,
        if status != self.status and self.pre_position_length:
            # self.pre_position_length 是指不计算当前 line 之前的状态
            # 要将之前的行, 作为一个 block, 其逻辑存储起来
            self.add_as_block(status=self.status, includes_current_line=False)
        self.status = status


    def add_as_block(self, status=None, includes_current_line=False):
        if status is None:
            status = self.status
        if includes_current_line:
            rng = [self.start_position, self.position_length]
            diff = 0
        else:
            # 不包括当前行, 但是行的长度已经计算, 会有个 diff 产生, reset 之后, 赋予 self.position_length
            rng = [self.start_position, self.pre_position_length]
            diff = self.position_length - self.pre_position_length
        if not rng[1]:
            return # ignore
        self.blocks_result.append([tuple(rng), status])
        self.start_position = sum(rng)
        self.reset()
        self.position_length = diff


    def compute_one_line(self, line_index, line_text):
        old_status = self.status
        self.current_indent = get_indent_in_text(line_text)
        result = self._compute_one_line(line_index, line_text)
        new_status = self.status
        if new_status != old_status:
            self.block_indent = self.current_indent
        return result

    def _compute_one_line(self, line_index, line_text):
        i = line_index
        line = line_text
        line_length = len(line)
        if i == self.last_i:
            length_increased = line_length
        else:
            length_increased = line_length + 1
        self.pre_position_length = self.position_length
        self.position_length += length_increased

        if self.status == 'list':
            # 已经是 list 内的，除了提交 block 之外, 当前行仍然会参与后续的逻辑
            if not is_list_item_line(line):  # 已经不是 list 了
                if not self.for_gui and self.current_indent >= self.block_indent + 4:
                    return 'continue'
                if line:
                    self.add_as_block()
                elif not line and i == line_length - 1:  # 最后一行, 虽然也是空行, 但是进行 list 的提交
                    self.add_as_block()
                    return 'continue'
                else:
                    # 空行, 继续下去, 保留 status=list
                    return 'continue'
            else:  # 仍然是 list 内的
                return 'continue'

        if i == 0 and line.startswith('---') and line.rstrip(' ') == '---' and self.try_header:
            self.status = 'yaml_header'
            return 'continue'
        elif self.status == 'yaml_header':
            if line.rstrip(' ') == '---':
                self.add_as_block(includes_current_line=True)
            return 'continue'

        if i == 0 and is_simple_kv_line(line, is_first_line=True) and self.try_header:  # simple header
            self.status = 'simple_header'
            return 'continue'
        elif i != 0 and self.status == 'simple_header':
            if line and not is_simple_kv_line(line):
                # 已经跳出 simple header, 但是当前行会仍然执行下去
                self.add_as_block()
                # if not line.strip():
                #    continue
                # else:
            else:
                # simple header 内的
                return 'continue'

        # code block
        if self.status != 'code_block' and re.match('\s*```([^`]|$)', line):
            self.set_status_by_current_line('code_block')
            return 'continue'
        elif self.status == 'code_block':
            if re.match('\s*```\s*$', line):
                self.add_as_block(includes_current_line=True)
            return 'continue'

        # blockquote
        if self.status != 'blockquote' and is_blockquote_line(line):
            self.set_status_by_current_line('blockquote')
            return 'continue'
        elif self.status == 'blockquote':
            if not is_blockquote_line(line):  # 严谨的 blockquote
                self.add_as_block(includes_current_line=False)
                #self.status = 'normal'
                return 'retry'
            return 'continue'

        # list
        if self.status != 'list' and is_list_item_line(line):
            self.set_status_by_current_line('list')
            return 'continue'

        # header
        if self.status == 'normal' and is_header_line(line):
            self.set_status_by_current_line('header')
            self.add_as_block(includes_current_line=True)
            return 'continue'


    def compute(self):
        lines_length = len(self.lines)
        for i, line  in enumerate(self.lines):
            next_operation = self.compute_one_line(i, line)
            if next_operation == 'continue':
                continue
            elif next_operation == 'retry':
                self.position_length = 0
                # 当前行起到了状态截断的作用，重新计算
                self.compute_one_line(i, line)

        # at last, as the last block
        if self.position_length:
            self.add_as_block(includes_current_line=True)
            self.has_auto_last_block = True

        return self.blocks_result



def compute_markdown_blocks_line_by_line(content, position_offset=0, for_gui=False):
    # [(rng, block_type), (rng, block_type), .etc]
    content = smart_unicode(content)
    computer = MarkdownBlocksComputer(content, position_offset=position_offset, for_gui=for_gui)
    blocks_result = computer.compute()
    if not blocks_result:
        return blocks_result

    last_block = blocks_result[-1]
    last_block_rng, last_block_type = last_block
    if last_block_type in ['code_block', 'yaml_header'] and computer.has_auto_last_block:
        position, position_length = last_block_rng
        last_block_content = content[position: position+position_length]
        should_re_compute_last_block = False
        if last_block_type == 'code_block' and not re.search('\n```\s*$', last_block_content):
            should_re_compute_last_block = True
        elif last_block_type == 'yaml_header' and not re.search('\n---\n?$', last_block_content):
            should_re_compute_last_block = True
        if should_re_compute_last_block and '\n' in last_block_content:
            # 没有正常闭合的
            first_block_type = last_block_type
            if first_block_type == 'yaml_header':
                # yaml header 没有闭合的, 就是普通的状态
                first_block_type = 'normal'
            first_line, rest_content = last_block_content.split('\n', 1)
            first_line += '\n'
            first_line_length = len(first_line)
            first_line_rng = [position, first_line_length]
            first_line_block = [first_line_rng, first_block_type]
            blocks_result[-1] = first_line_block
            rest_position_offset =  sum(first_line_rng)
            reset_computer = MarkdownBlocksComputer(rest_content, position_offset=rest_position_offset, try_header=False, for_gui=for_gui)
            blocks_result += reset_computer.compute()

    return blocks_result





########### blocks 的重新计算逻辑 starts ##########

def split_normal_block(block_data):
    block_range, block_type, block_text = block_data
    should_split = False
    positions = [0]
    for match in re.finditer(r'\n{2,}', block_text):
        positions.append(match.end())
        should_split = True
    if not should_split: # 不需要分割
        return [block_data]
    else:
        blocks = []
        positions.append(len(block_text)) # 补全所有的 positions
        block_start, block_length = block_range
        for i in range(len(positions)-1):
            start, end = positions[i], positions[i+1]
            part_length = end - start
            part_text = block_text[start:end]
            part_text_stripped = re.sub(r'<!--[^<>]*-->', '', part_text).strip()
            if not part_text_stripped:
                continue
            part_range = [block_start+start, part_length]
            blocks.append([
                part_range,
                block_type,
                part_text
            ])
        return blocks


def compute_markdown_blocks_line_by_line_and_split_normal(content):
    # 对 normal 的进一步分割成更多的 cell
    content = smart_unicode(content)
    raw_blocks = compute_markdown_blocks_line_by_line(content)
    blocks = []
    for block_range, block_type in raw_blocks:
        start, length = block_range
        block_text = content[start: start+length]
        block_text_stripped = re.sub(r'<!--[^<>]*-->', '', block_text).strip()
        if not block_text_stripped:
            continue
        block_data = [block_range, block_type, block_text]
        if block_type != 'normal':
            blocks.append(block_data)
        else:
            blocks += split_normal_block(block_data)
    return blocks


########### blocks 的重新计算逻辑 ends ##########
