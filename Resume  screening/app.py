import os
import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf
from matcher import calculate_similarity

from sklearn.feature_extraction.text import CountVectorizer

def get_top_terms(resume_text, job_text, top_n=5):
    vectorizer = CountVectorizer(stop_words='english')
    vectorizer.fit([resume_text, job_text])

    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    matched_words = resume_words.intersection(job_words)
    return list(matched_words)[:top_n]

def color_score(val):
    if val >= 0.75:
        return 'background-color: #a3f7bf'
    elif val >= 0.5:
        return 'background-color: #fff3b0'
    else:
        return 'background-color: #ffb3b3'

st.title("📄 AI-Powered Resume Screening Tool")

st.subheader("1️⃣ Upload or Load Job Description")

job_desc = st.text_area("Paste the job description here:")

if st.button("📂 Load from job_description.txt"):
    try:
        with open("job_description.txt", "r", encoding="utf-8") as file:
            job_desc = file.read()
        st.success("✅ Job description loaded!")
    except FileNotFoundError:
        st.error("❌ job_description.txt not found!")

st.subheader("2️⃣ Resumes Folder")
st.write("Reading all PDF files from the resumes/ folder...")

resume_folder = "resumes"
pdf_files = [f for f in os.listdir(resume_folder) if f.endswith(".pdf")]

if not pdf_files:
    st.warning("⚠️ No PDF resumes found in the 'resumes/' folder.")
else:
    resume_texts = []
    names = []

    for file_name in pdf_files:
        file_path = os.path.join(resume_folder, file_name)
        text = extract_text_from_pdf(file_path)
        resume_texts.append(text)
        names.append(file_name)

if st.button("🚀 Rank Candidates"):
    if not job_desc:
        st.error("❌ Please enter a job description before ranking.")
    elif not pdf_files:
        st.error("❌ No resumes found.")
    else:
        scores = calculate_similarity(resume_texts, job_desc)
        results_df = pd.DataFrame({"Candidate": names, "Score": scores})
        results_df.sort_values(by="Score", ascending=False, inplace=True)
        
        st.subheader("📊 Ranked Candidates")
        st.dataframe(results_df.style.applymap(color_score, subset=['Score']))
# CSV download button
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
          label="⬇️ Download Results as CSV",
          data=csv,
          file_name='ranked_candidates.csv',
          mime='text/csv'
     )
        results_df.to_csv("ranked_candidates.csv", index=False)
        st.success("✅ Results saved to 'ranked_candidates.csv'")

        st.subheader("🎯 Top Matched Keywords")
        for name, text in zip(names, resume_texts):
            keywords = get_top_terms(text, job_desc)
            st.markdown(f"*{name}* → {', '.join(keywords)}")