import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Feedback Assistant")

st.write("Paste student answer and rubric")

# Inputs
rubric = st.text_area("Marking Criteria (Rubric)")
student_answer = st.text_area("Student Answer")

tone = st.selectbox("Tone", ["Supportive", "Direct"])
detail = st.selectbox("Detail Level", ["Brief", "Detailed"])

if st.button("Generate Feedback"):
    if rubric and student_answer:
        
        prompt = f"""
        You are a university teacher.

        Marking criteria:
        {rubric}

        Student answer:
        {student_answer}

        Tone: {tone}
        Detail level: {detail}

        Generate feedback in:
        1. Strengths
        2. Weaknesses
        3. Suggestions

        Do not give full answers. Guide the student.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        feedback = response.choices[0].message.content

        st.subheader("Feedback")
        st.write(feedback)

    else:
        st.warning("Please fill both fields.")
