import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Load API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

st.title("Research Assistant (Free Version)")

query = st.text_input("Enter your research question:")

if st.button("Search & Summarize"):
    if not query:
        st.warning("Please type something.")
        st.stop()

    st.info("🔎 Searching DuckDuckGo...")

    # Use DuckDuckGo HTML Search (FREE, NO API KEY NEEDED)
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(search_url, headers=headers)
        r.raise_for_status()
    except Exception as e:
        st.error(f"Search error: {e}")
        st.stop()

    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for a in soup.select("a.result__a"):
        text = a.get_text(strip=True)
        if text:
            results.append(text)

    results = results[:5]  # top 5 results

    if not results:
        st.warning("No results found — try a different question.")
        st.stop()

    st.write("### 🔎 Top Search Results")
    for i, res in enumerate(results, 1):
        st.write(f"**{i}.** {res}")

    combined = " ".join(results)

    st.info("🧠 Summarizing using ChatGPT… (Free API)")

    # ==== ChatGPT Summarizer ====
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",   # free model
            messages=[
                {"role": "user", 
                 "content": f"Summarize the following search results clearly:\n{combined}"}
            ],
            max_tokens=250
        )

        summary = completion.choices[0].message.content

    except Exception as e:
        summary = f"Error calling ChatGPT: {e}"

    st.write("### 📝 AI Summary")
    st.write(summary)
