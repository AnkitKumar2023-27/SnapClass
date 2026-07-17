import streamlit as st
from src.components.database.db import create_attendance
def show_attendance_result(df, logs):
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, use_container_width=True)

    present = len(df[df['Status'].str.contains('Present')])
    total = len(df)
    st.write(f"**{present}/{total} students present**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            st.rerun()

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                st.rerun()
            except Exception as e:
                st.error('Sync failed!')

@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df,logs)
