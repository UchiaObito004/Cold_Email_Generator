# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# ──────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Cold Email Generator",
    page_icon="📧",
)

# ──────────────────────────────────────────
# Session State Init
# ──────────────────────────────────────────
if "email_history" not in st.session_state:
    st.session_state.email_history = []

# ──────────────────────────────────────────
# Cache Chain and Portfolio
# ──────────────────────────────────────────
@st.cache_resource
def get_chain():
    return Chain()

@st.cache_resource
def get_portfolio():
    p = Portfolio()
    p.load_portfolio()
    return p

# ──────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    sender_name     = st.text_input("Your Name", value="Mohan")
    company_name    = st.text_input("Company Name", value="SharpCoders")
    company_tagline = st.text_input("Company Description", value="an AI & Software Consulting company")

    st.divider()

    tone = st.selectbox("Email Tone", [
        "Professional",
        "Friendly & Conversational",
        "Assertive & Direct",
        "Concise",
    ])

    language = st.selectbox("Language", [
        "English", "Hindi", "Spanish", "French", "German"
    ])

    st.divider()

    max_links = st.slider("Max Portfolio Links", 1, 5, 2)
    show_raw  = st.toggle("Show Extracted Job Data", value=False)

    st.divider()

    if st.button("🗑️ Clear History"):
        st.session_state.email_history = []
        st.success("History cleared.")

    if st.button("🔄 Reload Portfolio"):
        get_portfolio.clear()
        st.success("Portfolio will reload on next run.")

# ──────────────────────────────────────────
# Main UI
# ──────────────────────────────────────────
st.title("📧 Cold Email Generator")
st.caption("Paste a job posting URL or the job description text directly.")

input_method = st.radio(
    "Input Method",
    ["Paste Job Description Text", "Scrape from URL"],
    horizontal=True,
)

clean_data = ""
url_input  = ""

if input_method == "Paste Job Description Text":
    job_text   = st.text_area(
        "Paste Job Description Here",
        placeholder="Copy and paste the full job description from any website — LinkedIn, Naukri, Internshala, Greenhouse...",
        height=300,
    )
    clean_data = clean_text(job_text.strip())

else:
    url_input = st.text_input(
        "Job Posting URL",
        placeholder="https://boards.greenhouse.io/glooko/jobs/3768285",
    )

submit = st.button("✉️ Generate Email", type="primary", use_container_width=True)

# ──────────────────────────────────────────
# Generation
# ──────────────────────────────────────────
if submit:

    # Validate input
    if input_method == "Paste Job Description Text":
        if not clean_data:
            st.warning("Please paste a job description.")
            st.stop()

    else:
        if not url_input.strip():
            st.warning("Please enter a job posting URL.")
            st.stop()

        with st.spinner("Fetching job posting…"):
            try:
                headers    = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                response   = requests.get(url_input, headers=headers, timeout=10)
                soup       = BeautifulSoup(response.text, "html.parser")
                raw        = soup.get_text(separator=" ", strip=True)
                clean_data = clean_text(raw)
            except Exception as e:
                st.error(f"Could not fetch URL: {e}")
                st.info("Try switching to 'Paste Job Description Text' instead.")
                st.stop()

    llm_chain = get_chain()
    portfolio  = get_portfolio()

    try:
        with st.spinner("Extracting job requirements…"):
            jobs = llm_chain.extract_jobs(clean_data)

        if not jobs:
            st.info("No jobs found. Try pasting the job description text directly.")
            st.stop()

        for idx, job in enumerate(jobs, start=1):
            role       = job.get("role", "Unknown Role")
            skills     = job.get("skills", [])
            experience = job.get("experience", "Not specified")

            st.divider()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(f"Job {idx}: {role}")
            with col2:
                st.metric("Experience", experience)

            if show_raw:
                with st.expander("🔍 Raw Extracted Job Data"):
                    st.json(job)

            if skills:
                st.markdown("**Required Skills:**")
                st.markdown(" ".join([f"`{s}`" for s in skills]))
            else:
                st.markdown("**Required Skills:** Not listed")

            with st.spinner("Matching portfolio…"):
                links = portfolio.query_links(skills, n_results=max_links)

            with st.spinner("Writing email…"):
                email = llm_chain.write_mail(
                    job=job,
                    links=links,
                    language=language,
                    tone=tone,
                    sender_name=sender_name,
                    company_name=company_name,
                    company_tagline=company_tagline,
                )

            st.markdown("**✉️ Generated Cold Email:**")
            st.text_area("", value=email, height=400, key=f"email_{idx}")

            st.download_button(
                label="⬇️ Download as .txt",
                data=email,
                file_name=f"cold_email_{role.replace(' ', '_')}.txt",
                mime="text/plain",
                key=f"download_{idx}",
            )

            st.session_state.email_history.append({
                "role": role,
                "url": url_input if input_method == "Scrape from URL" else "Pasted Text",
                "tone": tone,
                "language": language,
                "email": email,
            })

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.info("Make sure your GROQ_API_KEY is set correctly in your .env file.")

# ──────────────────────────────────────────
# Email History
# ──────────────────────────────────────────
if st.session_state.email_history:
    st.divider()
    st.subheader("🕘 Email History")

    for i, item in enumerate(reversed(st.session_state.email_history)):
        label = f"#{len(st.session_state.email_history) - i} — {item['role']} ({item['tone']}, {item['language']})"
        with st.expander(label):
            st.caption(f"Source: {item['url']}")
            st.text_area("", value=item["email"], height=300, key=f"hist_{i}")
            st.download_button(
                "⬇️ Download",
                data=item["email"],
                file_name=f"email_{i}.txt",
                mime="text/plain",
                key=f"hist_dl_{i}",
            )
