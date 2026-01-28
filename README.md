# AI Cold Email Generator

## Overview

This project is an AI-powered cold email generator designed to create personalized outreach emails directly from job descriptions. The goal is to automate and improve cold outreach by tailoring emails to specific job requirements using semantic understanding rather than generic templates.

The system combines a large language model with semantic search to ensure that each email highlights the most relevant skills and portfolio work.

---

## Problem Statement

Cold emails are often ignored because they are generic and poorly aligned with the recipient’s needs. Writing personalized emails for every job posting is time-consuming and does not scale. This project solves that problem by automatically generating targeted, context-aware outreach emails based on job descriptions.

---

## Workflow

1. **Job Description Ingestion**

   * The user provides a job description as input
   * Key requirements and expectations are extracted using an LLM

2. **Semantic Understanding with LLM**

   * **LLaMA 3** (via the **Groq API**) is used through **LangChain**
   * The model understands role requirements, skills, and context

3. **Portfolio Semantic Search**

   * Personal portfolio data is stored in **ChromaDB**
   * Vector embeddings are generated for portfolio entries
   * Semantic search retrieves the most relevant past work based on the job description

4. **Context-Aware Email Generation**

   * Retrieved portfolio items are injected into the LLM prompt
   * The model generates a personalized cold email aligned with the role

---

## Key Features

* Job-description-driven email generation
* Semantic matching between job requirements and portfolio work
* Fully automated and scalable outreach workflow
* Human-like, role-specific email content

---

## Tech Stack

* Python
* LLaMA 3 (Groq API)
* LangChain
* ChromaDB
* Vector Embeddings

---

## Key Takeaways

* Practical use of LLMs for real-world automation
* Combines generative AI with semantic search
* Clear separation between understanding, retrieval, and generation
* Designed for personalization at scale
