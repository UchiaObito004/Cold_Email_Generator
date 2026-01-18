import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("groq_api_key"),
            model_name="llama-3.3-70b-versatile"
        )

    # -----------------------------
    # Extract job data from webpage
    # -----------------------------
    def extract_jobs(self, cleaned_text):
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT:
            {page_data}

            ### INSTRUCTION:
            Extract job postings and return JSON with these keys ONLY:
            - role
            - experience
            - skills (array of strings)
            - description

            Return ONLY valid JSON.
            """
        )

        chain = prompt | self.llm
        res = chain.invoke({"page_data": cleaned_text})

        try:
            parser = JsonOutputParser()
            parsed = parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Failed to parse job data.")

        return parsed if isinstance(parsed, list) else [parsed]

    # -----------------------------
    # Write cold email (bullet skills)
    # -----------------------------
    def write_mail(self, job, links, language="English"):
        prompt = PromptTemplate.from_template(
            """
            ### JOB DETAILS:
            {job_description}

            ### INSTRUCTION:
            You are Mohan, Business Development Executive at SharpCoders
            (an AI & Software Consulting company).

            Write a professional cold email in **{language}**.

            STRICT RULES:
            - Extract "skills" from the job description
            - Show skills ONLY as bullet points
            - Do NOT convert skills into sentences
            - Keep skill names short and exact
            - Be polite and professional
            - Do NOT add any preamble or explanation

            EMAIL STRUCTURE:
            1. Short introduction
            2. Job title mention
            3. Required Skills (bullet list using •)
            4. How SharpCoders can help
            5. Portfolio links
            6. Closing

            Portfolio links:
            {link_list}

            ### EMAIL (NO PREAMBLE):
            """
        )

        chain = prompt | self.llm
        res = chain.invoke({
            "job_description": job,
            "link_list": links,
            "language": language
        })

        return res.content
