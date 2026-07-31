import streamlit as st



def style_background_home():
    st.markdown("""
    <style>

    html, body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"]{
        background: #E2BDEA !important;
    }

    .block-container{
        background: transparent !important;
    }

    </style>
    """, unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown(
        """
        <style>

        .stApp,
        [data-testid="stAppViewContainer"]{
            background-color: #E0E3FF !important;
        }

        h1,h2,h3,h4,h5,h6,p,span,div,label{
            color:black !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def style_base_layout():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100;200;300;400;500;600;700;800;900&family=Climate+Crisis&display=swap');

        #MainMenu,
        footer,
        header{
            visibility:hidden;
        }

        .block-container{
            padding-top:3rem !important;
            padding-bottom:2rem !important;
            padding-left:5rem !important;
            padding-right:5rem !important;
        }

        body{
            font-family:'Outfit',sans-serif;
        }

        h1{
            font-family:'Climate Crisis',cursive !important;
            font-size:3.5rem !important;
            line-height:1.1 !important;
            margin-bottom:0.5rem !important;
            color:white !important;
        }

        h2{
            font-family:'Climate Crisis',sans-serif !important;
            font-size:2rem !important;
            line-height:1.1 !important;
            margin-bottom:0 !important;
            color:white !important;
        }

        button[kind="secondary"]{
            border-radius:1.5rem !important;
            background:#EB4459 !important;
            color:white !important;
            border:none !important;
            transition:transform .25s ease-in-out !important;
        }

        button[kind="tertiary"]{
            border-radius:1.5rem !important;
            background:black !important;
            color:white !important;
            border:none !important;
            transition:transform .25s ease-in-out !important;
        }

        button{
            border-radius:1.5rem !important;
            background:#5865F2 !important;
            color:white !important;
            border:none !important;
            transition:transform .25s ease-in-out !important;
        }

        button:hover{
            transform:scale(1.05);
        }

        </style>
        """,
        unsafe_allow_html=True
    )