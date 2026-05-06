import streamlit as st

st.title("AI Feedback Assistant")

st.write("Paste student answer and rubric")

# Input fields
rubric = st.text_area("Marking Criteria (Rubric)")
student_answer = st.text_area("Student Answer")

tone = st.selectbox("Tone", ["Supportive", "Direct"])
detail = st.selectbox("Detail Level", ["Brief", "Detailed"])

# Button
if st.button("Generate Feedback"):
    st.write("Generating feedback...")

    # Temporary fake output (no AI yet)
    st.subheader("Feedback")
    st.write(f"""
    Tone: {tone}
    Detail: {detail}

    Strengths:
    - Good attempt at answering the question.

    Weaknesses:
    - Needs more explanation.

    Suggestions:
    - Add more examples and detail.
    """)
