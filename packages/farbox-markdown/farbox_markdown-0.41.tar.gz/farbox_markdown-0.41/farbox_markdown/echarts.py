# coding: utf8
import re, shortuuid
from collections import OrderedDict
import os

line_char = u'\uffff'

name_c = re.compile(u'[\(\uff08][^\\\(\)\uff08\uff09]+[\)\uff09]$')


def auto_number(s):
    s = s.replace(line_char, '')
    if '.' in s:
        try: return float(s)
        except: return 0.
    else:
        try: return int(s)
        except: return 0


def auto_name(name):
    # return name, stack_name
    name = name.strip()
    stack_name = ''
    stack_c = name_c.search(name)
    if stack_c:
        raw_stack_name = stack_c.group()
        stack_name = raw_stack_name[1:-1]
        name = name[:-len(raw_stack_name)].strip()
    return name, stack_name

def auto_echarts_html(html):
    if os.environ.get('echarts_animation', 'true') in ['false']:
        # 禁用 echart 的动画
        html = html.replace('animation: true,', 'animation: false,', 1)
    return html


"""
'#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                        '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                        '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
"""

default_echarts_color_list = ['#18A67A', '#E14B78',  '#3B8FBD', '#FAB432','#4D79B9', '#92C6AE',
                               '#AD314D', '#F7A63F', '#41B882', '#D28268',
                              '#395DAD', '#1B9FCF'
                              ]

def get_echarts_color_list(as_string=False):
    color_list = []
    color_list_in_env = os.environ.get('echarts_color_list', '')
    raw_color_list = re.split(' |,', color_list_in_env)
    for color in raw_color_list:
        color = color.strip()
        if color:
            color_list.append(color)
    color_list = color_list or default_echarts_color_list
    if as_string:
        color_list = "['%s']" % "','".join(color_list)
    return color_list



def get_echarts_color_for_item():
    # 主要是单个 bar, 每一列都赋予不同的颜色
    raw_color_list_content = get_echarts_color_list(as_string=True)
    color_list_content = """
    ,itemStyle: {
                normal: {
                    color: function(params) {
                        var colorList = %s;
                        return colorList[params.dataIndex%%colorList.length]
                    }
                }
            }
    """ % raw_color_list_content
    return color_list_content




def create_axis_with_data(data_s, boundary_gap=True):
    # 根据指定的 data 的字符串, 获得 x & y 轴的设定
    template = """
    xAxis: {
        boundaryGap: %s,
        data: %s,
        axisLine:{
            lineStyle:{
                color: '%s'
            }
        },
        axisLabel:{
            color: '%s',
            interval:0
        },
        splitLine:{
            lineStyle: {
                color: '%s'
            }
        },
    },
    yAxis:{
        axisLine:{
            lineStyle:{
                color: '%s'
            }
        },
        axisLabel:{
            color: '%s'
        },
        splitLine:{
            lineStyle: {
                color: '%s'
            }
        },
    },
    """
    line_color = os.environ.get('echarts_line_color') or '#ccc'
    label_color = os.environ.get('echarts_line_label_color') or '#555'
    split_line_color = os.environ.get('echarts_split_line_color') or '#f0f0f0'
    boundary_gap = 'true' if boundary_gap else 'false'
    content_to_return = template % (boundary_gap, data_s,
                                    line_color, label_color, split_line_color,
                                    line_color, label_color, split_line_color)
    return content_to_return



def create_legend(ys=None, items=None):
    js_content = ''
    items = items or []
    if ys and not items and len(ys)>2:
        items = ys[1:]
    if items and len(set(items))>1: # 这里会去重
        y_names = [name_c.sub('', name) for name in items]
        y_names_s = '["%s"]' % '" , "'.join(y_names)
        js_content = u"""
        legend: {
                data: %s
            },
        """ % y_names_s
    return js_content.strip()



def create_dict_data(names, values):
    # 生成 js 的 data list，里面每个都是name, value 的形式
    if len(names) != len(values):
        data = ''
    else:
        data_list = []
        for i, name in enumerate(names):
            value = values[i]
            data_list.append(u'{value:%s, name:"%s"}' % (value, name))
        data = ','.join(data_list)
    return 'data: [%s]' % data




def create_container_dom_html():
    dom_id = 'Z%s' % shortuuid.uuid()
    html = u'<!--md_echarts--><div class="md_echarts" id="%s" style="width:100%%;min-width: 600px;height:400px;"></div>' % dom_id
    return dom_id, html



######################  bar starts #########################

def create_one_bar_series(values, name='_', series_count=1):
    name, stack_name = auto_name(name)
    values_s = '[%s]' % ','.join(values)
    js_content = """
    {
        name: '%s',
        type: 'bar',
        data: %s
        %s
    }
    """ % (name, values_s, get_echarts_color_for_item() if series_count==1 else '')
    js_content = js_content.strip()
    if stack_name:
        js_content = '{' +  'stack: "%s",'%stack_name + js_content[1:]
    return js_content


def create_bar_series(series, values):
    js_contents = []
    for i, name in enumerate(series):
        try: sub_values = values[i]
        except: continue
        js_contents.append(create_one_bar_series(sub_values, name, series_count=len(series)))
    series_js_content = 'series:[ %s ]' % ','.join(js_contents)
    return series_js_content


def create_bar_table_js_content(items, values, series=None):
    series = series or items

    # 先得到横x坐标的 data
    xs_s = '["%s"]' % '","'.join(items)
    series_content = create_bar_series(series, values)
    dom_id, html = create_container_dom_html()
    html += u"""
    <!--js_run_it--><script type="text/javascript">
    var my_chart = echarts.init(document.getElementById('%s'));
    var option = {
        animation: true,
        color: %s,
        tooltip : {
            trigger: 'axis'
        },
        %s
        %s
        %s
    };
    my_chart.setOption(option);
    </script>
    """ % (dom_id,
           get_echarts_color_list(as_string=True),
           create_axis_with_data(xs_s),
           create_legend(items=series),
           series_content)
    return auto_echarts_html(html)


def create_bar_table(xs, value_parts, ys=None):
    if not value_parts:
        return ''

    # bar table 是无始 value_parts 的，都会叠加在一起
    value_part = []
    for v in value_parts:
        value_part += v

    values = []
    if len(xs) == 1 and ys and len(ys)>2: # 纵向，基本上忽略第一行的声明
        items = ys[1:]
        for row in value_parts[0]:
            if row: values.append(row[0])
        series = [xs[0]]
        values = [values]
    else:
        items = xs[:]
        for v in value_parts:
            values += v
        if not ys:
            # 纯一维
            series = ['Value']
        else:
            series = ys[1:]

    html = create_bar_table_js_content(items, values, series)

    return html

######################  bar ends #########################







######################  line starts #########################


def create_one_line_series(values, name='_'):
    name, stack_name = auto_name(name)
    values_s = '[%s]' % ','.join(values)
    js_content = """
    {
        name: '%s',
        type: 'line',
        areaStyle: {normal: {}},
        data: %s
    }
    """ % (name, values_s)
    js_content = js_content.strip()
    if stack_name:
        js_content = '{' +  'stack: "%s",'%stack_name + js_content[1:]
    return js_content


def create_line_series(series, values):
    js_contents = []
    for i, name in enumerate(series):
        try: sub_values = values[i]
        except: continue
        js_contents.append(create_one_line_series(sub_values, name))
    series_js_content = 'series:[ %s ]' % ','.join(js_contents)
    return series_js_content



def create_line_table_js_content(items, values, series=None):
    series = series or items
    # 先得到横x坐标的 data
    xs_s = '["%s"]' % '","'.join(items)
    series_content = create_line_series(series, values)
    dom_id, html = create_container_dom_html()
    html += u"""
    <!--js_run_it--><script type="text/javascript">
    var my_chart = echarts.init(document.getElementById('%s'));
    var option = {
        animation: true,
        color: %s,
        tooltip : {
            trigger: 'axis'
        },
        grid: {
            left: '3%%',
            right: '4%%',
            bottom: '3%%',
            containLabel: true
        },
        %s
        %s
        %s
    };
    my_chart.setOption(option);
    </script>
    """ % (dom_id,
           get_echarts_color_list(as_string=True),
           create_axis_with_data(xs_s, boundary_gap=False),
           create_legend(items=series),
           series_content)
    return auto_echarts_html(html)


def create_line_table(xs, value_parts, ys=None):
    if not value_parts:
        return ''

    # bar table 是无始 value_parts 的，都会叠加在一起
    value_part = []
    for v in value_parts:
        value_part += v

    values = []
    if len(xs) == 1 and ys and len(ys)>2 and not re.match(r'\(.*?\)$', ys[0].strip()): # 纵向，基本上忽略第一行的声明
        items = ys[1:]
        for row in value_parts[0]:
            if row: values.append(row[0])
        series = [xs[0]]
        values = [values]
    else: # 横向
        items = xs[:]
        for value_part in value_parts:
            for row in value_part:
                values.append(row)
        if not ys:
            # 纯一维, 但可能是多条线
            series = ['Value'] * len(values)
        else:
            series = ys[1:]

    html = create_line_table_js_content(items, values, series)

    return html



######################  line ends #########################









######################  pie starts #########################


def create_one_pie_series(names, values, radius="'55%'", name='_', core=False):
    # '55%' 单圆； "[0, '30%']" 扇形
    data_s = create_dict_data(names, values)
    if core:
        # 双层 pie 的核心
        core_label = """
        label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
        """
    else:
        core_label = ''
    js_content = """
    {
        name: '%s',
        type: 'pie',
        radius : %s,
        %s
        %s,
        itemStyle: {
            emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
        }
    }
    """ % (name, radius, core_label, data_s)
    js_content = js_content.strip()
    return js_content


def create_pie_series(stack_names, stack_values, names, values, ys=None):
    js_contents = []
    if ys and len(ys) - len(names) ==1: # 两维，可以取得 name
        name = ys[0]
    else:
        name = ''
    if stack_names and stack_values:
        # 两层
        stack_js_content = create_one_pie_series(stack_names, stack_values, radius="[0, '30%']", core=True, name=name)
        normal_js_content = create_one_pie_series(names, values, radius="['40%', '55%']", name=name)
        js_contents = [stack_js_content, normal_js_content]
    else: # 单层，园 or 扇形，如何处理？
        js_contents.append(create_one_pie_series(names, values, radius="'55%'", name=name))
        pass
    series_js_content = 'series:[ %s ]' % ','.join(js_contents)
    return series_js_content



def create_pie_table_js_content(stack_names, stack_values, names, values, ys=None):
    series_content = create_pie_series(stack_names, stack_values, names, values, ys)
    dom_id, html = create_container_dom_html()
    html += u"""
    <!--js_run_it--><script type="text/javascript">
    var my_chart = echarts.init(document.getElementById('%s'));
    var option = {
        animation: true,
        color: %s,
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%%)"
        },
        %s
        %s
    };
    my_chart.setOption(option);
    </script>
    """ % (dom_id,
           get_echarts_color_list(as_string=True),
           create_legend(ys),
           series_content)
    return auto_echarts_html(html)


def create_pie_table(xs, value_parts, ys=None):
    if not value_parts:
        return ''
    items = []
    values = []
    if len(xs) == 1 and ys and len(ys)>2: # 纵排
        items = ys[1:]
        for row in value_parts[0]:
            if row: values.append(row[0])
    elif not ys and len(xs)>1: # 横排
        items = xs
        values = value_parts[0][0]
    if not items or not values:
        return ''
    if len(items) != len(values):
        return ''

    # 不能用 dict，可能有重复的 name
    # 萃取汇总的内容
    raw_stack_data_dict = OrderedDict() # name: [indexes]
    names = []
    stacked = False
    for i, name in enumerate(items):
        name, stack_name = auto_name(name)
        names.append(name)
        if stack_name:
            raw_stack_data_dict.setdefault(stack_name, []).append(i)
            stacked = True
        else:
            # 当前属于单独一类，即本身
            raw_stack_data_dict.setdefault(name, []).append(i)

    stack_names = []
    stack_values = []
    if stacked:
        for stack_name, indexes in raw_stack_data_dict.items():
            value = 0
            for index in indexes:
                value += auto_number(values[index])
            stack_names.append(stack_name)
            stack_values.append(str(value))

    html = create_pie_table_js_content(stack_names, stack_values, names, values, ys)
    return html



######################  bar ends #########################