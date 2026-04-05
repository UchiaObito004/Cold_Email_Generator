# 📧 AI Cold Email Generator

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=flat&logo=langchain)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange?style=flat)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203-blueviolet?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

An AI-powered cold email generator that creates **personalised outreach emails from job posting URLs**. Paste a job link or job description, get a tailored cold email in seconds — powered by **LLaMA 3**, **semantic search**, and your own portfolio.

---

## 🖥️ Demo

![img1](https://github.com/UchiaObito004/Cold_Email_Generator/blob/main/img1.png?raw=true)

![img2](https://github.com/UchiaObito004/Cold_Email_Generator/blob/main/img2.png?raw=true)

## 🧠 How It Works

```
Job Posting URL / Pasted Job Description
            ↓
  BeautifulSoup scrapes the page
            ↓
  clean_text() removes HTML noise & unicode
            ↓
  LLaMA 3 (Groq) extracts:
  role · skills · experience · description
            ↓
  ChromaDB semantic search
  → finds matching portfolio projects
            ↓
  LLaMA 3 generates a personalised cold email
            ↓
  User copies / downloads the email
```

---

## ✨ Features

- 🔗 **URL-based scraping** — paste any Lever-hosted job URL and scrape automatically
- 📋 **Direct text input** — paste job description from any website (LinkedIn, Naukri, Internshala)
- 🤖 **LLM-powered extraction** — understands role requirements, not just keywords
- 🔍 **Semantic portfolio matching** — ChromaDB finds your most relevant projects
- 🌍 **Multi-language support** — English, Hindi, Spanish, French, German
- 🎨 **Tone control** — Professional, Friendly, Assertive, or Concise
- ⚙️ **Fully configurable** — sender name, company name, tone from the sidebar
- 📥 **Download as .txt** — one-click export
- 🕘 **Email history** — all generated emails saved in session

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | LLaMA 3.3 70B via Groq API |
| Orchestration | LangChain |
| Vector Database | ChromaDB |
| Frontend | Streamlit |
| Web Scraping | BeautifulSoup + Requests |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
Cold_Email_Generator/
├── app.py              # Streamlit UI — sidebar config, input, email display, history
├── chains.py           # LLM logic — job extraction & email generation
├── portfolio.py        # ChromaDB — vector store for portfolio projects
├── utils.py            # Text cleaning — strips HTML tags & unicode noise
├── my_portfolio.csv    # Your portfolio data (Techstack + Links)
├── requirements.txt    # Python dependencies
├── dockerfile          # Docker setup
└── .env                # API keys (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/UchiaObito004/Cold_Email_Generator.git
cd Cold_Email_Generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at 👉 [console.groq.com](https://console.groq.com)

### 4. Add your portfolio data
Edit `my_portfolio.csv` with your own projects:
```
Techstack,Links
"React, Node.js, MongoDB",https://github.com/you/project1
"Python, FastAPI, PostgreSQL",https://github.com/you/project2
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🚀 Usage

### Option 1 — Scrape from URL
1. Go to any **Lever-hosted** job posting — `https://jobs.lever.co`
2. Copy the job URL
3. Select **"Scrape from URL"** in the app
4. Paste the URL and click **Generate Email**

### Option 2 — Paste Job Description
1. Go to **any job posting** — LinkedIn, Naukri, Internshala, anywhere
2. Select all text (`Ctrl+A`) and copy (`Ctrl+C`)
3. Select **"Paste Job Description Text"** in the app
4. Paste and click **Generate Email**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit UI (app.py)         │
│  Sidebar: name · company · tone · lang  │
│  Input: URL scrape or paste text        │
└──────────────┬──────────────────────────┘
               │
       ┌───────▼────────┐
       │   chains.py    │  ← LangChain + LLaMA 3 (Groq)
       │  extract_jobs  │     extracts role, skills,
       │  write_mail    │     generates cold email
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │  portfolio.py  │  ← ChromaDB vector store
       │  load_portfolio│     semantic search on
       │  query_links   │     your portfolio projects
       └────────────────┘
```

---

## 🔑 Key Technical Decisions

**Why Groq?**
Groq's LPU delivers ultra-fast inference speeds — critical for real-time email generation UX. Response times are significantly faster than standard GPU inference.

**Why ChromaDB?**
Lightweight embedded vector database with no server required. Perfect for portfolio-scale semantic search out of the box — no complex infrastructure needed.

**Why LangChain?**
Clean abstraction for prompt templates, output parsers, and LLM chaining. Keeps `chains.py` modular, readable, and easy to extend with new models or providers.

**Why BeautifulSoup over WebBaseLoader?**
`BeautifulSoup`'s `get_text()` extracts clean visible content from HTML far more reliably than `WebBaseLoader`, which often leaves behind tag fragments and noise that confuse the LLM's JSON parser.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)
