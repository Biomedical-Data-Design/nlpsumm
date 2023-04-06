import streamlit as st
from annotated_text import util
from streamlit_timeline import st_timeline
#import streamlit_scrollable_textbox as stx
from streamlit.components.v1 import html
import base64
import re
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
# -- Set page config
apptitle = 'EHR summary'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:", )


# side bar
st.sidebar.markdown("## Input files")
my_upload = st.sidebar.file_uploader("Upload an file or a folder", type=["xml"],accept_multiple_files=True)
if my_upload is not None:
    names = [re.sub(".xml","",my_upload[i].name) for i in range(len(my_upload))]
    st.sidebar.markdown("## Select a patient")
    select_event = st.sidebar.selectbox('select a patient?',names)
    if select_event is not None:
        num = names.index(select_event)
        tree = ET.parse(my_upload[num])
        root = tree.getroot()
        nt = re.sub('\n',' ',root[0].text)
        nt = re.sub('\t',' ',nt) 
        nt = re.sub('"',"'",nt)
        ## sample 214 has a weird character
        nt = re.sub('>','&gt;',nt) 
        nt = re.sub('<','&lt;',nt)
        ## new wired character
        nt = re.sub('Â',' ',nt)
        nt = re.sub('â',' ',nt)
        nt = re.sub('€',' ',nt)
        nt = re.sub('™',' ',nt)



# main page
st.title('Patient Overview')
st.markdown("""
* Use the menu at left to select a patient
* Patient's summary will appear below
""")
if select_event is not None:

    items = [
        {"id": 1, "content": "doc1", "start": "2022-10-20"},
        {"id": 2, "content": "doc2", "start": "2022-10-09"},
        {"id": 3, "content": "doc3", "start": "2022-10-18"},
        {"id": 4, "content": "doc4", "start": "2022-10-16"},
        {"id": 5, "content": "doc5", "start": "2022-10-25"},
        {"id": 6, "content": "doc6", "start": "2022-10-27"},
    ]
    opts = {
        "height": '150px',
        "moveable": False
    }
    timeline = st_timeline(items, groups=[], options=opts)



    st.subheader("Health Record")
    tt = util.get_annotated_html(
    "This ",
    ("is", "verb"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    "This ",
    ("is", "verb"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    ".")

    html(tt, height=100, scrolling=True)
