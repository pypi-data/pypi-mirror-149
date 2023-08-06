#coding: utf8
import re
from farbox_markdown.zrey_utils import smart_unicode

def get_link_title_id_in_wiki_syntax(line):
    # 已经去除头尾的 [[ 与 ]] 了
    # 要考虑有多个 | ，多个 # 的情况...
    # get_link_title_id_in_wiki_syntax("hello")
    # get_link_title_id_in_wiki_syntax("hello | title #id")
    # get_link_title_id_in_wiki_syntax("hello #id |title")
    # get_link_title_id_in_wiki_syntax("hello #more |title # id | title2")
    line = smart_unicode(line.strip())
    if line.startswith("#"):
        line = line[1:]
        is_tag = True
    else:
        is_tag = False
    link_id_c = re.search("#([^#|]+)(\||$)", line)
    if link_id_c:
        link_id = link_id_c.group(1).strip()
    else:
        link_id = ""
    link_title_c = re.search("\|([^#|]+)(#|$)", line)
    if link_title_c:
        link_title = link_title_c.group(1).strip()
    else:
        link_title = ""
    link_parts = re.split("[#|]", line)
    if link_parts:
        link = link_parts[0].strip()
    else:
        link = ""
    if is_tag:
        link = "#" + link
    return link, link_title, link_id



def compile_markdown_wiki_link_syntax(line):
    if "[[" not in line or "]]" not in line:
        return line
    matches = re.finditer("(?<!\[)((\[\[)([^\[\]]+)(\]\]))", line)
    for m in matches:
        full_link_text = m.group(1)
        pure_link_text = m.group(3)
        link, link_title, link_id = get_link_title_id_in_wiki_syntax(pure_link_text)
        if not link_title:
            link_title = link.lstrip("#")
        if link.startswith("#"): # tag
            url = "/__wiki_tag/%s?type=wiki_link"%link[1:]
        else:
            url = "/__wiki_link/%s?type=wiki_link&name=%s" % (link.lstrip("/"), link_title)
            if link_id:
                url = "%s&hash=%s#%s" % (url, link_id, link_id)
        wiki_link_html = '<a href="%s" class="md_wikilink">%s</a>' % (url, link_title)
        line = line.replace(full_link_text, wiki_link_html, 1)
    return line



