import streamlit as st
import requests
from bs4 import BeautifulSoup

# Load API key from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

st.title("Research Assistant with Grok API")

query = st.text_input("Enter your research question:")

if st.button("Search & Summarize"):
    if not query:
        st.warning("Please enter a question!")
    else:
        st.info("🔎 Searching the web...")

        # DuckDuckGo search
        search_url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            st.error(f"Failed to fetch search results: {e}")
            st.stop()

        soup = BeautifulSoup(response.text, "html.parser")
        results = [a.get_text() for a in soup.find_all("a", {"class": "result__a"})][:5]

        if not results:
            st.warning("No results found.")
        else:
            st.write("### Top 5 Search Snippets")
            for i, r in enumerate(results, 1):
                st.write(f"**{i}.** {r}")

            combined_text = " ".join(results)
            st.info("🧠 Summarizing using Grok API...")

            # Call Grok API
            grok_url = "https://api.grok.com/v1/generate"  # Replace with actual endpoint
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "prompt": f"Summarize the following content in clear points:\n{combined_text}",
                "max_tokens": 300
            }

            try:
                r = requests.post(grok_url, headers=headers, json=payload)
                r.raise_for_status()
                summary = r.json().get("text", "No summary returned")
            except Exception as e:
                summary = f"Error calling Grok API: {e}"

            st.write("### AI Summary")
            st.write(summary)
