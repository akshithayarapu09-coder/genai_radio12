import sqlite3
import random
import pyttsx3
from openai import OpenAI
client = OpenAI()


# ============================================================
# Initialize DB
# ============================================================
def init_db():
    conn = sqlite3.connect("genai_radio.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS podcasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            topics TEXT,
            filename TEXT
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# LONG PODCAST GENERATOR (4–5 mins)
# ============================================================
def fetch_live_news(topic):
    """Generate 90–120 sec content per topic (AI narration format)."""

    prompt = f"""
    Create a detailed 90–120 second podcast narration about: {topic}.

    Style: 
    - Friendly radio host
    - Engaging storytelling
    - No dates, no breaking news, no live events
    - No repeating sentences
    - Smooth transitions and natural tone
    - 4–6 paragraphs
    - Creative and informative
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"].strip()


# ============================================================
# OFFLINE TTS (NO INTERNET)
# ============================================================
def save_podcast_tts(text, filename):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)   # slower (clear)
    engine.setProperty("volume", 1.0)

    # Save to file
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename


# ============================================================
# MCQ Generator (unchanged)
# ============================================================
from nltk.tokenize import sent_tokenize

def generate_mcqs(sentences, n=5):
    mcqs = []
    random.shuffle(sentences)

    for s in sentences:
        if len(mcqs) >= n:
            break

        words = [w for w in s.split() if w.isalpha() and len(w) > 4]
        if not words:
            continue

        ans = random.choice(words)
        q = s.replace(ans, "_")

        fake = random.sample(["India", "Sports", "Science", "Tech", "Economy", "Health"], 3)
        opts = fake + [ans]
        random.shuffle(opts)

        mcqs.append({
            "question": q,
            "options": opts,
            "answer": ans
        })

    return mcqs