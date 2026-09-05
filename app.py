import streamlit as st
import re

st.set_page_config(
    page_title="AI Resume Screening & Job Recommendation",
    page_icon="💼",
    layout="wide"
)

st.title("🤖 AI Based Resume Screening & Job Recommendation System")
st.write("Upload your resume and enter a job role to get skill matching and job recommendations.")

# -----------------------------
# Resume text extraction
# -----------------------------

def extract_resume_text(resume):
    file_name = resume.name.lower()

    try:
        if file_name.endswith(".pdf"):
            from pypdf import PdfReader

            reader = PdfReader(resume)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text

        elif file_name.endswith(".docx"):
            from docx import Document

            document = Document(resume)
            return "\n".join(
                paragraph.text for paragraph in document.paragraphs
            )

        elif file_name.endswith(".txt"):
            return resume.read().decode("utf-8", errors="ignore")

    except Exception as e:
        st.error(f"Could not read the resume: {e}")
        return ""

    return ""


# -----------------------------
# Skills database
# -----------------------------

skill_categories = {

    "Technology": [
        "python", "java", "c", "c++", "c#", "javascript", "typescript",
        "html", "css", "react", "angular", "node.js", "nodejs",
        "django", "flask", "streamlit", "sql", "mysql", "mongodb",
        "postgresql", "git", "github", "docker", "aws", "azure",
        "machine learning", "deep learning", "artificial intelligence",
        "ai", "nlp", "data science", "data analysis", "power bi",
        "tableau", "excel", "tensorflow", "pytorch"
    ],

    "Healthcare": [
        "nursing", "patient care", "patient assessment",
        "vital signs", "medication administration", "wound dressing",
        "infection control", "iv care", "clinical documentation",
        "first aid", "emergency care", "bls",
        "basic life support", "clinical practice",
        "pediatrics", "surgery", "medicine",
        "community health", "healthcare", "medical",
        "patient monitoring", "health education",
        "electronic documentation"
    ],

    "Finance": [
        "accounting", "finance", "financial analysis", "bookkeeping",
        "tally", "gst", "taxation", "auditing", "budgeting",
        "financial reporting", "accounts payable", "accounts receivable",
        "payroll", "ms excel"
    ],

    "Human Resources": [
        "human resources", "hr", "recruitment", "talent acquisition",
        "employee relations", "payroll", "training and development",
        "performance management", "hr management"
    ],

    "Marketing": [
        "marketing", "digital marketing", "social media marketing",
        "seo", "content marketing", "advertising", "branding",
        "market research", "sales", "customer service"
    ],

    "Education": [
        "teaching", "lesson planning", "classroom management",
        "curriculum development", "education", "training",
        "academic", "student counselling", "assessment"
    ],

    "Engineering": [
        "engineering", "autocad", "solidworks", "matlab",
        "design", "manufacturing", "quality control",
        "quality assurance", "project management",
        "mechanical", "electrical", "civil", "electronics"
    ],

    "General": [
        "communication", "teamwork", "leadership", "problem solving",
        "time management", "critical thinking", "documentation",
        "customer service", "management"
    ]
}


# -----------------------------
# Job roles and related skills
# -----------------------------

job_database = {

    "python developer": [
        "python", "django", "flask", "sql", "git"
    ],

    "software developer": [
        "python", "java", "c++", "javascript", "sql", "git"
    ],

    "data analyst": [
        "sql", "excel", "data analysis", "power bi", "tableau"
    ],

    "data scientist": [
        "python", "machine learning", "data science",
        "data analysis", "sql"
    ],

    "machine learning engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch"
    ],

    "ai engineer": [
        "python", "artificial intelligence",
        "machine learning", "deep learning", "nlp"
    ],

    "web developer": [
        "html", "css", "javascript", "react"
    ],

    "nurse": [
        "nursing", "patient care", "patient assessment",
        "vital signs", "medication administration",
        "infection control", "clinical documentation"
    ],

    "staff nurse": [
        "nursing", "patient care", "vital signs",
        "medication administration", "wound dressing",
        "infection control"
    ],

    "registered nurse": [
        "nursing", "patient care", "patient assessment",
        "medication administration", "clinical documentation"
    ],

    "clinical nurse": [
        "nursing", "clinical practice", "patient monitoring",
        "vital signs", "medication administration"
    ],

    "healthcare assistant": [
        "healthcare", "patient care", "patient monitoring",
        "first aid", "communication"
    ],

    "accountant": [
        "accounting", "finance", "bookkeeping",
        "tally", "excel", "gst"
    ],

    "financial analyst": [
        "finance", "financial analysis", "excel",
        "financial reporting", "budgeting"
    ],

    "hr executive": [
        "human resources", "recruitment",
        "employee relations", "payroll"
    ],

    "hr manager": [
        "human resources", "recruitment",
        "performance management", "leadership"
    ],

    "teacher": [
        "teaching", "lesson planning",
        "classroom management", "communication"
    ],

    "marketing executive": [
        "marketing", "digital marketing",
        "social media marketing", "communication"
    ],

    "sales executive": [
        "sales", "customer service", "communication",
        "negotiation"
    ]
}


# -----------------------------
# Find skills in resume
# -----------------------------

def find_skills(text):
    text = text.lower()
    found_skills = []

    for category, skills in skill_categories.items():
        for skill in skills:

            # Special handling for short skills
            if len(skill) <= 2:
                pattern = r"\b" + re.escape(skill) + r"\b"
            else:
                pattern = re.escape(skill)

            if re.search(pattern, text):
                if skill not in found_skills:
                    found_skills.append(skill)

    return found_skills


# -----------------------------
# Detect suitable job roles
# -----------------------------

def recommend_jobs(found_skills):
    recommendations = []

    for role, required_skills in job_database.items():

        matched = [
            skill for skill in required_skills
            if skill in found_skills
        ]

        if len(matched) >= 2:
            score = round((len(matched) / len(required_skills)) * 100)

            recommendations.append(
                {
                    "role": role.title(),
                    "score": score,
                    "matched": matched
                }
            )

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations


# -----------------------------
# User Interface
# -----------------------------

resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx", "txt"]
)

job_role = st.text_input(
    "💼 Enter Job Role",
    placeholder="Example: Nurse, Python Developer, Accountant, Teacher"
)


if resume:

    resume_text = extract_resume_text(resume)

    if resume_text.strip():

        st.success("✅ Resume uploaded successfully!")

        with st.expander("📋 View Extracted Resume Text"):
            st.write(resume_text[:5000])

        found_skills = find_skills(resume_text)

        st.subheader("🔍 Skills Found in Resume")

        if found_skills:
            st.write(", ".join(skill.title() for skill in found_skills))
        else:
            st.warning(
                "No predefined skills were detected. "
                "Try a resume containing skills, education, or experience details."
            )

        # -----------------------------
        # Job role matching
        # -----------------------------

        if job_role.strip():

            entered_role = job_role.lower().strip()

            # Exact / partial role search
            selected_role = None

            for role in job_database:

                if role in entered_role or entered_role in role:
                    selected_role = role
                    break

            if selected_role:

                required_skills = job_database[selected_role]

                matched_skills = [
                    skill for skill in required_skills
                    if skill in found_skills
                ]

                missing_skills = [
                    skill for skill in required_skills
                    if skill not in found_skills
                ]

                score = round(
                    (len(matched_skills) / len(required_skills)) * 100
                )

                st.subheader("🎯 Job Role Analysis")

                st.write(
                    f"**Selected Role:** {selected_role.title()}"
                )

                st.progress(score / 100)

                st.write(
                    f"**Skill Match Score: {score}%**"
                )

                if matched_skills:
                    st.success(
                        "Matched Skills: "
                        + ", ".join(
                            skill.title()
                            for skill in matched_skills
                        )
                    )

                if missing_skills:
                    st.warning(
                        "Skills to Improve: "
                        + ", ".join(
                            skill.title()
                            for skill in missing_skills
                        )
                    )

            else:

                st.info(
                    "This exact job role is not in the database. "
                    "Showing the closest job recommendations based on your resume."
                )

        # -----------------------------
        # Recommendations
        # -----------------------------

        recommendations = recommend_jobs(found_skills)

        st.subheader("💼 Recommended Jobs")

        if recommendations:

            for item in recommendations[:8]:

                st.write(
                    f"### {item['role']}"
                )

                st.write(
                    f"**Match Score:** {item['score']}%"
                )

                st.write(
                    "**Matched Skills:** "
                    + ", ".join(
                        skill.title()
                        for skill in item["matched"]
                    )
                )

                st.divider()

        else:

            st.info(
                "No strong job match was found yet. "
                "The resume can still be processed successfully."
            )

    else:

        st.error(
            "❌ Could not extract text from this resume."
        )
