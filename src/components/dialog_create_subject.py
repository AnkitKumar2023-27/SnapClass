import  streamlit as st
from src.components.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the detail of new Subject")
    sub_id=st.text_input("Subject Code",placeholder="CS101")
    sub_name=st.text_input("Subject Name",placeholder="AIML")
    sub_section=st.text_input("Section",placeholder="A" )


    if st.button("Create Subject now",type="primary",width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,) 
                st.toast("Subject Created  Sucessfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error:{str(e)}")
        else:
            st.warning("please Fill all Details")        