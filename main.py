
import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title = "Ai resume analizer",page_icon = "📄",layout = "centered")
st.title("Ai resume analizer")
st.markdown("Upload your resume and get Ai powered feedback!!!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
uploadFile = st.file_uploader("Upload your resume (PDF or TXT)",type = ["pdf","txt"])
jobRole = st.text_input("Enter the job role you are targetting (optional)")
Analyze = st.button("Analyze button")

def extract_Text_From_Pdf(pdf_file):
    pdfReader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdfReader.pages:
        text+= page.extract_text() + "\n"
        return text

def extract_Text_From_File(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_Text_From_Pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-3")   
if Analyze and uploadFile:
    try:
        fileContent = extract_Text_From_File(uploadFile)
        if not fileContent.strip():
            st.error("File does not have any contents....")
            st.stop()

        promp = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience description
        4. Specific improvements for {jobRole if jobRole else "general job applications"}

        Resume content: {fileContent}
        Please provide your analysis in a clear structured format with recommendations."""

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume viewer with years of experience."},
                {"role": "user", "content": promp}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis result")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



     