import time
import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_dashboard
from src.components.database.db import create_teacher, check_teacher_exists, teacher_login,get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card  import subject_card

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if st.session_state.get("is_logged") and st.session_state.get("user_role") == "teacher":
        teacher_dashboard()
    elif st.session_state.get("teacher_login_type") == "register":
        teacher_screen_register()
    else:
        teacher_screen_login()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button("Logout", type="secondary", key="teacher_logout_btn", shortcut="control+backspace"):
            st.session_state["is_logged"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.write("")

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        if st.button("Take Attendance",type="primary",width="stretch", icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        if st.button("Manage Subjects", type="secondary",idth="stretch", icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        if st.button("Attendance Records", type="primary",width="stretch", icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    st.header("Take AI Attendance")


def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_data']
    col1 ,col2=st.columns(2)
    
    with col1 :
        st.header("Manage Subject",width="stretch")
    with col2:
       
       if st.button("create new subject" , width= "stretch") :
            create_subject_dialog(teacher_id) 
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:

            stats = [
                ("👥", "Students", sub["total_students"]),
                ("🕒", "Classes", sub["total_classes"]),
            ]

            def share_btn():
                if st.button(
                    f"Share Code: {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                 share_subject_dialog(sub["name"], sub["subject_code"])

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn,
            )

    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")

def teacher_tab_attendance_records():
    st.header("Attendance Records")     


def login_teacher(username, password):
    if not username.strip() or not password.strip():
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged = True
        return True
    else:
        return False
    




def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Go Back", type="secondary", key="loginbackbtn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using password")

    teacher_username = st.text_input("Enter username", placeholder="user id", key="login_username")
    teacher_password = st.text_input("Enter password", placeholder="Enter password", type="password", key="login_password")

    st.divider()
    st.write("")
    st.write("")

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Login", type="secondary", icon=":material/passkey:", shortcut="control+enter", width="stretch", key="login_btn"):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome Back", icon="👋")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")

    with btnc2:
        if st.button("Register Instead", type="primary", icon=":material/passkey:", shortcut="control+enter", width="stretch", key="goto_register_btn"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_password, confirm_password):
    if not teacher_name or not teacher_username or not teacher_password:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_password != confirm_password:
        return False, "Passwords do not match"
    try:
        create_teacher(
            username=teacher_username,
            password=teacher_password,
            name=teacher_name
        )
        return True, "Successfully registered!"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Go Back Home", type="secondary", key="registerbackbtn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register your Teacher Profile")

    teacher_username = st.text_input("Enter username", placeholder="user id", key="reg_username")
    teacher_name = st.text_input("Enter Name", placeholder="Name", key="reg_name")
    teacher_password = st.text_input("Enter password", placeholder="Enter password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm password", placeholder="Confirm password", type="password", key="reg_confirm_password")

    st.divider()
    st.write("")
    st.write("")

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button("Register", type="secondary", icon=":material/passkey:", shortcut="control+enter", width="stretch", key="register_btn"):
            success, message = register_teacher(
                teacher_username=teacher_username,
                teacher_name=teacher_name,
                teacher_password=teacher_password,
                confirm_password=confirm_password
            )
            if success:
                st.success(message)
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", shortcut="control+enter", width="stretch", key="goto_login_btn"):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()