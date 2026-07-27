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

    # dialog_attendance_result.py mein
    with col2:
        if st.button('Confirm & Save', 
                    width='stretch', 
                    type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance saved!")

                # ✅ Auto check low attendance
                from src.components.email_alerts import (
                    check_and_send_alerts
                )
                from src.components.database.db import (
                    get_all_students_attendance_for_subject
                )

                subject_id = logs[0]['subject_id']
                attendance_list = (
                    get_all_students_attendance_for_subject(
                        subject_id
                    )
                )
                low_students = [
                    s for s in attendance_list 
                    if s['percentage'] < 75
                ]

                if low_students:
                    sent, _ = check_and_send_alerts(
                        subject_id=subject_id,
                        subject_name="",
                        subject_code="",
                        attendance_list=low_students
                    )
                    if sent:
                        st.info(
                            f"📧 Auto-alerts sent to "
                            f"{len(sent)} students"
                        )

                st.session_state.attendance_images = []
                st.rerun()

            except Exception as e:
                st.error(f'Sync failed: {e}')

@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df,logs)
