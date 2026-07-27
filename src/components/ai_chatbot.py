import streamlit as st
from cerebras.cloud.sdk import Cerebras
from src.components.database.db import get_student_stats_for_ai


def get_cerebras_client():
    return Cerebras(
        api_key = st.secrets["cerebras"]["api_key"]
    )


def build_context(student_data, stats_list):
    name       = student_data.get('name', 'Student')
    student_id = student_data.get('student_id')

    context = f"""You are SnapClass AI Assistant — a friendly attendance assistant.
You have real-time access to student attendance data from the database.

Student: {name} (ID: {student_id})

Current Attendance Data:
"""

    if not stats_list:
        context += "\n- No subjects enrolled yet.\n"
    else:
        overall_total   = 0
        overall_present = 0

        for sub in stats_list:
            overall_total   += sub['total']
            overall_present += sub['present']

            context += f"""
Subject: {sub['name']} ({sub['code']}) — Section {sub['section']}
  Attended    : {sub['present']} / {sub['total']} classes
  Percentage  : {sub['percentage']}%
  Status      : {sub['status']}
  Need for 75%: {sub['classes_needed_for_75']} more classes
  Recent dates: {', '.join(sub['dates'][-5:]) if sub['dates'] else 'None'}
"""

        overall_pct = (
            round((overall_present / overall_total) * 100, 1)
            if overall_total > 0 else 0
        )

        context += f"""
Overall Summary:
  Total Classes : {overall_total}
  Total Present : {overall_present}
  Overall %     : {overall_pct}%
  Subjects      : {len(stats_list)}
"""

    context += """
Rules:
- Reply in same language as student (Hindi/English/Hinglish)
- Be friendly and encouraging
- Give exact numbers always
- If attendance low → tell how many classes needed for 75%
- Use emojis to make it friendly
- Keep answers short and clear
"""
    return context


#   print(Cerebras(api_key=...).models.list())
PRIMARY_MODEL  = "gpt-oss-120b"
FALLBACK_MODEL = "zai-glm-4.7"


def get_ai_response(user_message, student_data, chat_history):
    stats_list = get_student_stats_for_ai(student_data['student_id'])
    context    = build_context(student_data, stats_list)

    messages = [{"role": "system", "content": context}]

    for msg in chat_history[-10:]:
        messages.append({
            "role":    msg["role"],
            "content": msg["content"]
        })

    messages.append({"role": "user", "content": user_message})

    try:
        client   = get_cerebras_client()
        response = client.chat.completions.create(
            model      = PRIMARY_MODEL,
            messages   = messages,
            max_tokens = 1000,
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)

        try:
            client = get_cerebras_client()
            response = client.chat.completions.create(
                model      = FALLBACK_MODEL,
                messages   = messages,
                max_tokens = 1000,
            )
            return response.choices[0].message.content
        except Exception as e2:
            return f"❌ AI Error: {str(e2)}"


def chatbot_ui(student_data):
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #5865F2, #EB459E);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    ">
        <h3 style="color: white; margin: 0;">🤖 SnapClass AI Assistant</h3>
        <p style="color: rgba(255,255,255,0.8); margin: 8px 0 0 0;">
            Powered by Cerebras — Super Fast AI ⚡
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {
                "role":    "assistant",
                "content": (
                    f"Hi {student_data['name']}! 👋 Main SnapClass AI hoon.\n\n"
                    "Main aapki help kar sakta hoon:\n"
                    "📊 Attendance percentage check karna\n"
                    "📚 Low attendance subjects dekhna\n"
                    "🎯 75% ke liye kitni classes chahiye\n"
                    "📅 Recent attendance history\n\n"
                    "Kya jaanna chahte ho? 😊"
                )
            }
        ]

    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🗑️", key="clear_chat", help="Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

    if user_input := st.chat_input("Ask about your attendance..."):
        st.session_state.chat_history.append({
            "role":    "user",
            "content": user_input
        })

        with st.spinner("⚡ Thinking..."):
            response = get_ai_response(
                user_message = user_input,
                student_data = student_data,
                chat_history = st.session_state.chat_history[:-1]
            )

        st.session_state.chat_history.append({
            "role":    "assistant",
            "content": response
        })

        st.rerun()

    st.markdown("""
    <p style="color:#999; font-size:0.8rem; text-align:center; margin-top:10px;">
    💡 Try: "Meri attendance kya hai?" · "Which subject is low?" · "Am I safe?"
    </p>
    """, unsafe_allow_html=True)