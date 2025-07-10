import streamlit as st
import requests
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from datetime import datetime
import os

# ─── CONFIG ─────────────────────────────────────────────────────────────
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
GPT_MODEL = os.getenv("GPT_MODEL", "mistralai/mistral-7b-instruct")

# Load embeddings from Github at runtime <5s
GITHUB_EMBEDDINGS_URL = "https://raw.githubusercontent.com/ZaynIkhlaq/Ayats_Tagged/main/quran_embeddings.pkl"

# ─── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="🕊️ Journal with the Quran",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        color: #fcd34d;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 500;
        text-shadow: 0 0 8px rgba(252, 211, 77, 0.3);
        margin-bottom: 2rem;
    }
    
    .ayah-box {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333;
        margin: 1rem 0;
    }
    
    .comfort-box {
        background: #1a1a1a;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #fcd34d;
        margin: 1rem 0;
    }
    
    .emotion-box {
        background: #1c1c1c;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .emotion-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: capitalize;
        margin: 0.25rem;
    }
    
    .emotion-green { background-color: #22c55e; color: #000; }
    .emotion-yellow { background-color: #facc15; color: #000; }
    .emotion-red { background-color: #ef4444; color: #fff; }
    
    .arabic-text {
        font-family: 'Noto Naskh Arabic', serif;
        direction: rtl;
        font-size: 1.5rem;
        line-height: 2;
        text-align: right;
        margin-bottom: 0.5rem;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #fcd34d;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ─── OPTIMIZED DATA LOADING ───────────────────────────────────────────
@st.cache_resource
def load_embeddings_from_github():
    """Load pre-computed embeddings from GitHub"""
    
    # Try main embeddings first
    try:
        with st.spinner("🔄 Loading embeddings from GitHub..."):
            response = requests.get(GITHUB_EMBEDDINGS_URL, timeout=30)
            if response.status_code == 200:
                cache_data = pickle.loads(response.content)
                st.success(f"✅ Loaded {cache_data['metadata']['total_verses']} verses!")
                return cache_data
    except Exception as e:
        st.warning(f"⚠️ Main embeddings not found: {e}")
        return None

# ─── UTILITIES ────────────────────────────────────────────────────────
def call_openrouter(system: str, user: str, api_key: str) -> str:
    """Call OpenRouter API for AI responses with user-provided API key"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GPT_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    }

    try:
        res = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        if "choices" not in data or "message" not in data["choices"][0]:
            st.error("Unexpected OpenRouter response")
            return ""

        return data["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        st.error(f"OpenRouter error: {e}")
        return ""

def detect_emotion(entry: str, api_key: str) -> str:
    """Detect emotion in journal entry using AI"""
    system = (
        "You are an emotion classifier. Your job is to detect the dominant emotion in a journal entry. "
        "Respond with exactly ONE WORD (lowercase), and choose only from this list: "
        "sad, anxious, hopeful, grateful, angry, stressed, tired, peaceful, confused, happy, lonely, heartbroken, content, reflective. "
        "Do NOT explain. Do NOT use any other words."
    )
    user = f"Emotion in journal entry:\n{entry}"

    raw = call_openrouter(system, user, api_key)
    
    if not raw:
        return "unsure"

    first_word = raw.strip().lower().split()[0]
    valid_emotions = {
        "sad", "anxious", "hopeful", "grateful", "angry", "stressed", "tired",
        "peaceful", "confused", "happy", "lonely", "heartbroken", "content", "reflective"
    }

    if first_word in valid_emotions:
        return first_word
    else:
        return "unsure"

def generate_comfort_message(entry: str, api_key: str) -> str:
    """Generate comforting message for journal entry"""
    system = ("You're a soft, kind Islamic companion who replies to emotional journal entries in simple, warm words. "
              "Use short sentences. Avoid poetry or deep metaphors. No quotes, no 'I'm sorry to hear'. Just calming, real advice, like a good friend.")
    user = f"My journal entry: {entry}\n\nWrite a 2–3 line comforting message."
    return call_openrouter(system, user, api_key) or "You're doing better than you think. One step at a time is still progress. 🤍"

def get_emotion_color(emotion: str) -> str:
    """Get color class for emotion tag"""
    if not emotion:
        return "emotion-yellow"
    
    emotion = emotion.lower().strip()
    green_emotions = ['peaceful', 'happy', 'reflective']
    yellow_emotions = ['grateful', 'hopeful', 'content']
    red_emotions = ['sad', 'anxious', 'angry', 'stressed', 'lonely', 'heartbroken', 'tired', 'confused']
    
    if emotion in green_emotions:
        return "emotion-green"
    elif emotion in yellow_emotions:
        return "emotion-yellow"
    elif emotion in red_emotions:
        return "emotion-red"
    else:
        return "emotion-yellow"

def find_similar_verses(entry: str, df, embeddings):
    """Find similar verses using pre-computed embeddings"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    entry_embedding = model.encode([entry], convert_to_tensor=False)
    
    similarities = util.cos_sim(entry_embedding, embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:3]
    
    matches = []
    for idx in top_indices:
        row = df.iloc[int(idx)]
        matches.append({
            'surah': row['surah_name_roman'],
            'ayah_no': int(row['ayah_no_surah']),
            'ayah': row['ayah_en'].strip(),
            'ayah_ar': row['ayah_ar'].strip()
        })
    
    return matches

# ─── MAIN APP ────────────────────────────────────────────────────────
def main():
    st.markdown('<h1 class="main-header">🕊️ Journal with the Quran</h1>', unsafe_allow_html=True)
    
    # Load embeddings
    cache_data = load_embeddings_from_github()
    
    if cache_data is None:
        st.error("❌ Failed to load data. Please check your internet connection or upload embeddings to GitHub.")
        st.markdown("""
        ### 🔧 Setup Instructions:
        1. Run `python create_embeddings.py` to create embeddings
        2. Upload `quran_embeddings.pkl` to your GitHub repository
        3. Update the `GITHUB_EMBEDDINGS_URL` in this script
        4. Restart the app
        """)
        return
    
    df = cache_data['df']
    embeddings = cache_data['embeddings']
    metadata = cache_data['metadata']
    
    # Sidebar for app info and API key
    with st.sidebar:
        st.title("📊 App Info")
        st.metric("Total Verses", metadata['total_verses'])
        st.metric("Embedding Size", f"{metadata['embedding_dimension']}D")
        
        if metadata.get('is_test'):
            st.warning("⚠️ Using test data")
        
        st.markdown("---")
        st.title("🔑 API Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="Enter your OpenRouter API key here...",
            help="Get your API key from https://openrouter.ai/keys"
        )
        
        if api_key:
            st.success("✅ API key provided. AI features enabled.")
        else:
            st.info("AI-powered emotion and comfort features are optional. Enter your API key above to enable them.")
        
        st.markdown("---")
        st.markdown("### 📖 How to get an API key:")
        st.markdown("""
        1. Go to [OpenRouter](https://openrouter.ai/keys)
        2. Sign up or log in
        3. Create a new API key
        4. Copy and paste it above
        """)
    
    # Main journal page
    show_journal_page(df, embeddings, api_key)

def show_journal_page(df, embeddings, api_key):
    """Display the main journal entry page"""
    st.markdown("### Write your thoughts below and discover relevant ayahs with reflection.")

    # Use a form for cleaner UI and Enter-to-submit
    with st.form("journal_form", clear_on_submit=False):
        entry = st.text_area(
            "Your Journal Entry",
            placeholder="Write your journal entry here...",
            height=150,
            key="journal_entry"
        )
        submitted = st.form_submit_button("Submit (or press Enter)", use_container_width=True)

    if submitted and entry.strip():
        process_journal_entry(entry.strip(), df, embeddings, api_key)

def process_journal_entry(entry: str, df, embeddings, api_key):
    """Process a journal entry and display results"""
    
    # Create progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### Processing your entry...")
        
        # Step 1: Find similar ayahs (always available)
        with st.spinner("🔍 Finding relevant Quran verses..."):
            matches = find_similar_verses(entry, df, embeddings)
        
        # Step 2: Detect emotion and generate comfort message (only if API key is provided)
        if api_key:
            with st.spinner("🧠 Analyzing emotions..."):
                emotion = detect_emotion(entry, api_key)
            with st.spinner("🌿 Creating comforting message..."):
                comfort = generate_comfort_message(entry, api_key)
        else:
            emotion = None
            comfort = None
        
        # Clear progress and display results
        progress_container.empty()
        display_results(matches, comfort, emotion, api_key is not None)

def display_results(matches, comfort, emotion, show_ai_features):
    """Display the results of journal processing"""
    st.markdown("---")
    st.markdown("### 📖 Relevant Ayahs")
    
    # Display ayahs
    for match in matches:
        with st.container():
            st.markdown(f"""
            <div class="ayah-box">
                <div class="arabic-text">{match['ayah_ar']}</div>
                <p style="font-size: 1.1rem; color: #e0e0e0; margin: 0.5rem 0;">"{match['ayah']}"</p>
                <p style="font-size: 0.9rem; color: #999; margin: 0;">— Surah {match['surah']}, Ayah {match['ayah_no']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Only show AI features if API key is provided
    if show_ai_features:
        st.markdown("### 🌿 Gentle Reminder")
        st.markdown(f"""
        <div class="comfort-box">
            <p style="color: #fcd34d; margin: 0; font-style: italic;">{comfort}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💭 Detected Emotion")
        emotion_color = get_emotion_color(emotion)
        st.markdown(f"""
        <div class="emotion-box">
            <p style="margin: 0;">Your entry reflects: <span class="emotion-tag {emotion_color}">{emotion}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.success("✅ Entry processed successfully! Write another entry above to continue.")

if __name__ == "__main__":
    main() 