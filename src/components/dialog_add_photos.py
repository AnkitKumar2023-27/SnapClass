import streamlit as st
import numpy as np
from PIL import Image
import time


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write('Add classroom photos to scan for attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type="secondary", width='stretch'):
            st.session_state.photo_tab = 'camera'
            st.rerun()                                    # ✅ rerun added

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type='primary', width='stretch'):
            st.session_state.photo_tab = 'upload'
            st.rerun()                                    # ✅ rerun added

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            img = np.array(Image.open(cam_photo).convert("RGB"), dtype=np.uint8)
            st.session_state.attendance_images.append(img)
            st.toast('Photo Captured')
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True
        )
        if uploaded_files:
            for f in uploaded_files:
                img = np.array(Image.open(f).convert("RGB"), dtype=np.uint8)
                st.session_state.attendance_images.append(img)
            st.toast(f'{len(uploaded_files)} photo(s) added')
            st.rerun()

    st.divider()
    count = len(st.session_state.attendance_images)
    st.write(f"📸 {count} photo(s) ready to scan")

    if count > 0:
        if st.button("Clear all photos", type='tertiary'):
            st.session_state.attendance_images = []
            st.rerun()