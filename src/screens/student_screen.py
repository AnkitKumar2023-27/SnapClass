import time
import numpy as np
import streamlit as st
from PIL import Image
from src.pipelines.geofence_pipeline import geofence_check_ui
from src.components.ai_chatbot import chatbot_ui

from src.components.header import header_dashboard
from src.screens.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_dashboard
from src.components.database.db import (
    create_student,
    get_all_students,
    unenroll_student_from_subject,
    get_student_subjects,
    get_student_attendance,
)
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.pipelines.liveness_pipeline import get_random_challenge, verify_liveness_from_frames
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialog


def liveness_check_ui():
    if 'current_challenge' not in st.session_state:
        st.session_state.current_challenge = get_random_challenge()
        st.session_state.liveness_passed   = False

    challenge = st.session_state.current_challenge

    st.markdown("""
    <div style="
        background: #E0E3FF;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    ">
        <h3 style="color: #5865F2; margin: 0;">🔐 Liveness Check</h3>
        <p style="color: #333; margin: 8px 0 0 0;">Security verification required</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        f"**Challenge:** {challenge['text']}\n\n"
        f"*{challenge['hint']}*\n\n"
        f"⏱️ You have {challenge['time']} seconds"
    )

    photo = st.camera_input("Complete the challenge above", key="liveness_camera")

    col1, col2 = st.columns(2)

    with col1:
        verify_btn = st.button("✅ Verify Liveness", type="primary",   width="stretch", key="verify_liveness_btn")

    with col2:
        if st.button("🔄 New Challenge",             type="secondary", width="stretch", key="new_challenge_btn"):
            st.session_state.pop('current_challenge', None)
            st.rerun()

    if verify_btn and photo:
        img = np.array(Image.open(photo).convert("RGB"), dtype=np.uint8)

        with st.spinner("Analyzing your action..."):
            passed, confidence, message = verify_liveness_from_frames(
                [img], challenge['id']
            )

        if passed:
            st.success(f"✅ {message} (Confidence: {confidence}%)")
            st.session_state.liveness_passed = True
            st.session_state.liveness_image  = img
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ {message} (Confidence: {confidence}%)")
            st.warning("💡 Tip: Make sure your face is clearly visible and well lit")
            st.session_state.pop('current_challenge', None)
            time.sleep(2)
            st.rerun()


def student_dashboard():
    student_data = st.session_state.student_data
    student_id   = student_data['student_id']

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type="secondary", key="student_logout_btn"):
            del st.session_state.student_data
            st.session_state.pop('chat_history', None)
            st.session_state.is_logged_in = False
            st.rerun()

    st.write("")

    tab1, tab2 = st.tabs(["📚 My Subjects", "🤖 AI Assistant"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.header("My Subjects")
        with col2:
            if st.button("+ Enroll in Subject", type="primary", width="stretch"):
                enroll_dialog()

        st.divider()

        subjects        = get_student_subjects(student_id)
        attendance_logs = get_student_attendance(student_id)

        stats_map = {}
        for log in attendance_logs:
            sid = log['subject_id']
            if sid not in stats_map:
                stats_map[sid] = {"total": 0, "attended": 0}
            stats_map[sid]['total'] += 1
            if log.get('is_present'):
                stats_map[sid]['attended'] += 1

        if subjects:
            cols = st.columns(2)
            for i, sub_node in enumerate(subjects):
                sub        = sub_node['subjects']
                sid        = sub['subject_id']
                stats      = stats_map.get(sid, {"total": 0, "attended": 0})
                percentage = (
                    round((stats['attended'] / stats['total']) * 100)
                    if stats['total'] > 0 else 0
                )

                def unenroll_button(s=sid, sn=sub):
                    if st.button(
                        "Unenroll from this course",
                        type='tertiary',
                        width='stretch',
                        icon=':material/delete_forever:',
                        key=f"unenroll_{s}"
                    ):
                        unenroll_student_from_subject(student_id, s)
                        st.toast(f'Unenrolled from {sn["name"]} successfully!')
                        st.rerun()

                with cols[i % 2]:
                    subject_card(
                        name=sub['name'],
                        code=sub['subject_code'],
                        section=sub['section'],
                        stats=[
                            ('📋', 'Total Classes', stats['total']),
                            ('✅', 'Attended',       stats['attended']),
                            ('📊', 'Percentage',     f"{percentage}%"),
                        ],
                        footer_callback=unenroll_button
                    )
        else:
            st.info("No subjects yet. Click '+ Enroll' to get started!")

    with tab2:
        chatbot_ui(student_data)

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Go Back", type="secondary", key="loginbackbtn"):
            for key in [
                'current_challenge', 'liveness_passed',
                'liveness_image',    'geofence_passed',
                'student_location'
            ]:
                st.session_state.pop(key, None)
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using FaceID")
    st.write("")

    # ── Step 1: Geo-fence check ───────────────────
    geofence_ok = st.session_state.get('geofence_passed', False)

    if not geofence_ok:
        geofence_check_ui()
        return

    st.success("✅ Location verified — You are inside campus!")
    st.write("")

    # ── Step 2: Liveness check ────────────────────
    liveness_passed = st.session_state.get('liveness_passed', False)

    if not liveness_passed:
        liveness_check_ui()
        return

    st.success("✅ Liveness verified!")
    st.write("")

    # ── Step 3: Face scan ─────────────────────────
    img = st.session_state.get('liveness_image')

    if img is not None:
        with st.spinner("AI is scanning your face..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found. Please redo liveness check.")
                for key in ['current_challenge', 'liveness_passed', 'liveness_image']:
                    st.session_state.pop(key, None)
                import time
                time.sleep(2)
                st.rerun()

            elif num_faces > 1:
                st.warning("More than one face found.")
                for key in ['current_challenge', 'liveness_passed', 'liveness_image']:
                    st.session_state.pop(key, None)
                import time
                time.sleep(2)
                st.rerun()

            else:
                if detected:
                    student_id   = list(detected.keys())[0]
                    all_students = get_all_students()
                    student      = next(
                        (s for s in all_students if s["student_id"] == student_id), None
                    )
                    if student:
                        for key in [
                            'current_challenge', 'liveness_passed',
                            'liveness_image',    'geofence_passed'
                        ]:
                            st.session_state.pop(key, None)
                        st.session_state.is_logged_in = True
                        st.session_state.user_role    = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}")
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.info("Face not recognized. You might be a new student.")
                        st.session_state.show_registration = True
                else:
                    st.info("Face not recognized. You might be a new student.")
                    st.session_state.show_registration = True

    footer_dashboard()