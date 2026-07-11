import streamlit as st
from supabase import create_client ,client

supabase:client=create_client(
    st.secrets["SUPABSE_URl"],
    st.secrets["SUPABASE_KEY"]
)
