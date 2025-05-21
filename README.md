# KaleidoscopeChat – Your Literary Companion for NCERT Class 12 English

Welcome to **KaleidoscopeChat** – an AI-powered conversational assistant designed to help students learn and engage deeply with the *Kaleidoscope* Class 12 NCERT English textbook. Whether it's a poem, story, drama, or non-fiction, **Shalini** (your chatbot muse) guides you with literary insights, summaries, and answers to your doubts.

HuggingFace Space Link: https://huggingface.co/spaces/aakashaldankar/KaleidoscopeChat
---

## ✨ Project Highlights

- 💬 **Chatbot Name**: *Shalini* – your creative literary guide.
- 📚 **Dataset**: Class 12 NCERT English book *Kaleidoscope* (all chapters in PDF).
- 🧠 **LLM Used**: `llama-3.3-70b-versatile` via [Groq API](https://console.groq.com/).
- 🧾 **Tech Stack**: Python, LangChain, Gradio, Qdrant, LlamaIndex, Groq API.
- 🔎 **Retrieval**: Qdrant for chapter-wise vector search with TreeIndex for poems.
- 📁 **Chapters**: Categorized into Stories, Poems, Dramas, and Non-Fictions.
- 🧵 **Conversation Memory**: Keeps track of the last few exchanges for coherent context.

---

## 🗂️ Project Structure

```bash
KaleidoscopeChat/
│
├── Dataset/
│   ├── poems/
│   ├── stories/
│   ├── dramas/
│   └── non_fiction/
│
├── qdrant/
│   ├── poems_index/
│   ├── stories_index/
│   └── ...
│
├── .env
├── main.py
├── chat_engine.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run the Project Locally

Follow the steps below to clone, set up, and run **KaleidoscopeChat** on your local machine.

### ✅ Prerequisites

- Python 3.10 or higher  
- An API Key from [Groq Console](https://console.groq.com/)  
- Git (for cloning)

---

### 🔧 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/aakashaldankar/KaleidoscopeChat.git
   cd KaleidoscopeChat
   ```

2. **Create and Activate a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the App**

   ```bash
   python main.py
   ```

> The Gradio interface will open in your browser. Select a chapter, type your query, and start chatting with Shalini!

---

## 📦 Features

- 📘 **Chapter Selection**: Choose any chapter from the dropdown.
- 💡 **Smart Responses**: Get creative and informative answers based on the selected chapter.
- 📥 **Download Chapters**: Download the PDF of the selected chapter for reference.
- 🧠 **Contextual Understanding**: Maintains chat history for meaningful interactions.
- 🎨 **Beautiful Interface**: Custom-styled Gradio interface with poetic themes.

---

## 🧠 Tech Stack Overview

| Component          | Technology                     |
|--------------------|--------------------------------|
| **LLM**            | LLaMA-3.3 70B (via Groq Cloud) |
| **Interface**      | Gradio                         |
| **Vector Database**| Qdrant                         |
| **Retrieval Engine**| LlamaIndex (Tree + Vector Index) |
| **Framework**      | LangChain                      |

---

## 📌 Notes

- Ensure all Qdrant vector DB files and PDFs are in their appropriate folders.
- The large language model (`llama-3.3-70b-versatile`) runs via **Groq API**, so internet access and a valid API key are required.

---

## 📮 Contact

If you face any issues or would like to contribute:

- 📧 Email: `aakashaldankar@gmail.com`
- 🧠 Created by: **Aakash**

---

## 🌟 Future Enhancements (Planned)

- 🎙️ Voice-based input/output support  
- 🧾 Summary cards for chapters  
- 📌 Bookmarks and query highlights  
- 🇮🇳 Hindi version of Kaleidoscope  
- 📱 Mobile UI support  

---

> “Let the chapters whisper, the poems hum, and the stories unfold — with Shalini by your side.” 📖✨
