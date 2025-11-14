import streamlit as st
import requests

st.title("🔎 Research Assistant ")

# ---------------------------------------------------
# 1. Wikipedia FREE Search (no API key required)
# ---------------------------------------------------
def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract top 5 snippets
    return [item["snippet"].replace("<span class=\"searchmatch\">", "")
                             .replace("</span>", "")
            for item in data["query"]["search"]][:5]


# ---------------------------------------------------
# 2. AI Summarizer using ChatGPT-Free API
# ---------------------------------------------------
def summarize_text(text):
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "input": f"Summarize the following text in simple bullet points:\n\n{text}"
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.json()["output_text"]


# ---------------------------------------------------
# UI
# ---------------------------------------------------
query = st.text_input("Enter your research question:")

if st.button("Search & Summarize"):
    if not query:
        st.warning("Please type something.")
        st.stop()

    st.info("🔍 Searching Wikipedia…")
    results = search_wikipedia(query)

    if not results:
        st.error("No results found.")
        st.stop()

    st.write("### 📌 Top Wikipedia Snippets")
    for i, text in enumerate(results, 1):
        st.write(f"**{i}.** {text}")

    combined = " ".join(results)

    st.info("🧠 Generating summary…")
    summary = summarize_text(combined)

    st.write("### 📝 AI Summary")
    st.write(summary)
