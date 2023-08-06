#coding: utf8
from __future__ import absolute_import
from farbox_markdown.compile_md import compile_markdown
import time


raw_content = u"""# MarkEditor的Markdown语法
>  Markdown是非常棒以及流行的写作语法，平文本，「易读易写」，一般只需几分钟就能学会Markdown的基本用法。

## 标题:
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
分别对应HTML中的`<h1>一级标题</h1>`，以此类推。

**用两个星号标记起来，表示加粗**，*一个星号，表示斜体*，~~这样子表示删除~~，这些就是最基本的语法了。


## 插入链接
**插入链接:**
这是一个 [链接](http://url.com/)

**快速链接:**
只需要在网址头尾用尖括号包裹即可，比如<http://url.com>

**邮箱链接:**
这是一个 <myname@example.com> 邮箱的链接。

**MarkEditor特别支持:**
[Google (target=_blank id=google_link)](google.com)  其中内容括号内的`target=_blank id=google_link` 会自动扩展到最终 HTML 对应 A 标签下的属性，另外，`google.com` 作为一个域名，不需要补全`http://`, 最终会自动补全。


## 列表
无序列表:
- Red
- Green
- Blue

**有序列表则使用数字接着一个英文句点：**
1.  Bird
2.  McHale
3.  Parish

**也可以混合在一起使用:**
-   Bird
    - blue bird
-   McHale
    1.  a man
    2.  HoustonRockets
-   Parish



## 分割线
**`-`加上空格组成，三个以上:**
- - - - - -


## 样式修饰: 居中、色彩、字体大小 .etc
在当前行



## 注释
// 这是 MarkEditor 的特别支持!
/// 多了一个/，也是注释，但最终注释内容不会出现在源码中。
注释后的内容，最终会以 HTML 的注释格式`<!--我是内容-->`存在，不会显示在正文中，但包含在 HTML 的源码中；如果是`/// `开头的，则也不包括在源码中。



## 内容引用
用`>`放在段首，之后是空格，输入文字:

> 你
> 一会看我
> 一会看云

>  我觉得
>  你看我时很远
>  你看云时很近


## 插入图片
> 插入图片的语法跟插链接很像，在MarkEditor中，一般可以通过拖拽的方式进行插图，不一定会看到这个语法，而可能直接看到图片本身。

**常见的插图语法:**
![图片的alt信息，可空](图片的url)

**另一种插图语法:**
![alt text][image_id]
[image_id]: 图片的url

**MarkEditor特别支持:**
![图片的alt信息，可空](图片的url)的形式中，如果图片的 url 不是 Web 地址，而是本地的指向，则后面跟上`?r=90&w=100&h=100`，可以设定图片的尺寸。其中 r 表示缩放90%,  w 表示最大宽度 (像素)，h 表示最大高度。r、w、h 并不需要全部进行声明，按需则可。
如果是图片直接在编辑区域内可见(非 Markdown 语法显示)，双击图片，可以直接进行调整。"""

def test(times=100):
    t1 = time.time()
    for i in range(times):
        html = compile_markdown(raw_content)
    print time.time() - t1

    return html



if __name__ == '__main__':
    h = test()
    print h