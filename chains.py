# chains.py
import os
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

TONE_INSTRUCTIONS = {
    "Professional": "Use a formal, polished, and respectful tone throughout.",
    "Friendly & Conversational": "Use a warm, approachable, and conversational tone.",
    "Assertive & Direct": "Be confident and direct. Lead with value, cut fluff, use short impactful sentences.",
    "Concise": "Keep the entire email under 120 words. Every sentence must earn its place.",
}

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.3,                                          # Fix 1
            groq_api_key=os.getenv("GROQ_API_KEY") or os.getenv("groq_api_key"),
            model_name="llama-3.3-70b-versatile",
        )

    def extract_jobs(self, cleaned_text: str, retries: int = 2) -> list:
        prompt = PromptTemplate.from_template(
            """
### SCRAPED TEXT FROM JOB POSTING:
{page_data}

### INSTRUCTION:
Extract all job postings and return a valid JSON array.
Each object must have EXACTLY these keys:
- "role"        : job title (string)
- "experience"  : required years/level (string)
- "skills"      : list of required skills (array of strings)
- "description" : one-sentence summary (string)

Return ONLY the JSON array — no markdown, no explanation, no preamble.
"""
        )
        chain = prompt | self.llm
        parser = JsonOutputParser()

        last_error = None
        for attempt in range(retries + 1):                           # Fix 2
            try:
                res = chain.invoke({"page_data": cleaned_text})
                parsed = parser.parse(res.content)
                return parsed if isinstance(parsed, list) else [parsed]
            except OutputParserException as e:
                last_error = e
                if attempt < retries:
                    time.sleep(1)

        raise OutputParserException(f"Failed after {retries + 1} attempts: {last_error}")

    def write_mail(
        self,
        job: dict,
        links: list,
        language: str = "English",
        tone: str = "Professional",           # Fix 4
        sender_name: str = "Mohan",           # Fix 3
        company_name: str = "SharpCoders",    # Fix 3
        company_tagline: str = "an AI & Software Consulting company",  # Fix 3
    ) -> str:
        tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["Professional"])

        prompt = PromptTemplate.from_template(
            """
### JOB DETAILS:
{job_description}

### INSTRUCTION:
You are {sender_name}, Business Development Executive at {company_name} — {company_tagline}.
Write a cold email in **{language}**.

Tone: {tone_instruction}

Email Structure:
1. Subject line (prefix with "Subject: ")
2. Short personalised opening referencing the role
3. One line on what {company_name} does
4. Required Skills as bullet points using "•"
5. How {company_name} can help
6. Portfolio links (only from below, max 3)
7. Clear call-to-action
8. Sign-off with {sender_name} and {company_name}

Rules:
- Write ONLY the email. No preamble, no explanation.
- Skills MUST be bullet points, not prose.
- Do NOT invent portfolio links.

### PORTFOLIO LINKS:
{link_list}

### EMAIL:
"""
        )

        chain = prompt | self.llm
        res = chain.invoke({
            "job_description": str(job),
            "link_list": links,
            "language": language,
            "tone_instruction": tone_instruction,
            "sender_name": sender_name,
            "company_name": company_name,
            "company_tagline": company_tagline,
        })
        return res.content.strip()
