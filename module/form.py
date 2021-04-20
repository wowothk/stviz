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
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "andby": andby,
        "orientation": orientation,
        "title": title,
        "color": color
    }

def line(df):
    opt = df.columns.tolist()
    show = st.selectbox('show', tuple(opt))
    by = st.selectbox('by', tuple(opt))
    andby = st.selectbox('and', tuple([None] + opt))
    title = st.text_input('Title')
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "andby": andby,
        "title": title,
        "color": color
    }

def pie(df):
    opt = df.columns.tolist()
    show = st.selectbox('show', tuple(opt))
    by = st.selectbox('by', tuple(opt))
    doughnut = st.checkbox('dougnut')
    title = st.text_input('Title')
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "doughnut": doughnut,
        "title": title,
        "color": color
    }

def scatter(df):
    opt = df.columns.tolist()
    x = st.selectbox('x', tuple(opt))
    y = st.selectbox('y', tuple(opt))
    group = st.selectbox('group', tuple([None] + opt))
    title = st.text_input('Title')
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        "x": x,
        "y": y,
        "group": group,
        'title': title,
        "color": color
    }

def heatmap(df):
    opt = df.columns.tolist()
    x = st.selectbox('x', tuple(opt))
    y = st.selectbox('y', tuple(opt))
    value = st.selectbox('value', tuple(opt))
    title = st.text_input('Title')
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        'x': x,
        'y': y,
        'value': value,
        'title': title,
        'color': color
    }

def boxplot(df):
    opt = df.columns.tolist()
    show = st.selectbox('Show', tuple(opt))
    by = st.selectbox('By', tuple([None] + opt))
    orientation = st.selectbox('orientation', (
        'horizontal',
        'vertical'
    ))
    title = st.text_input('Title')
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        "show": show,
        "by": by,
        "orientation": orientation,
        "title": title,
        'color': color
    }

def histogram(df):
    opt = df.columns.tolist()
    show = st.selectbox("Show", tuple(opt))
    title = st.text_input("Title")
    color = st.selectbox("color pallete", 
        ('default', 'base', 'pastel', 'husl', 'set2')
    )
    del df
    del opt
    return {
        'show': show,
        'title': title,
        'color': color
    }
