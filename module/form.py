import streamlit as st

def bar(df):
    opt = df.columns.tolist()
    show = st.selectbox('show', tuple(opt))
    by = st.selectbox('by', tuple(opt))
    andby = st.selectbox('and', tuple([None] + opt))
    orientation = st.selectbox('orientation', (
        'horizontal',
        'vertical'
    ))
    title = st.text_input('Title')
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "andby": andby,
        "orientation": orientation,
        "title": title
    }

def line(df):
    opt = df.columns.tolist()
    show = st.selectbox('show', tuple(opt))
    by = st.selectbox('by', tuple(opt))
    andby = st.selectbox('and', tuple([None] + opt))
    title = st.text_input('Title')
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "andby": andby,
        "title": title
    }

def pie(df):
    opt = df.columns.tolist()
    show = st.selectbox('show', tuple(opt))
    by = st.selectbox('by', tuple(opt))
    doughnut = st.checkbox('dougnut')
    title = st.text_input('Title')
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "doughnut": doughnut,
        "title": title
    }