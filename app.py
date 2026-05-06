import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI Feedback Assistant")
st.write("Upload or paste student work and marking criteria.")

def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    return ""

# PDF uploads
st.subheader("Upload Files")

rubric_pdf = st.file_uploader("Upload Marking Criteria PDF", type=["pdf"])
student_pdf = st.file_uploader("Upload Student Work PDF", type=["pdf"])

rubric_pdf_text = extract_pdf_text(rubric_pdf)
student_pdf_text = extract_pdf_text(student_pdf)

# Manual text option
st.subheader("Or Paste Text Manually")

rubric_text = st.text_area("Marking Criteria / Rubric", value=rubric_pdf_text, height=180)
student_answer = st.text_area("Student Work / Answer", value=student_pdf_text, height=220)

tone = st.selectbox("Tone", [
    "Warm and encouraging",
    "Professional and balanced",
    "Direct and clear",
    "Gentle and supportive",
    "Firm but respectful",
    "Motivational",
    "Neutral academic"
])

detail = st.selectbox("Detail Level", [
    "Very brief",
    "Brief",
    "Moderate",
    "Detailed",
    "Very detailed with examples"
])

feedback_style = st.selectbox("Feedback Style", [
    "Human teacher comment",
    "Strengths and improvements",
    "Rubric-based feedback",
    "Feedforward advice",
    "Question-based guidance",
    "Kind but honest feedback",
    "Student-friendly simple language",
    "Higher education academic style",
    "Coaching style",
    "Balanced praise and correction"
])
if st.button("Generate Feedback"):
    if rubric_text.strip() and student_answer.strip():

        prompt = f"""
You are an experienced university teacher.

Your task is to generate feedback on the student's work using the marking criteria.

Marking criteria:
{rubric_text}

Student work:
{student_answer}

Teacher settings:
Tone: {tone}
Detail level: {detail}
Feedback style: {feedback_style}

Write the feedback in a natural human teacher voice.
Avoid robotic, generic, or overly polished AI language.
Make it sound like a real educator reviewing student work.

Generate feedback in this structure:

1. Strengths
2. Areas for improvement
3. Rubric-based comments
4. Suggested feedforward advice

Rules:
- Do not give a final grade.
- Do not invent marks.
- Do not rewrite the whole assignment for the student.
- Do not provide full answers.
- Keep the teacher as the final author.
- Feedback must be editable and suitable for teacher review.
"""

        with st.spinner("Generating feedback..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

        feedback = response.choices[0].message.content

        st.subheader("AI Draft Feedback")
        editable_feedback = st.text_area("Teacher Editable Feedback", value=feedback, height=350)

        st.download_button(
            label="Download Final Feedback",
            data=editable_feedback,
            file_name="final_feedback.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please upload or paste both marking criteria and student work.")
