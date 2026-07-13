import time
import numpy as np
import streamlit as st
from PIL import Image

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_dashboard
from src.components.database.db import create_student, get_all_students
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding


def student_dashboard():
    st.header("DASHBOARD HERE")


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
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using FaceID")
    st.write("")
    st.write("")

    photo_source = st.camera_input("Position your face in the camera center")

    if photo_source:
        img = np.array(Image.open(photo_source).convert("RGB"), dtype=np.uint8)
        st.session_state.captured_img = img

        with st.spinner("AI is scanning"):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found")
            elif num_faces > 1:
                st.warning("More than one face found — please ensure only you are in frame")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s["student_id"] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.info("Face not recognized. You might be a new student.")
                        st.session_state.show_registration = True
                else:
                    st.info("Face not recognized. You might be a new student.")
                    st.session_state.show_registration = True

    if st.session_state.get("show_registration", False):
        with st.container(border=True):
            st.header("Register new profile")
            new_name = st.text_input("Enter your name", placeholder="e.g. Ankit")
            st.subheader("Optional: voice enrollment")
            st.info("Enroll your voice for voice-only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input("Record your audio, e.g. 'I am present, my name is Akash'")
            except Exception:
                st.error("Audio recording failed")

            if st.button("Create Account", type="primary"):
                if new_name:
                    img = st.session_state.get("captured_img")
                    if img is None:
                        st.warning("Please capture a photo first.")
                    else:
                        with st.spinner("Creating profile"):
                            encodings = get_face_embeddings(img)
                            if encodings:
                                face_emb = encodings[0].tolist()
                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embedding(audio_data.getvalue())
                                response_data = create_student(
                                    new_name,
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )
                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = "student"
                                    st.session_state.student_data = response_data
                                    st.session_state.show_registration = False
                                    st.session_state.captured_img = None
                                    st.toast(f"Profile created! Hi, {new_name}")
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("No face detected in photo. Please try again.")
                else:
                    st.warning("Please enter your name")

    footer_dashboard()