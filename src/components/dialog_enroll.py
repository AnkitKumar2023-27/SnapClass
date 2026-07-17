import time
import streamlit as st
from src.components.database.db import enroll_student_to_subject, check_student_enrolled


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if join_code:
            from src.components.database.config import supabase
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()

            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                already_enrolled = check_student_enrolled(student_id, subject['subject_id'])

                if already_enrolled:
                    st.warning('You are already enrolled in this subject')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success('Successfully enrolled!')
                    time.sleep(1)
                    st.rerun()
            else:
                st.error('Subject not found. Check the code and try again.')
        else:
            st.warning('Please enter a subject code')                                                                                                                                                                                                                                           