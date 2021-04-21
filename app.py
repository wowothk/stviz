import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from module import form
from lib.visualization import Visual
from lib.geomap import usaMap
import json
from streamlit_echarts import Map

default = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
base = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860', '#DA8BC3', '#8C8C8C', '#CCB974', '#64B5CD']
pastel = ['#A1C9F4', '#FFB482', '#8DE5A1', '#FF9F9B', '#D0BBFF', '#DEBB9B', '#FAB0E4', '#CFCFCF', '#FFFEA3', '#B9F2F0']
husl = ['#F77189', '#D58C32', '#A4A031', '#50B131', '#34AE91', '#37ABB5', '#3BA3EC', '#BB83F4', '#F564D4']
set2 = ['#66C2A5', '#FC8D62', '#E78AC3', '#A6D854', '#FFD92F', '#E5C494', '#B3B3B3']

def fileUpload():
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    df = pd.read_csv(uploaded_file)
    return df

def selectVisual():
    option = st.sidebar.selectbox('Choose Type Of Visualization', 
    ('Auto', 'Bar', 'Line', 'Pie', "Scatter", "Heatmap", "Box", "Histogram", "Map"))
    return option

def colormap_check(data):
    if data == "default":
        color = default
    elif data == "base":
        color = base
    elif data == "pastel":
        color = pastel
    elif data == "husl":
        color = husl
    else:
        color = set2
    
    return color

def main():
    st.sidebar.title("Stream Vis")
    st.sidebar.markdown("""
        Streamlit Visualization using Echart 
    """)
    st.sidebar.markdown("""---""")
    try:
        df = fileUpload()
        st.write(df)
        option = selectVisual()
        if option == "Bar":
            data = form.bar(df)
            if st.button('Generate Bar'):
                opt = Visual.barchart(df,
                    data['show'],
                    data['by'],
                    data['andby'],
                    data['orientation'],
                    data['title']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt)
        elif option == "Line":
            data = form.line(df)
            if st.button('Generate Line'):
                opt = Visual.line(df,
                    data['show'],
                    data['by'],
                    data['andby'],
                    data['title']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt)
        elif option == "Pie":
            data = form.pie(df)
            if st.button("Generate Pie"):
                opt = Visual.pie(df,
                    data['show'],
                    data['by'],
                    data['title'],
                    data['doughnut']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt)
        elif option == "Scatter":
            data = form.scatter(df)
            if st.button("Generate Scatter"):
                opt = Visual.scatter(df,
                    data['x'],
                    data['y'],
                    data['group'],
                    data['title']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt)
        elif option == "Box":
            data = form.boxplot(df)
            if st.button("Generate Box"):
                opt = Visual.boxplot(df,
                    data['show'],
                    data['by'],
                    data['orientation'],
                    data['title']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt['option'])
        elif option == "Heatmap":
            data = form.heatmap(df)
            if st.button('Generate Heatmap'):
                opt = Visual.heatmap(df,
                    data['x'],
                    data['y'],
                    data['value'],
                    data['title']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt)
        elif option == "Histogram":
            data = form.histogram(df)
            if st.button("Generate Histogram"):
                opt = Visual.histogram(df,
                    data['show'],
                    data['title']
                )
                opt['color'] = colormap_check(data['color'])
                st_echarts(opt)

        elif option == "Map":
            data = form.geomap(df)
            st.echo(data)
            if st.button("Generate Map"):
                opt = Visual.geomap(df,
                    data["region"],
                    data["value"],
                    data["map_title"],
                    data["title"]
                )
                if data['map'] == "jakarta": 
                    with open("lib/jakarta.json", "r") as f:
                        map = Map(data["map_title"], json.loads(f.read()))
                elif data['map'] == "jogja":
                    with open("lib/jogja.json", "r") as f:
                        map = Map(data["map_title"], json.loads(f.read()))

                st_echarts(opt, map=map)
        else:
            if st.button("Generate"):
                opts = Visual.auto_generator(df)
                for x in opts:
                    st_echarts(x)
 
    except:
        st.markdown("""
            There is no dataset
        """)

if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Echarts Visualization", page_icon=":tada:")
    main()