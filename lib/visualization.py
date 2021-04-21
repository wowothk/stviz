import pandas as pd
import numpy as np
import re

numeric_type = ["int64", "float64", "int", "float"]
categorical_type = ["U"]
default = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
base = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860', '#DA8BC3', '#8C8C8C', '#CCB974', '#64B5CD']
pastel = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', '#DEBB9B', '#FAB0E4', '#CFCFCF', '#FFFEA3', '#B9F2F0']
husl = ['#F77189', '#D58C32', '#A4A031', '#50B131', '#34AE91', '#37ABB5', '#3BA3EC', '#BB83F4', '#F564D4']
set2 = ['#66C2A5', '#FC8D62', '#E78AC3', '#A6D854', '#FFD92F', '#E5C494', '#B3B3B3']

class Visual:
    @staticmethod
    def barchart(df, show, by, and_by=None, orientation="horizontal", title=None):
        """
        show: the numeric value variable
        by: the categoric/index variabel
        and_by: grouper
        orientation: horizontal/vertical, if horizontal 'show' is x index else 'show' is y index
        """
        if str(df[show].dtype) not in numeric_type:
            return "error, cannot use a non-numerical column as measure"
        else:
            if and_by:
                df[by] = df[by].astype("str")
                df[and_by] = df[and_by].astype("str")
                ndf = df.groupby(by=[by, and_by], sort=False).sum()
                grp = list(ndf.to_dict().values())[0]
                series = []
                axis = []
                legend_data = []
                for j in df[and_by].unique():
                    data = []
                    for i in df[by].unique():
                        try:
                            data.append(grp[(i, j)])
                        except:
                            data.append(0)

                        if i not in axis:
                            axis.append(i)

                    legend_data.append(j)
                    series.append({
                        "name": j,
                        "type": "bar",
                        "barGap": "5%",
                        "label": {
                            "show": True,
                            "position": "top"
                        },
                        "data": data
                    })

                index_by = {
                    "type": "category",
                    "data": axis
                }
            else:
                df[by] = df[by].astype("str")            
                ndf = df.groupby(by=[by]).sum()
                index_by = {
                        "type":'category',
                        "data": ndf.index.tolist()
                }

                series = [{
                        "data": ndf[show].values.tolist(),
                        "type": 'bar',
                        'name': show,
                        "label": {"show": True, "position": "top"},
                }]

                legend_data = [show]

            if orientation == "horizontal":
                option = {
                    "title":{"text": title},
                    "legend":{"data":legend_data, "show": True},
                    "tooltip":{},
                    "xAxis": index_by,
                    "yAxis": {"type": "value"},
                    "series": series
                }
            else:
                for i in series:
                    i['label']['position'] = "right"
                option = {
                    "title":{"text": title},
                    "legend":{"data":legend_data, "show": True},
                    "tooltip":{},
                    "yAxis": index_by,
                    "xAxis": {"type": "value"},
                    "series": series
                }
            return option
            
    @staticmethod
    def line(df, show, by, and_by=None, title=None):
        """
        show: the numeric value variable
        by: the categoric/index variabel
        and_by: grouper
        orientation: horizontal/vertical, if horizontal 'show' is x index else 'show' is y index
        """
        if str(df[show].dtype) not in numeric_type:
            return "error, cannot use a non-numerical column as measure"
        else:
            if and_by:
                df[by] = df[by].astype("str")
                df[and_by] = df[and_by].astype("str")
                ndf = df.groupby(by=[by, and_by], sort=False).sum()
                grp = list(ndf.to_dict().values())[0]
                series = []
                axis = []
                legend_data = []
                for j in df[and_by].unique():
                    data = []
                    for i in df[by].unique():
                        try:
                            data.append(grp[(i, j)])
                        except:
                            data.append(0)

                        if i not in axis:
                            axis.append(i)

                    legend_data.append(j)
                    series.append({
                        "name": j,
                        "type": "line",
                        "barGap": "5%",
                        "label": {
                            "show": True,
                            "position": "top"
                        },
                        "data": data
                    })

                index_by = {
                    "type": "category",
                    "data": axis
                }
            else:
                df[by] = df[by].astype("str")            
                ndf = df.groupby(by=[by]).sum()
                index_by = {
                        "type":'category',
                        "data": ndf.index.tolist()
                }

                series = [{
                        "data": ndf[show].values.tolist(),
                        "type": 'line',
                        'name': show
                }]
                legend_data = [show]
        
            option = {
                "title":{"text": title},
                "legend":{"data":legend_data},
                "tooltip":{},
                "xAxis": index_by,
                "yAxis": {"type": "value"},
                "series": series
            }
            
            return option

    @staticmethod
    def pie(df, show, by, title=None, doughnut=False):
        """
        by: categorical data
        show: numerical data
        """
        if str(df[show].dtype) in numeric_type and str(df[by].dtype) not in numeric_type:
            ndf = df.groupby(by=[by], sort=False).sum()
            data = [{"value": y, "name": x} for x, y in ndf[show].to_dict().items()]

            option = {
                "title": {
                    "text":title,
                    "left": 'center'
                },
                "tooltip": {},
                "legend": {
                    "orient": "vertical",
                    "left": "left"
                },
                "series": {
                    "type": "pie",
                    "data": data
                }
            }

            if doughnut:
                option["series"]["radius"] = ["40%", "70%"]

            return option
        else:
            return "error, cannot use a non-numerical column as measure on the right place"    

    @staticmethod
    def scatter(df, x, y, group=None,title=None):
        if str(df[x].dtype) in numeric_type and str(df[y].dtype) in numeric_type:
            if group:
                series = []
                unq = df[group].unique()
                grp = df.groupby(by=[group])
                for i in unq:
                    set_grp = grp.get_group(i)[[x,y]].to_dict('split')
                    series.append({
                        "name": i,
                        "data": set_grp['data'],
                        "type": "scatter"
                    })
            else:
                series = {
                    'data': df[[x,y]].to_dict('split')['data'],
                    "type": "scatter"
                }

            option = {
                "title": {
                    "text":title
                },
                'xAxis':{},
                'yAxis':{},
                "legend": {},
                "series": series
            }
            return option
        else:
            return "error"

    @staticmethod
    def histogram(df, show, title=None):
        if str(df[show].dtype) in numeric_type:
            data, idx = np.histogram(df[show], bins='auto')
            index = []
            i = 1
            while i < len(idx):
                if i == 1:
                    index.append(str(idx[i]) + " - " + str(idx[i-1]))
                else:
                    index.append(str(idx[i-1]) + " - " + str(idx[i]))
                i += 1
            
            option = {
                "title": {"text":title},
                "tooltip": {},
                "xAxis": {
                    "type": 'category',
                    "data": index,
                    "scale": True
                },
                "yAxis": {
                    "type": 'value'
                },
                "series": [{
                    "data": [float(i) for i in data],
                    "type": 'bar',
                    "barWidth": '99.3%',
                    "label": {
                        "show": True,
                        "position": 'top'
                    },
                    
                }]
            }
            return option
        else:
            return "error"


    @staticmethod
    def heatmap(df, x, y, value, title=""):
        data = []
        for i in range(len(df[y].unique())):
            for j in range(len(df[x].unique())):
                val = df[(df[x] == df[x].unique()[j]) & (df[y] == df[y].unique()[i])][value]
                if list(val):
                    if str(df[value].dtype) == "int64":
                        data.append([j, i, int(val)])
                    elif str(df[value].dtype) == "float64":
                        data.append([j, i, float(val)])
                else:
                    data.append([j, i, None])

        series = {
            'data': data,
            'type': 'heatmap',
            "label": {
                "show": True
            }
        }

        option = {
            "title": {
                "text": title,
            },
            "tooltip":{'position': 'top'},
            "xAxis": {
                'type': 'category',
                'data': df[x].unique().tolist(),
            },
            "yAxis": {
                'type': 'category',
                'data': df[y].unique().tolist(),
            },
            "visualMap": {
                "min": int(df[value].min()),
                "max": int(df[value].max()),
                'calculable': True,
                'orient': 'horizontal',
                'left': 'center',
                # 'bottom': '15%'
            },
            "series": series
        }
        return option


    @staticmethod
    def boxplot(df, show, by= None, orientation="horizontal", title = None):
        """
        show: numerical
        byy: categorical
        """
        
        if by:
            grp = df.groupby(by=[by], sort=False)
            axisData = []
            data = []
            for i in df[by].unique():
                group = grp.get_group(i)
                axisData.append(i)
                data.append(group[show].tolist())

            xAxis = {
                "type": 'category',
                "data": axisData,
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {
                    "show": False
                },
                "splitLine": {
                    "show": False
                }
            }
            yAxis= {
                "type": 'value',
                "splitArea": {
                    "show": True
                }
            }
        else:
            data = [df[show].tolist()]
            xAxis = {
                "type": 'category',
                "data": [show],
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {
                    "show": False
                },
                "splitLine": {
                    "show": False
                }
            }
            yAxis= {
                "type": 'value',
                "splitArea": {
                    "show": True
                }
            }

        option = {
            "title": {
                'text': title
            },
            "tooltip": {}
        }

        if orientation == "vertical":
            option["xAxis"] = yAxis
            option["yAxis"] = xAxis
        else:
            option["xAxis"] = xAxis
            option["yAxis"] = yAxis

        return { 
            "option":option,
            "data": data
        }

    @staticmethod
    def auto_generator(df):
        dtypes = df.dtypes.astype(str).to_dict()
        options = []
        for i in dtypes.keys():
            if dtypes[i] in numeric_type:
                options.append(Visual.histogram(df, i, i))
            else:
                ndf = df[[i]]
                ndf['count'] = 1
                options.append(Visual.barchart(
                    df=ndf,
                    show="count",
                    by=i,
                    title=i
                ))
                del ndf

        return options

    @staticmethod
    def geomap(df, region, value, map_title, title):
        region = df[region].tolist()
        value = df[value].tolist()
        data = []
        for i in range(len(region)):
            data.append({
                "name": region[i],
                "value": value[i]
            })

        options = {
            "title": {
                "text": title
            },
            "tooltip": {
                "trigger": "item",
                "showDelay": 0,
                "transitionDuration": 0.2
            },
            "visualMap": {
                "left": "right",
                "min": min(value),
                "max": max(value),
                "inRange": {
                    "color": [
                        "#313695",
                        "#4575b4",
                        "#74add1",
                        "#abd9e9",
                        "#e0f3f8",
                        "#ffffbf",
                        "#fee090",
                        "#fdae61",
                        "#f46d43",
                        "#d73027",
                        "#a50026",
                    ]
                },
                "text": ["High", "Low"],
                "calculable": True,
            },
            "series": [
                {
                    "type": "map",
                    "roam": True,
                    "map": map_title,
                    "emphasis": {"label": {"show": True}},
                    "data": data,
                }
            ],
        }
        return options

    @staticmethod
    def radar(df, show, by, title=None, method="sum"):
        """
        show list (multiselect)
        """
        ndf = df.groupby(by).agg(method)
        # indic = df.groupby(by).agg("sum").max(axis=1).to_dict()
        indic = (ndf[show].max(axis=1)+10).to_dict()
        indicator = [{"name":i, "max": j} for i, j in indic.items()]
        del indic
        del df
        data = []
        for x in show:
            data.append({
                "name": x,
                "value": ndf[x].tolist()
            })
        
        del ndf
        options = {
            "title": {
                "text": title
            },
            "tooltip": {},
            "legend": {
                "data": show,
                "orient": "vertical",
                "left": "left"
            },
            "radar": {
                "name": {
                    "textStyle": "#fff",
                    "backgroundColor": "#999",
                    "borderRadius": 3,
                    "padding": [3, 5]
                },
                "indicator": indicator
            },
            "series": [{
                "type": "radar",
                "data": data
            }]
        }
        return options