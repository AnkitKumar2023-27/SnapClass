import streamlit as st
import streamlit.components.v1 as components


def subject_card(name, code, section, stats=None, footer_callback=None):

    stats_html = ""
    if stats:
        stats_html = '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:15px;">'
        for icon, label, value in stats:
            stats_html += f'<div style="background:#EB459E22;padding:6px 12px;border-radius:12px;font-size:0.9rem;color:#1E293B;">{icon} <b>{value}</b> {label}</div>'
        stats_html += "</div>"

    html = f"""
    <div style="
        background:white;
        border-left:8px solid #EB459E;
        padding:25px;
        border-radius:20px;
        border:1px solid #ddd;
        margin-bottom:10px;
        box-shadow:0 4px 10px rgba(0,0,0,0.08);
        font-family:'Outfit',sans-serif;
    ">
        <h3 style="margin:0;color:#1E293B;font-size:1.5rem;">{name}</h3>
        <p style="color:#64748B;margin:10px 0;">
            Code :
            <span style="background:#E0E3FF;color:#5865F2;padding:2px 8px;border-radius:5px;font-weight:bold;">
                {code}
            </span>
        </p>
        <p style="color:#64748B;margin:10px 0 20px 0;">
            Section : <b>{section}</b>
        </p>
        {stats_html}
    </div>
    """

    components.html(html, height=220)

    if footer_callback:
        footer_callback()