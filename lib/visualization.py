import pandas as pd
import numpy as np
import re

numeric_type = ["int64", "float64", "int", "float"]
categorical_type = ["U"]

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