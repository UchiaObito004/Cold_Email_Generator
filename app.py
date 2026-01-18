# app.py
import streamlit as st

from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# -----------------------------
# Streamlit App Function
# -----------------------------
def create_streamlit_app(llm_chain, portfolio):
    st.set_page_config(layout="wide", page_title="📧 Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Email Generator")

    url_input = st.text_input("Enter a Job Posting URL:", 
                              placeholder="https://careers.nike.com/senior-information-security-analyst/job/R-74144")
    
    language = st.selectbox("Select Email Language:", ["English", "Hindi", "Spanish", "French"])
    
    submit_button = st.button("Generate Cold Email")

    if submit_button:
        if not url_input:
            st.warning("Please enter a valid URL!")
            return

        try:
            with st.spinner("Fetching job details..."):
                # Load the webpage content
                loader = WebBaseLoader([url_input])
                page_content = loader.load().pop().page_content
                clean_data = clean_text(page_content)

            # Load portfolio projects
            portfolio.load_portfolio()

            # Extract jobs and required skills
            jobs = llm_chain.extract_jobs(clean_data)

            if not jobs:
                st.info("No jobs found on this page.")
                return

            for idx, job in enumerate(jobs, start=1):
                st.subheader(f"Job {idx}: {job.get('role', 'Perfect Title')}")
                skills = job.get("skills", [])
                st.markdown("**Required Skills:**")
                if skills:
                    for skill in skills:
                         st.markdown(f"- {skill}")
                else:
                   st.markdown("Not listed")


                # Match your portfolio projects
                project_links = portfolio.query_links(skills)

                # Generate personalized email
                email = llm_chain.write_mail(job, project_links, language=language)
                
                st.markdown("**Generated Cold Email:**")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"An error occurred: {e}")


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    llm_chain = Chain()       # Your LLM wrapper
    portfolio = Portfolio()   # Your portfolio projects
    create_streamlit_app(llm_chain, portfolio)
