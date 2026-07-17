import streamlit as st
from src.components.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    subject_code = st.text_input("Subject Code", placeholder="e.g. CS101", key="new_sub_code")
    name = st.text_input("Subject Name", placeholder="e.g. Data Structures", key="new_sub_name")
    section = st.text_input("Section", placeholder="e.g. A", key="new_sub_section")

    st.write("")

    if st.button("Create", type="primary", width="stretch", key="create_sub_btn"):
        if not subject_code or not name or not section:
            st.error("All fields are required!")
        else:
            result = create_subject(
                subject_code=subject_code,
                name=name,
                section=section,
                teacher_id=teacher_id     
            )
            if result:
                st.toast("Subject created!", icon="✅")
                st.rerun()
            else:
                st.error("Failed to create subject")