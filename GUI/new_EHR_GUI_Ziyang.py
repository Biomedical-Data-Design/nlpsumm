import streamlit as st
from annotated_text import util
from streamlit_timeline import st_timeline
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
#import streamlit_scrollable_textbox as stx
from streamlit.components.v1 import html
import re
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from ast import literal_eval as le
# -- Set page config
apptitle = 'EHR summary'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:",layout="wide")


# side bar
st.sidebar.markdown("## Input files")
my_upload = st.sidebar.file_uploader("Upload an file or a folder", type=["csv"])

#default path to load current data
default_upload = "D:/GitHub/nlpsumm/GUI/corpus_test.csv"

select_event = None
if my_upload is not None:
    rawin = pd.read_csv(my_upload)
    rawin["PatientID"] = rawin["PatientID"].map(str)
    rawin["TimeID"] = rawin["TimeID"].map(str)
    names = rawin["PatientID"].unique().tolist()
    st.sidebar.markdown("## Select a patient")
    select_event = st.sidebar.selectbox('select a patient?', names)
    xldf = rawin[rawin["PatientID"] == select_event]
else:
    rawin = pd.read_csv(default_upload)
    rawin["PatientID"] = rawin["PatientID"].map(str)
    rawin["TimeID"] = rawin["TimeID"].map(str)
    names = rawin["PatientID"].unique().tolist()
    st.sidebar.markdown("## Select a patient")
    select_event = st.sidebar.selectbox('select a patient?', names)
    xldf = rawin[rawin["PatientID"] == select_event]

# get the time for creating timeline
filetime_list = []
for text_tag_str in xldf["Real_text_tag"].tolist():
    #remove the first and last []
    text_tag_str = text_tag_str[1:-1]
    #split by , and get the first one
    time_tag_str = text_tag_str.split(",")[2]
    #remove the first and last ''
    time_tag_str = time_tag_str[2:-1]
    filetime = time_tag_str.split(" ")[0]
    filetime_list.append(filetime)
# print(filetime_list)

    

# main page
st.title('Patient Overview')
st.write(filetime_list)
st.markdown("""
* Use the menu at left to select a patient
* Patient's summary will appear below
""")
if select_event is not None:
    # create df for checkbox
    all_cat = ["CAD", "MEDICATION", "SMOKER", "HYPERTENSION", "DIABETES",'FAMILY_HIST','OBESE','HYPERLIPIDEMIA']
    dat_cat = pd.DataFrame(all_cat, columns=['Category'])
    dat_doc = pd.DataFrame()
    for i in range(xldf["TimeID"].shape[0]):
        tf = [x in le(xldf["Pred_tag_doc"].iloc[i]) for x in all_cat]
        # here change the value to reflect true categories for each docu
        # dat_doc.insert(loc=i, column=xldf["TimeID"].iloc[i], value=tf)

        dat_doc.insert(loc=i, column=filetime_list[i], value=tf)
    df = pd.concat([dat_doc, dat_cat], axis = 1)

    # render check box from Java
    checkbox_renderer = JsCode(
            """
            class CheckboxRenderer{
            init(params) {
                this.params = params;
                this.eGui = document.createElement('input');
                this.eGui.type = 'checkbox';
                this.eGui.checked = params.value;
                this.checkedHandler = this.checkedHandler.bind(this);
                this.eGui.addEventListener('click', this.checkedHandler);
            }
            checkedHandler(e) {
                let checked = e.target.checked;
                let colId = this.params.column.colId;
                this.params.node.setDataValue(colId, checked);
            }
            getGui(params) {
                return this.eGui;
            }
            destroy(params) {
            this.eGui.removeEventListener('click', this.checkedHandler);
            }
            }//end class
        """
        )
    
    # make check box
    gd = GridOptionsBuilder.from_dataframe(df)
    #gd.configure_pagination(enabled = True) 
    gd.configure_default_column(groupable = False)
    gd.configure_column("Category", minWidth=150, maxWidth=150, suppressMovable=True)
    #pin the first column
    gd.configure_column("Category", pinned='left', lockPinned=True)

    for i in range(len(filetime_list)):
        # gd.configure_column(xldf["TimeID"].iloc[i], editable=True, cellRenderer=checkbox_renderer, resizable=True, suppressMovable=True)
        gd.configure_column(filetime_list[i], editable=True, cellRenderer=checkbox_renderer, resizable=True, suppressMovable=True)
    gd.configure_selection(selection_mode = 'multiple', use_checkbox = False)
    
    
    gridOption = gd.build()

    ag_grid = AgGrid(
            df,
            gridOptions=gridOption,
            allow_unsafe_jscode=True,
            data_return_mode="as_input",
            update_mode="grid_changed")
    
    # update the hight based on check box changes
    if "df" not in st.session_state:
        st.session_state.df = df
    
    st.session_state.df = ag_grid["data"]
    ## apparant bug: category column changed locatioin!!! affect the num+1 -> num down below

    # make timeline
    items = []
    for i in range(xldf["TimeID"].shape[0]):
        # add the date to "start": date
        temp = {"content": filetime_list[i], "start": filetime_list[i]}
        items.append(temp)
    opts = {
        "height": '200px',
        "moveable": False,
        "zoomable": False,
        # "end": len(items),
        "timeAxis": {"scale": "year", "step": 1}
    }
    timeline = st_timeline(items, groups=[], options=opts)
    #hide the time under the timeline

    
# show text
    if timeline is not None:
        st.subheader("Health Record: "+timeline["content"])
        num = filetime_list.index(timeline["content"])
        ## get what check box is selected for a document
        if "selected_rows_array" not in st.session_state:
            st.session_state.selected_rows_array = []
        st.session_state.selected_rows_array = st.session_state.df.iloc[:,num].array
        if not np.array_equal(st.session_state.selected_rows_array, st.session_state.df.iloc[:,num].array):
            st.session_state.selected_rows_array = st.session_state.df.iloc[:,num+1].array
            st.experimental_rerun()
        
        rows = [idx for idx, value in enumerate(list(st.session_state.selected_rows_array)) if value == True]
        categories = list(st.session_state.df["Category"].iloc[rows])
        
        if len(rows) == 0:
            st.markdown('<b style="color:#69c"> * No risk factor tagged</b>', unsafe_allow_html=True)

            text = xldf["CleanedText"].iloc[num]
            words = text.strip().split()

            ## get word bags
            word_bag = [i for i in le(xldf["Pred_text_tag"].iloc[num]) if i.split()[2]!="O"]
            wlcad = [i.split()[0] for i in word_bag if i.split()[2]=="CAD"]
            wlsmo = [i.split()[0] for i in word_bag if i.split()[2]=="SMOKER"]
            wlmed = [i.split()[0] for i in word_bag if i.split()[2]=="MEDICATION"]
            wlten = [i.split()[0] for i in word_bag if i.split()[2]=="HYPERTENSION"]
            wldia = [i.split()[0] for i in word_bag if i.split()[2]=="DIABETES"]
            wllip = [i.split()[0] for i in word_bag if i.split()[2]=="HYPERLIPIDEMIA"]
            wlobe = [i.split()[0] for i in word_bag if i.split()[2]=="OBESE"]
            wlfmh = [i.split()[0] for i in word_bag if i.split()[2]=="FAMILY_HIST"]
            
            to_be_tag = {"CAD": wlcad,
                        "SMOKER": wlsmo,
                        "MEDICATION": wlmed,
                        "HYPERTENSION": wlten,
                        "DIABETES": wldia,
                        "FAMILY_HIST": wlfmh,
                        "OBESE": wlobe,
                        "HYPERLIPIDEMIA": wllip}
            annotated = []

            for i in words:
                for c in categories:
                    if c == "CAD":
                        color = "#8ef"
                    elif c == "SMOKER":
                        color = "#faa"
                    elif c == "MEDICATION":
                        color = "#fea"
                    elif c == "HYPERTENSION":
                        color = "#afa"
                    elif c == "DIABETES":
                        color = "#faf"
                    elif c == "HYPERLIPIDEMIA":
                        color = "#48929b"
                    elif c == "OBESE":
                        color = "#69c"
                    elif c == "FAMILY_HIST":
                        color = "#664444"
                                            
                add = i+' '
                annotated.append(add)
            tt = util.get_annotated_html(annotated)
            html(tt, height=700, scrolling=True)
            
        else:
            ## get original text
            # raw_text = xldf["RawText"].iloc[num]
            # nt = re.sub('\n',' ',raw_text)
            # nt = re.sub('\t',' ',nt)  
            # nt = re.sub('"',"'",nt)
            # nt = re.sub('>','&gt;',nt) 
            # nt = re.sub('<','&lt;',nt)
            # nt = re.sub('Â',' ',nt)
            # nt = re.sub('â',' ',nt)
            # nt = re.sub('€',' ',nt)
            # nt = re.sub('™',' ',nt)
            # words = nt.strip().split()
            

            text = xldf["CleanedText"].iloc[num]
            words = text.strip().split()

            ## get word bags
            word_bag = [i for i in le(xldf["Pred_text_tag"].iloc[num]) if i.split()[2]!="O"]
            wlcad = [i.split()[0] for i in word_bag if i.split()[2]=="CAD"]
            wlsmo = [i.split()[0] for i in word_bag if i.split()[2]=="SMOKER"]
            wlmed = [i.split()[0] for i in word_bag if i.split()[2]=="MEDICATION"]
            wlten = [i.split()[0] for i in word_bag if i.split()[2]=="HYPERTENSION"]
            wldia = [i.split()[0] for i in word_bag if i.split()[2]=="DIABETES"]
            wllip = [i.split()[0] for i in word_bag if i.split()[2]=="HYPERLIPIDEMIA"]
            wlobe = [i.split()[0] for i in word_bag if i.split()[2]=="OBESE"]
            wlfmh = [i.split()[0] for i in word_bag if i.split()[2]=="FAMILY_HIST"]
            
            to_be_tag = {"CAD": wlcad,
                        "SMOKER": wlsmo,
                        "MEDICATION": wlmed,
                        "HYPERTENSION": wlten,
                        "DIABETES": wldia,
                        "FAMILY_HIST": wlfmh,
                        "OBESE": wlobe,
                        "HYPERLIPIDEMIA": wllip}
            annotated = []

            for i in words:
                for c in categories:
                    if c == "CAD":
                        color = "#8ef"
                    elif c == "SMOKER":
                        color = "#faa"
                    elif c == "MEDICATION":
                        color = "#fea"
                    elif c == "HYPERTENSION":
                        color = "#afa"
                    elif c == "DIABETES":
                        color = "#faf"
                    elif c == "HYPERLIPIDEMIA":
                        color = "#48929b"
                    elif c == "OBESE":
                        color = "#69c"
                    elif c == "FAMILY_HIST":
                        color = "#664444"
                    if i in to_be_tag[c]:
                        add = (i+' ', c, color)
                        break
                    else:
                        add = i+' '
                annotated.append(add)
            tt = util.get_annotated_html(annotated)
            html(tt, height=700, scrolling=True)
    else:
        tt = util.get_annotated_html([ "Please ", "select ", ("a ", "verb"), " file ", "in ","the ","timeline ","to ", "start."])
        st.subheader('Annotated Example')
        html(tt, height=100, scrolling=True)
    