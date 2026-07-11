import streamlit as st
from textwrap import dedent          # ✅ import added


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    html = dedent(f"""
    <div style="text-align:center; margin-top:30px; margin-bottom:30px;">
        <img src="{logo_url}" width="120" style="display:block; margin:0 auto;">
        <h1 style="
            color: white;
            margin-top: 15px;
            font-family: 'Climate Crisis', cursive;
            font-size: 2.8rem;
            letter-spacing: 4px;
            line-height: 1.2;
        ">
            SNAP<br>CLASS
        </h1>
        <p style="
            color: rgba(255,255,255,0.6);
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            margin-top: 6px;
            letter-spacing: 2px;
        ">
            AI-Powered Attendance System
        </p>
    </div>
    """)

    st.markdown(html, unsafe_allow_html=True)


def header_dashboard():         
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    html = dedent(f"""
    <div style="
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
    ">
        <img src="{logo_url}" width="48" style="border-radius:8px;">
        <h2 style="
            color: #5865F2 !important;
            font-family: 'Climate Crisis', cursive;
            font-size: 1.6rem;
            margin: 0;
            line-height: 1.1;
        ">
            SNAP CLASS
        </h2>
    </div>
    """)

    st.markdown(html, unsafe_allow_html=True)