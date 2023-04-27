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
# -- Set page config
apptitle = 'EHR summary'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:",layout="wide")


# side bar
st.sidebar.markdown("## Input files")
my_upload = st.sidebar.file_uploader("Upload an file or a folder", type=["xml"],accept_multiple_files=True)
if my_upload is not None:
    names = [re.sub(".xml","",my_upload[i].name) for i in range(len(my_upload))]
    st.sidebar.markdown("## Select a patient")
    select_event = st.sidebar.selectbox('select a patient?',names)



# main page
st.title('Patient Overview')
st.markdown("""
* Use the menu at left to select a patient
* Patient's summary will appear below
""")
if select_event is not None:
    # test df
    data = {"Category": ["CAD", "Medication", "Smoker", "Hypertention", "Diabetes"]}
    df = pd.DataFrame(data)
    for i in range(len(names)):
        # here change the value to reflect true categories for each docu
        df.insert(loc=i+1, column=names[i], value=False)

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
    gd.configure_default_column(groupable = True)
    gd.configure_column("Category", minWidth=90, maxWidth=90, suppressMovable=True)
    for i in range(len(names)):
        gd.configure_column(names[i], editable=True, cellRenderer=checkbox_renderer, resizable=True, suppressMovable=True)
    gd.configure_selection(selection_mode = 'multiple', use_checkbox = False)
    gridOption = gd.build()

    ag_grid = AgGrid(
            df,
            gridOptions=gridOption,
            allow_unsafe_jscode=True,)
    # update the hight based on check box changes
    if "df" not in st.session_state:
        st.session_state.df = []
    
    st.session_state.df = ag_grid["data"]
    st.write(ag_grid["data"])
    # make timeline
    items = []
    for i in range(len(names)):
        # add the date to "start": date
        temp = {"content": names[i], "start": i}
        items.append(temp)
    opts = {
        "height": '150px',
        "moveable": False
    }
    timeline = st_timeline(items, groups=[], options=opts)

    

    # show text
    if timeline is not None:
        st.subheader("Health Record: "+timeline["content"])
        num = names.index(timeline["content"])
        ## get what check box is selected for a document
        if "selected_rows_array" not in st.session_state:
            st.session_state.selected_rows_array = []
        st.session_state.selected_rows_array = st.session_state.df.iloc[:,num+1].array
        if not np.array_equal(st.session_state.selected_rows_array, st.session_state.df.iloc[:,num+1].array):
            st.session_state.selected_rows_array = st.session_state.df.iloc[:,num+1].array
            st.experimental_rerun()
        rows = [idx for idx, value in enumerate(list(st.session_state.selected_rows_array)) if value == True]
        categories = list(st.session_state.df.iloc[rows,0])
        
        if len(rows) == 0:
            html("Please select a category", height=100, scrolling=True)
        else:
            ## get original text
            tree = ET.parse(my_upload[num])
            root = tree.getroot()
            nt = re.sub('\n',' ',root[0].text)
            nt = re.sub('\t',' ',nt) 
            nt = re.sub('"',"'",nt)
            nt = re.sub('>','&gt;',nt) 
            nt = re.sub('<','&lt;',nt)
            nt = re.sub('Â',' ',nt)
            nt = re.sub('â',' ',nt)
            nt = re.sub('€',' ',nt)
            nt = re.sub('™',' ',nt)
            words = nt.strip().split()
            to_be_tag = {"CAD": ["Record"],
                        "Smoker": ["I"],
                        "Medication": ["not"],
                        "Hypertention": ["him"],
                        "Diabetes": ["you"]}
            annotated = []

            for i in words:
                for c in categories:
                    if i in to_be_tag[c]:
                        add = (i+' ', "verb")
                        break
                    else:
                        add = i+' '
                annotated.append(add)
            tt = util.get_annotated_html(annotated)
            html(tt, height=100, scrolling=True)
    else:
        tt = util.get_annotated_html(["This ", "is ", ("a ", "verb"), "preview."])
        html(tt, height=100, scrolling=True)