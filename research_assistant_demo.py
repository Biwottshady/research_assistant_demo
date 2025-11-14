import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = "YOUR_API_KEY_HERE"

st.title("Research Assistant with Grok API")

query = st.text_input("Enter your research question:")

if st.button("Search & Summarize"):
    if not query:
        st.warning("Please enter a question!")
    else:
        st.info("🔎 Searching the web...")

        # 1. DuckDuckGo search (simple scraping)
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = [a.get_text() for a in soup.find_all("a", {"class": "result__a"})][:5]

        st.write("### Top 5 Search Snippets")
        for i, r in enumerate(results, 1):
            st.write(f"**{i}.** {r}")

        # 2. Combine snippets
        combined_text = " ".join(results)

        st.info("🧠 Summarizing using Grok API...")

        # 3. Call Grok API
        grok_url = "https://api.grok.com/v1/generate"  # Replace with actual endpoint
        headers = {"Authorization": f"Bearer {GROK_API_KEY}"}
        payload = {
            "prompt": f"Summarize the following content in clear points:\n{combined_text}",
            "max_tokens": 300
        }

        r = requests.post(grok_url, headers=headers, json=payload)
        summary = r.json().get("text", "No summary returned")

        st.write("### AI Summary")
        st.write(summary)
