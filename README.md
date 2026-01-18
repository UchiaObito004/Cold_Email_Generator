# Cold_Email_Generator
A smart tool that generates personalized cold emails using AI. Matches job descriptions with relevant work using vector embeddings.
This project is an AI-powered cold email generator that creates personalized outreach emails from job descriptions. It uses LLaMA 3 via the Groq API with LangChain to understand job requirements, performs semantic search on portfolio data stored in ChromaDB using vector embeddings, and automatically selects the most relevant work. The system then generates clear, professional cold emails, helping freelancers, sales teams, and founders save time while sending more relevant and effective outreach.


Start
│
Input Source
- Web page, text, or URL
│
Text Extraction
- Pull raw text from input
│
LLM Understanding
- Understand meaning and intent
│
Vector Search
- Find related context
│
Context Retrieval
- Get most relevant data
│
LLM Generation
- Generate final content
│
Final Output
- Email, text, or response
│
End
