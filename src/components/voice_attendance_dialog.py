import streamlit as st
import pandas as pd
from datetime import datetime
from src.components.database.db import get_enrolled_students, create_attendance
from src.pipelines.voice_pipeline import process_bulk_audio


def show_attendance_result(df_results, logs):
    st.dataframe(df_results, hide_index=True, use_container_width=True)

    present = len(df_results[df_results['Status'].str.contains('Present')])
    total = len(df_results)
    st.write(f"**{present}/{total} students present**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Discard', width='stretch', key='voice_discard'):
            st.session_state.voice_attendance_results = None
            st.rerun()
    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary', key='voice_confirm'):
            try:
                create_attendance(logs)
                st.toast("Attendance saved!")
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error('Sync failed!')

@st.dialog("voice attendance Result")
def voice_attendance_tab(selected_subject_id):
    st.header("Voice Attendance")
    st.write("")

    audio_data = st.audio_input("Record classroom audio")

    if st.button("Run Voice Analysis", type="primary", width="stretch", disabled=not audio_data):
        with st.spinner("Scanning voices..."):

            enrolled_students = get_enrolled_students(selected_subject_id)  # ✅ db function

            if not enrolled_students:
                st.warning('No students enrolled in this course')
                return

            candidates_dict = {
                int(s['students']['student_id']): s['students']['voice_embedding']
                for s in enrolled_students
                if s['students'].get('voice_embedding')
            }

            if not candidates_dict:
                st.error('No enrolled students have voice profiles registered')
                return

            audio_bytes = audio_data.getvalue()                              # ✅ getvalue not read()

            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results, attendance_to_log = [], []

            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(int(student['student_id']), 0.0)  # ✅ int key
                is_present = bool(score > 0)

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Source": score if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)