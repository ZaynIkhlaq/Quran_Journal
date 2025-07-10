# Quran Journal

A simple Streamlit app. 
Get relevant Qur’anic ayahs and AI-powered emotion detection—all in one place.
Forked from Original Creator.
---

## Features

- **📖 Quranic Reflection:** Instantly find relevant ayahs (verses) from the Quran using AI-powered semantic search.
- **🧠 Emotion Detection:** The app detects your emotional state from your journal entry.
- **🔑 Easy Setup:** Enter your OpenRouter API key directly in the app—no environment variables needed.
- **⚡ Fast & Lightweight:** Loads pre-computed Quran embeddings directly from GitHub for quick verse matching.

---

## Try the Demo
[QuranJournal](https://quranjournal.streamlit.app/)

---

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ZaynIkhlaq/Quran_Journal.git
   cd Quran_Journal
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv myenv
   myenv\Scripts\activate  # On Windows
   # Or, for Mac/Linux:
   # source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. **Get your OpenRouter API key:**
   - Go to [OpenRouter](https://openrouter.ai/keys)
   - Sign up and create an API key
   - Enter it in the app sidebar when prompted

---

## 🛠️ Tech Stack

| Layer        | Tech Used                                        |
| ------------ | ------------------------------------------------ |
| **Frontend** | Streamlit                                        |
| **AI/ML**    | SentenceTransformers, OpenRouter API (Mistral-7B)|
| **Data**     | Pre-computed Quran embeddings (loaded from GitHub)|

---

## Project Structure

```
Quran_Journal/
│
├── app.py                # Main Streamlit app
├── create_embeddings.py  # Script to create Quran embeddings (only needed if updating data)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # License info
├── .gitignore            # Files/folders to ignore in git
```

---

## How It Works

1. **Write your journal entry** in the text area.
2. **Get relevant Quran verses** that match your thoughts.
3. **See your detected emotion** and receive a comforting message.
4. **Enter your API key** in the sidebar for AI emotion detection.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## Contributing

Pull requests and suggestions are welcome.  
Feel free to open an issue or submit a PR or learn or copy or pretty much anything you want.

---

## Acknowledgements

- Full Credit to Original Creator [QuranJournal](https://github.com/RoumaisaTanveer/Quran_Journal)
- [OpenRouter](https://openrouter.ai/) for LLM API access
- [SentenceTransformers](https://www.sbert.net/) for semantic search
- The Quranic text and translation community

---

**May this app help you find peace.**



