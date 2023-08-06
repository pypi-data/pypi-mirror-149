#coding: utf8
from __future__ import absolute_import
import sys, os, re

is_win = sys.platform == 'win32'

def same_slash(path):
    if path:
        path = path.replace('\\', '/')
        path = path.rstrip('/')
    return path


def get_relative_path(filepath, root, return_name_if_fail=True):
    filepath = same_slash(filepath)
    root = same_slash(root)
    if filepath and root and filepath.startswith(root+'/'):
        return filepath.replace(root, '').strip('/')
    else:
        if return_name_if_fail:
            return os.path.split(filepath)[-1]
        else:
            return filepath



##### image related starts
def fix_relative_image_path(path, content, root=None):
    #自动补足img的src, 但不会处理本地的协议，比如file://这个 ;  path 实际上 markdown 的文件路径
    # prefix 由 path 决定，本地的 path 会形成本地的 prefix，服务端的则一般过来相对（站点目录）地址
    # path 如果是本地的全路径，这里的 prefix 实际上是一个 post 路径的父目录路径; 如果 post_path 是/开头的，则是为 web 端 url 服务的
    # relative_prefix 则是以 / 开头的路径补足，一般为 web 端 url 服务的, 但仅仅是针对本地的解析（有 root 指定的）
    if '/' not in path.lstrip('/'):
        prefix = '/'
    else:
        prefix = path.rsplit('/', 1)[0] #前缀为md文件的父目录
        prefix = '/%s/' % prefix.strip('/').replace('//', '/') # windows下全路径，会得到/c:/类似的路径， 多了个/开头

    if root:
        # 这个是要在web类非本地请求的时候需要用到, 做成本地、远程两套兼容的补全
        relative_post_path = get_relative_path(path, root)
        if '/' not in relative_post_path: # 根目录
            relative_prefix = '/'
        else:
            relative_prefix = relative_post_path.rsplit('/', 1)[0]
            relative_prefix = '/%s/' % relative_prefix.strip('/').replace('//', '/')

        if is_win:
            content = content.replace('<img src="@/', '<img src="file:///%s/'%root, 1)
        else:
            content = content.replace('<img src="@/', '<img src="file://%s/'%root, 1)
    else:
        relative_prefix = ''
        content = content.replace('<img src="@/', '<img src="/', 1)


    # 非http:// & https://这种开头的 非/开头的，认为是错误的图片地址， 进而进行路径的补全
    # 1, <img  2, src="  3, ./(可有可无) 4, 图片路径(非 web，非/开头) 5, "
    bad_img_pat = re.compile(r"""(<img)([^<]*?src=['"])(?!/|http://|https://|file://|ftp://|data:image)(\./)?([^<]*?)(['"])""", re.I)
    # (\./)? 目的是去掉一个无意义的相对路径, -> 3

    if not relative_prefix:
        content = bad_img_pat.sub('\g<1>\g<2>%s\g<4>\g<5>' % prefix, content)
    else: # 必定有 root 的情况下  # double image src for fallback
        # prefix 实际指向本地，它作为fallback, 当 web 的 url 无法访问的时候，本地的 file 地址就会起作用
        if os.path.isdir(prefix.lstrip('/') if is_win else prefix): # prefix 本身是一个目录
            prefix = 'file://'+ prefix
        content = bad_img_pat.sub("""\g<1> onerror="this.src='%s\g<4>';this.onerror=null;" \g<2>%s\g<4>\g<5>"""%(prefix, relative_prefix), content)

    # '/users/hepochen/farbox/hello.txt' --> '_image/hello'
    image_for_post_path = '_image/%s' % os.path.splitext(os.path.split(path)[-1])[0]
    # /~/ 替换为 /_image/xxxxx/
    relative_image_path_c = re.compile(r"""(<img[^<]*?src=['"]/?[^<>]*?)(?:/~/|/%7E/)([^<]*?>)""", re.I)
    content = relative_image_path_c.sub('\g<1>/%s/\g<2>'% image_for_post_path, content)
    return content


def fix_images_in_markdown(path, content, root=None, for_local=False):
    # 对图片的一些特殊处理（在HTML中），缩放 & 路径补全
    content = fix_relative_image_path(path, content, root=root)
    # 图片的缩放写成style
    scaled_img_pat = re.compile(r"""(<img[^<]*? )(src=['"](.*)(\?r=)(\d+)['"])([^<]*?>)""", re.I)
    content = scaled_img_pat.sub('\g<1>src="\g<3>" style="width:\g<5>%" class="md_scaled_image" \g<6>', content)

    if path and root and for_local: # 给本地使用的情况, 比如 preview 的时候
        # 以/开头的图片地址，因为是本地无法读取的; 而 md compiler 中也不会做补全(用 error 的方式)
        image_prefix_c = re.compile(r"""(<img[^<]*?src=['"])(/[^<]*?['"])""", re.I)
        image_prefix = ('file:///' if is_win else 'file://') + root
        image_prefix = image_prefix.strip('/') # 可能本身有正则的敏感字符，比如含有.\1\2之类的，需要脱敏处理
        try:
            content = image_prefix_c.sub('\g<1>$$md_local_image_prefix$$\g<2>', content)
            content = content.replace('$$md_local_image_prefix$$', image_prefix)
        except:
            pass
        return content

    return content

##### image related ends
