class Ops:
    """
    show_null:
        输入data返回空值比例的柱形图
    例：show_null(data)

    show_null_int:
        输入data返回以0为空值的柱形图
    例：show_null_int(data,ops_int)

    show_null_str:
        输入data返回以字符串为空值的柱形图
    例：show_null_str(data,ops_str)
    """

    def show_null(data):
        if data.isnull().sum().max() == 0:
            print('无空值')
        else:
            from pyecharts import options as opts
            from pyecharts.charts import Bar
            from pyecharts.commons.utils import JsCode

            NULL = []
            x_columns = []
            x_i = data.columns
            null_list = data.isnull().sum().tolist()

            for i in range(0, len(data.columns)):
                if null_list[i] == 0:
                    pass
                else:
                    NULL.append(null_list[i])
                    x_columns.append(x_i[i])
            max_all = data.notnull().sum().max()
            line_null = []
            for i in range(0, len(NULL)):
                line_null.append(float("%.2f" % ((NULL[i] / max_all) * 100)))

            X = x_columns
            colors = ['#8A54B6', '#5F7FC8', '#E4002C']
            values = line_null
            # 指定柱子颜色的js代码
            color_function = """
                    function (params) {
                        if (params.value < 20) 
                            return '#5F7FC8';
                        else if (params.value > 20 && params.value < 80) 
                            return '#7884D6';
                        else return '#FF8325';
                    }
                    """

            bar = (
                Bar()
                    .add_xaxis(X)
                    .add_yaxis(""
                               , values
                               , category_gap="40%"
                               , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))

                               )

                    .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=20, name="20%"),
                                                                           opts.MarkLineItem(y=80, name="80%"),
                                                                           opts.MarkLineItem(y=50, name="50%")],
                                                                     label_opts=opts.LabelOpts(formatter="{c}%")),
                                     label_opts=opts.LabelOpts(formatter="{c}%")
                                     )

                    .set_global_opts(title_opts=opts.TitleOpts(title="各个商品销量比较"))
                    .set_global_opts(
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        name="",
                        min_=0,
                        max_=100,
                        position="left",
                        offset=0,

                        axisline_opts=opts.AxisLineOpts(
                            linestyle_opts=opts.LineStyleOpts(color=colors[0])
                        ),
                        axislabel_opts=opts.LabelOpts(formatter=("{value}%")),
                    ),

                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),

                    # 坐标轴显示不全处理
                    xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 45},
                                             name_textstyle_opts=opts.TextStyleOpts(font_size=100))
                )
                    .set_global_opts(title_opts=opts.TitleOpts(title="空值查看"))

            )

            return bar.render_notebook()

    def show_null_int(data, ops_int):
        if (data == ops_int).sum().max() == 0:
            print('无此空值')
        else:

            from pyecharts import options as opts
            from pyecharts.charts import Bar
            from pyecharts.commons.utils import JsCode

            x_columns = []
            x_i = data.columns

            NULL_int = []

            list_ops_int = (data == ops_int).sum().tolist()

            for i in range(0, len(data.columns)):
                if list_ops_int[i] == 0:
                    pass
                else:
                    NULL_int.append(list_ops_int[i])
                    x_columns.append(x_i[i])
            max_all = len(data)
            line_null = []
            for i in range(0, len(NULL_int)):
                line_null.append(float("%.2f" % ((NULL_int[i] / max_all) * 100)))

            X = x_columns
            colors = ['#8A54B6', '#5F7FC8', '#E4002C']
            values = line_null
            # 指定柱子颜色的js代码
            color_function = """
                    function (params) {
                        if (params.value < 20) 
                            return '#5F7FC8';
                        else if (params.value > 20 && params.value < 80) 
                            return '#7884D6';
                        else return '#FF8325';
                    }
                    """

            bar = (
                Bar()
                    .add_xaxis(X)
                    .add_yaxis(""
                               , line_null
                               , category_gap="40%"
                               , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))
                               , stack='stack')
                    .add_yaxis(""
                               , None
                               , category_gap="40%"
                               , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))
                               , stack='stack')

                    .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=20, name="20%"),
                                                                           opts.MarkLineItem(y=80, name="80%"),
                                                                           opts.MarkLineItem(y=50, name="50%")],
                                                                     label_opts=opts.LabelOpts(formatter="{c}%")),
                                     label_opts=opts.LabelOpts(formatter="{c}%")
                                     )

                    .set_global_opts(title_opts=opts.TitleOpts(title="各个商品销量比较"))
                    .set_global_opts(
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        name="",
                        min_=0,
                        max_=100,
                        position="left",
                        offset=0,

                        axisline_opts=opts.AxisLineOpts(
                            linestyle_opts=opts.LineStyleOpts(color=colors[0])
                        ),
                        axislabel_opts=opts.LabelOpts(formatter=("{value}%")),
                    ),

                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),

                    # 坐标轴显示不全处理
                    xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 45},
                                             name_textstyle_opts=opts.TextStyleOpts(font_size=100))
                )
                    .set_global_opts(title_opts=opts.TitleOpts(title="空值查看"))

            )

            return bar.render_notebook()

    # object指定空
    def show_null_str(data, ops_str):
        if (data == ops_str).sum().max() == 0:
            print('无此空值')
        else:
            from pyecharts import options as opts
            from pyecharts.charts import Bar
            from pyecharts.commons.utils import JsCode

            x_columns = []
            x_i = data.columns

            NULL_str = []

            list_ops_str = (data == ops_str).sum().tolist()

            for i in range(0, len(data.columns)):
                if list_ops_str[i] == 0:
                    pass
                else:
                    NULL_str.append(list_ops_str[i])
                    x_columns.append(x_i[i])
            max_all = len(data)
            line_null = []
            for i in range(0, len(NULL_str)):
                line_null.append(float("%.2f" % ((NULL_str[i] / max_all) * 100)))

            X = x_columns
            colors = ['#8A54B6', '#5F7FC8', '#E4002C']
            values = line_null
            # 指定柱子颜色的js代码
            color_function = """
                    function (params) {
                        if (params.value < 20) 
                            return '#5F7FC8';
                        else if (params.value > 20 && params.value < 80) 
                            return '#7884D6';
                        else return '#FF8325';
                    }
                    """

            bar = (
                Bar()
                    .add_xaxis(X)
                    .add_yaxis(""
                               , line_null
                               , category_gap="40%"
                               , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))
                               , stack='stack')
                    .add_yaxis(""
                               , None
                               , category_gap="40%"
                               , itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function))
                               , stack='stack')

                    .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=20, name="20%"),
                                                                           opts.MarkLineItem(y=80, name="80%"),
                                                                           opts.MarkLineItem(y=50, name="50%")],
                                                                     label_opts=opts.LabelOpts(formatter="{c}%")),
                                     label_opts=opts.LabelOpts(formatter="{c}%")
                                     )

                    .set_global_opts(title_opts=opts.TitleOpts(title="各个商品销量比较"))
                    .set_global_opts(
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        name="",
                        min_=0,
                        max_=100,
                        position="left",
                        offset=0,

                        axisline_opts=opts.AxisLineOpts(
                            linestyle_opts=opts.LineStyleOpts(color=colors[0])
                        ),
                        axislabel_opts=opts.LabelOpts(formatter=("{value}%")),
                    ),

                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),

                    # 坐标轴显示不全处理
                    xaxis_opts=opts.AxisOpts(name_rotate=60, axislabel_opts={"rotate": 45},
                                             name_textstyle_opts=opts.TextStyleOpts(font_size=100))
                )
                    .set_global_opts(title_opts=opts.TitleOpts(title="空值查看"))

            )

            return bar.render_notebook()
