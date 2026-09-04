import streamlit as st
import re

st.title("AI Based Resume Screening & Job Recommendation System")

st.write("Upload your resume to get started.")

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_role = st.text_input(
    "Enter Job Role",
    placeholder="Example: Python Developer"
)

if resume:
    st.success("Resume uploaded successfully!")

    text = ""

    if resume.name.endswith(".txt"):
        text = resume.read().decode("utf-8", errors="ignore")

    elif resume.name.endswith(".pdf"):
        try:
            from pypdf import PdfReader

            reader = PdfReader(resume)

            for page in reader.pages:
                text += page.extract_text() or ""

        except Exception:
            st.error("PDF reading failed. Please install pypdf.")

    elif resume.name.endswith(".docx"):
        try:
            from docx import Document

            doc = Document(resume)

            for paragraph in doc.paragraphs:
                text += paragraph.text + " "

        except Exception:
            st.error("DOCX reading failed. Please install python-docx.")

    if text:

        st.subheader("Resume Screening")

        skills = [
            "python",
            "java",
            "c++",
            "sql",
            "machine learning",
            "deep learning",
            "html",
            "css",
            "javascript",
            "react",
            "django",
            "flask",
            "streamlit",
            "excel",
            "nlp",
            "data analysis",
            "mysql",
            "git"
        ]

        found_skills = []

        resume_text = text.lower()

        for skill in skills:
            if skill in resume_text:
                found_skills.append(skill)

        st.write("### Skills Found")

        if found_skills:
            st.success(", ".join(found_skills))
        else:
            st.warning("No matching skills found.")

        # Job role matching
        if job_role:

            role = job_role.lower()

            job_skills = {
                "python developer": [
                    "python",
                    "django",
                    "flask",
                    "sql",
                    "git"
                ],

                "data scientist": [
                    "python",
                    "machine learning",
                    "data analysis",
                    "sql"
                ],

                "machine learning engineer": [
                    "python",
                    "machine learning",
                    "deep learning",
                    "sql"
                ],

                "ai engineer": [
                    "python",
                    "machine learning",
                    "deep learning",
                    "nlp"
                ],

                "web developer": [
                    "html",
                    "css",
                    "javascript",
                    "react"
                ]
            }

            required_skills = job_skills.get(role, [])

            if required_skills:

                matched = []

                for skill in required_skills:
                    if skill in resume_text:
                        matched.append(skill)

                score = int(
                    (len(matched) / len(required_skills)) * 100
                )

                st.subheader("Job Match Result")

                st.metric(
                    "Match Percentage",
                    f"{score}%"
                )

                st.write("### Matching Skills")

                if matched:
                    st.success(", ".join(matched))
                else:
                    st.warning("No matching skills found.")

                missing = [
                    skill for skill in required_skills
                    if skill not in matched
                ]

                st.write("### Missing Skills")

                if missing:
                    st.warning(", ".join(missing))
                else:
                    st.success("You have all required skills!")

            else:
                st.info(
                    "Job role not available in the recommendation database."
                )

        # Job Recommendations
        st.subheader("Job Recommendations")

        recommendations = []

        if "python" in resume_text:
            recommendations.append("Python Developer")

        if "machine learning" in resume_text:
            recommendations.append("Machine Learning Engineer")

        if "nlp" in resume_text:
            recommendations.append("NLP Engineer")

        if "data analysis" in resume_text or "sql" in resume_text:
            recommendations.append("Data Analyst")

        if (
            "html" in resume_text
            and "css" in resume_text
            and "javascript" in resume_text
        ):
            recommendations.append("Web Developer")

        if "streamlit" in resume_text:
            recommendations.append("AI Application Developer")

        if recommendations:

            for job in recommendations:
                st.success(f"✓ {job}")

        else:
            st.warning(
                "No suitable job recommendations found."
            )

        st.write("### Resume Text Preview")

        st.text_area(
            "Extracted Resume",
            text,
            height=250
        )