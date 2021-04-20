import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from module import form
from lib.visualization import Visual

def fileUpload():
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    df = pd.read_csv(uploaded_file)
    return df

def selectVisual():
    option = st.sidebar.selectbox('Choose Type Of Visualization', 
    ('Bar', 'Line', 'Pie'))
    return option


def main():
    st.sidebar.title("Stream Vis")
    st.sidebar.markdown("""
        Streamlit Visualization using Echart 
    """)

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
                st_echarts(opt)

    except:
        st.markdown("""
            There is no dataset
        """)


if __name__ == "__main__":
    main()