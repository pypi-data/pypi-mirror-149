#coding: utf8
import datetime
from farbox_markdown.zrey_utils import smart_unicode
import re
import yaml, pyaml
from .util import string_types
#from yaml.parser import ParserError
#from yaml.scanner import ScannerError


def safe_meta(meta):  # 保证mongodb可以存储的key
    new_meta = {}
    for key in meta:
        value = meta[key]
        key = smart_unicode(key).lower()  # key全部处理为小写的
        if not re.match(r'^(?!\d)\w+$', key):
            continue
        if type(value) == datetime.date:  # date类型的，转为datetime类型的; 否则mongodb不识别
            value = datetime.datetime.combine(value, datetime.time(0, 0, 0))
        elif isinstance(value, string_types):
            value = value.strip().strip('\'"')
        new_meta[key] = value
    return new_meta


yaml_pat = re.compile("""^(?:---\s*\n)?(.*?)\n---\s*(?:\n|$)""", re.S)
meta_pat = re.compile(u'^((?:\w+[:\uff1a].*?(?:[\r\n]+|$))+)', re.S)
meta_pat_dict = re.compile(u'^(\w+)[:\uff1a](.*?)$', re.M)



cn_colon_char = u'\uff1a' # 中文

def extract_metadata(content, use_farbox_meta=False):
    # 从内容中提取 metadata 的声明内容以及属性
    # use_farbox_meta 默认为false，后续在yaml匹配失败的时候，会尝试这个方式
    raw_content = content
    content = content.strip()
    if re.match(r'\w+://', content): # 可能是网址
        return content, {}
    if use_farbox_meta:
        match = meta_pat.match(content)
    else:
        match = yaml_pat.match(content) or meta_pat.match(content) # 使用yaml or 使用FB的
    if not match:
        return content, {}
    tail = content[len(match.group(0)):]
    raw_metadata_str = match.group(1).strip()

    # 对 metadata str 中的 中文冒号的 替换
    raw_metadata_str_lines = []
    for line in raw_metadata_str.split('\n'):
        should_replace_cn_colon_char = True
        if u':' in line and cn_colon_char in line:
            en_line_index = line.index(':')
            cn_line_index = line.index(cn_colon_char)
            if cn_line_index > en_line_index:
                should_replace_cn_colon_char = False
        if should_replace_cn_colon_char:
            line = line.replace(u'\uff1a', ':', 1)
        raw_metadata_str_lines.append(line)
    raw_metadata_str = '\n'.join(raw_metadata_str_lines)


    # key value之间要有空格，不然yaml就可能读取失败
    metadata_str = re.sub('^(\w+:)(\S)', '\g<1> \g<2>', raw_metadata_str, flags=re.M)
    metadata_str = re.sub(r'\t', ' '*4, metadata_str)

    # 以转成字符串的优先 FarBox的规则
    metadata = safe_yaml(metadata_str, dict(meta_pat_dict.findall(metadata_str)))
    if metadata.get('_yaml_failed') and not use_farbox_meta: # yaml 解析失败，强制使用FarBox的规则，重来一次
        return extract_metadata(raw_content, use_farbox_meta=True)

    # 不是以---为开头的的，并且第一行中没有:
    if not re.match(r'^---', content) and ':' not in raw_metadata_str.split('\n', 1)[0]:
        return content, {}
    if not metadata: # 一般必然有，如果没有metadata，就原始数据返回
        return content, {}

    # 针对FarBox的兼容处理
    #if 'status' not in metadata and metadata.get('published', True):
    #    metadata['status'] = 'public'
    if 'url' not in metadata and ('permalink' in metadata or 'slug' in metadata):
        metadata['url'] = metadata.get('permalink', metadata.get('slug'))

    # 处理title, 可能会被当做时间来处理了 2012-12-11

    if 'title' in metadata and metadata['title'] and not isinstance(metadata['title'], string_types):
        title = smart_unicode(metadata['title'])
        title = re.sub(r'00(:|$)', '', title)
        metadata['title'] = title

    metadata['raw_metadata_str'] = raw_metadata_str

    return tail.lstrip('\r\n').rstrip(), metadata


def get_md_metadata(content):
    tail, metadata = extract_metadata(content)
    if not isinstance(metadata, dict):
        metadata = {}
    return metadata



def merge_metadata(raw_meta, extra):
    # 合并 metadata, 返回的是 unicode
    # raw_metadata 是原始的 meta 声明，extra 是一个 dict 属性的对象
    if isinstance(raw_meta, dict):
        metadata = raw_meta
    else: # 需要 compile 的
        blank_tail, metadata = extract_metadata('---\n%s\n---\n' % raw_meta)
    raw_meta = metadata.pop('raw_metadata_str', '') # 这个字段，不 merge
    metadata.update(extra) # extra 里可能有些会被清空
    metadata = {key:value for key,value in metadata.items() if value not in [None, '']}
    try:
        title = metadata.pop('title', None) # 保证 title 位于第一行
        new_meta = pyaml.dump(metadata)
        if title:
            new_meta = 'title: %s\n%s' % (title, new_meta)
        # 避免日期被字符串格式化
        new_meta = re.sub(r'((?:^|\n)date: ?)[\'"]([ -:0-9]+)[\'"]', '\g<1>\g<2>', new_meta)
    except: # pyaml　dump 失败的补救方式
        new_meta = raw_meta
        for field, value in extra.items():
            new_one = '\n%s: %s' % (field, value)
            if not re.search(r'(^|\n)%s:'%field, new_meta, re.I): # add
                new_meta += new_one
            else: # update
                new_meta = re.sub(r'(^|\n)%s:[^\n]*'%field, new_one, new_meta, count=1, flags=re.I)
    new_meta = smart_unicode(new_meta).strip()
    raw_meta = smart_unicode(raw_meta).strip()
    return new_meta, new_meta!=raw_meta # new content & updated or not


def merge_metadata_for_content(content, extra):
    clean_content, metadata = extract_metadata(content)
    if metadata.get('status') == 'public':
        metadata.pop('status', None)
    new_meta_str, updated = merge_metadata(metadata, extra)
    if updated:
        new_content = "---\n%s\n---\n\n%s" % (new_meta_str, clean_content)
        return new_content, True # updated
    else:
        return content, False



def values_not_blank(data):
    new_data = {}
    for key in data:
        value = data[key]
        if value:
            new_data[key] = value
    return new_data


def safe_yaml(strings, to_merger=None):
    try:
        meta = yaml.load(strings)
        if not isinstance(meta, dict):
            return {}
    except:
        meta = {'_yaml_failed': True}
        if to_merger and isinstance(to_merger, dict):
            string_lines = re.split(r'[\r\n]+', strings.strip())
            if len(string_lines) == len(to_merger):
                # 认为单行单个可以完全覆盖，yaml 解析不算失败
                meta.pop('_yaml_failed', None)
    # got the meta now
    if to_merger and isinstance(to_merger, dict):
        # meta = values_not_blank(meta) yaml meta 为什么要过滤掉空值?
        to_merger = values_not_blank(to_merger) # to_merger中的都是字符串， 所以要去空
        for key in to_merger:
            if key not in meta or meta.get(key) is None:
                meta[key] = to_merger[key]  # 补缺
    return safe_meta(meta)


