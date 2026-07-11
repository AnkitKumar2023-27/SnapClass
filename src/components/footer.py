import streamlit as st

def footer_home():
    

    st.markdown(
        f"""
        <div style="
            margin-top:2rem;
            display:flex;
            justify-content:center;
            align-items:center;
            gap:8px;
        ">
            <p style="
                margin:0;
                color:white;
                font-weight:bold;
            ">
                Created with ❤️ by  Ankit Kumar 
            </p>

          

        </div>
        """,
        unsafe_allow_html=True,
    )

def footer_dashboard():
    

    st.markdown(
        f"""
        <div style="
            margin-top:2rem;
            display:flex;
            justify-content:center;
            align-items:center;
            gap:8px;
        ">
            <p style="
                margin:0;
                color:black !important;
                font-weight:bold;
            ">
                Created with ❤️ by  Ankit Kumar 
            </p>

          

        </div>
        """,
        unsafe_allow_html=True,
    )