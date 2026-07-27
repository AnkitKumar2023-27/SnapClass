import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_email_config():
    return {
        'email': st.secrets['email']['sender_address'],
        'password': st.secrets['email']['app_password'],
        'name': st.secrets['email']['sender_name']
    }


def send_low_attendance_email(
    student_name,
    student_email,
    subject_name,
    subject_code,
    present,
    total,
    percentage
):
    if not student_email:
        return False, "No email address found"

    config = get_email_config()

    needed_for_75 = max(0, int(0.75 * total) - present + 1)

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; 
                 background: #f5f5f5; padding: 20px;">

        <div style="
            max-width: 500px;
            margin: auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            border-top: 5px solid #EB4459;
        ">
            <h2 style="color: #EB4459;">
                ⚠️ Low Attendance Alert
            </h2>

            <p>Dear <b>{student_name}</b>,</p>

            <p>Your attendance in 
               <b>{subject_name} ({subject_code})</b> 
               is below the required 75%.</p>

            <div style="
                background: #fff3f3;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                border-left: 4px solid #EB4459;
            ">
                <p>📊 <b>Classes Attended:</b> 
                   {present} / {total}</p>
                <p>📉 <b>Your Attendance:</b> 
                   {percentage}%</p>
                <p>🎯 <b>Required:</b> 75%</p>
                <p>📚 <b>Classes needed:</b> 
                   Attend {needed_for_75} more classes 
                   to reach 75%</p>
            </div>

            <p style="color: #666;">
                Please attend more classes to avoid 
                attendance shortage issues.
            </p>

            <div style="
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #999;
                font-size: 12px;
            ">
                SnapClass AI Attendance System
            </div>
        </div>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = (
            f"⚠️ Low Attendance: {subject_name} "
            f"({percentage}%)"
        )
        msg['From'] = (
            f"{config['name']} <{config['email']}>"
        )
        msg['To'] = student_email

        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(
                config['email'], 
                config['password']
            )
            server.send_message(msg)

        return True, "Email sent successfully"

    except Exception as e:
        return False, str(e)


def check_and_send_alerts(subject_id, subject_name, 
                          subject_code, attendance_list):
    sent = []
    failed = []

    for student in attendance_list:
        if student['percentage'] < 75:
            success, msg = send_low_attendance_email(
                student_name=student['name'],
                student_email=student['email'],
                subject_name=subject_name,
                subject_code=subject_code,
                present=student['present'],
                total=student['total'],
                percentage=student['percentage']
            )
            if success:
                sent.append(student['name'])
            else:
                failed.append(
                    f"{student['name']}: {msg}"
                )

    return sent, failed