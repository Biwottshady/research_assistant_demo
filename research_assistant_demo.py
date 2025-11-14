import streamlit as st
import requests

st.title("🔎 Research Assistant (Free Wikipedia Search + AI Summary)")

# ------------------ WIKIPEDIA SEARCH ------------------
def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    headers = {"User-Agent": "Mozilla/5.0 (ResearchAssistant/1.0)"}

    response = requests.get(url, params=params, headers=headers)

    try:
        data = response.json()   # THIS IS WHAT FAILED EARLIER
    except Exception as e:
        st.error("Wikipedia returned invalid JSON. Try a different search.")
        return []

    # Extract top 5 summaries
    return [
        item["snippet"]
        .replace("<span class=\"searchmatch\">", "")
        .replace("</span>", "")
        for item in data.get("query", {}).get("search", [])
    ][:5]


# ------------------ AI SUMMARY (ChatGPT Free) ------------------
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

    try:
        return r.json()["output_text"]
    except:
        return "⚠ AI summarizer failed to respond."


# ------------------ UI ------------------
query = st.text_input("Enter your research question:")

if st.button("Search & Summarize"):
    if not query:
        st.warning("Please type something first.")
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
