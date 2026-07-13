import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
    <div style="
        background:white;
        border-left:8px solid #EB459E;
        padding:25px;
        border-radius:20px;
        border:1px solid black;
        margin-bottom:20px;
        box-shadow:0 4px 10px rgba(0,0,0,0.08);
    ">

        <h3 style="
            margin:0;
            color:#1E293B;
            font-size:1.5rem;
        ">
            {name}
        </h3>

        <p style="
            color:#64748B;
            margin:10px 0;
        ">
            Code :
            <span style="
                background:#E0E3FF;
                color:#5865F2;
                padding:2px 8px;
                border-radius:5px;
                font-weight:bold;
            ">
                {code}
            </span>
        </p>

        <p style="
            color:#64748B;
            margin:10px 0 20px 0;
        ">
            Section :
            <b>{section}</b>
        </p>
    """

    if stats:
        html += """
        <div style="
            display:flex;
            gap:8px;
            flex-wrap:wrap;
            margin-bottom:15px;
        ">
        """

        for icon, label, value in stats:
            html += f"""
            <div style="
                background:#EB459E10;
                padding:6px 12px;
                border-radius:12px;
                font-size:0.9rem;
            ">
                {icon}
                <b>{value}</b>
                {label}
            </div>
            """

        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()