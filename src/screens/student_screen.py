import streamlit as st
from PIL import Image
import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_dashboard
from src.components.database.db import create_teacher, check_teacher_exists, teacher_login
import numpy as np



def student_screen():

    style_background_dashboard()
    style_base_layout()


    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Go Back", type="secondary", key="loginbackbtn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using  FaceID")
    st.space()
    st.space()

    photo_source=st.camera_input("position  yur face in the camara centre")
    if photo_source:
        np.array(Image.open(photo_source))



    footer_dashboard()

    
    
 