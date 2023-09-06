# streamlit_app.py

import streamlit as st

import json
from collections import defaultdict as dd
from os import listdir
from os.path import isfile, join
from functools import partial
@st.cache_data
def get_data(base_path):
    org_files = [f for f in listdir(base_path) if isfile(join(base_path, f))]
    data = dd(partial(dd,(partial(dd,dict))))
    categories = None
    for org_file in org_files:
        name = org_file.split('.json')[0]
        with open(join(base_path, org_file), 'r') as f:
            org_data = json.load(f)
        f.close()
        if categories is None:
            categories = list(org_data.keys())
        #q_data = dd(lambda: dd(dict))
        for cat, questions in org_data.items():
            for ques in questions:
                data[name][cat][ques['question']] = {'result': ques['result'], 'source': ques['source']}
        #data[name] = q_data

    names = list(data.keys())

    return data, names, categories

def create_tab(data):
    questions = [None] + list(data.keys())
    question = st.selectbox(
        'Select a question',
        (questions))
    if question is not None:
        ques_res = data[question]
        st.write(question)
        st.write(ques_res['result'])
        metadata = None
        for i, src in enumerate(ques_res['source']):
            if metadata is None:
                metadata = src['metadata']
            with st.expander(f'Source {i + 1}'):
                st.write(src['content'])

        st.divider()

        with st.expander("Metadata"):
            st.write(f'Organisation Section: {metadata["sector"]}')
            st.write(f'Organisation Links: {metadata["rel"]}')


st.title('NQuireOrg')
st.write('Get to know your BCorp Certified corporations')

base_path = 'data'

data, names, categories = get_data(base_path)

options = [None] + names

option = st.selectbox(
    'Select an organisation',
    (options))

if option is not None:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(categories)

    with tab1:
        cat_data = data[option][categories[0]]
        create_tab(cat_data)
    with tab2:
        cat_data = data[option][categories[1]]
        create_tab(cat_data)
    with tab3:
        cat_data = data[option][categories[2]]
        create_tab(cat_data)
    with tab4:
        cat_data = data[option][categories[3]]
        create_tab(cat_data)
    with tab5:
        cat_data = data[option][categories[4]]
        create_tab(cat_data)
    with tab6:
        cat_data = data[option][categories[5]]
        create_tab(cat_data)
    with tab7:
        cat_data = data[option][categories[6]]
        create_tab(cat_data)

