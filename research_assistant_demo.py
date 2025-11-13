import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
import pandas as pd
from transformers import pipeline

# -------------------------------
# 1. Streamlit UI: User Query
# -------------------------------
st.title("Research Assistant Demo (Free Version)")
query = st.text_input("Enter your research question:")

if query:
    st.write("🔎 Searching for relevant information...")

    # -------------------------------
    # 2. Simulated Search Results
    # -------------------------------
    # Replace with real API later if desired
    search_results = [
        "Article 1: Key insights about AI in education. AI can improve learning outcomes.",
        "Article 2: Study on LLMs improving research workflows. Automation can save time.",
        "Article 3: Using Python for automating research tasks and analyzing data efficiently."
    ]

    # Display search results in table
    st.subheader("Search Results")
    df = pd.DataFrame(search_results, columns=["Articles"])
    st.dataframe(df)

    # -------------------------------
    # 3. Summarization using Hugging Face
    # -------------------------------
    st.write("🧠 Summarizing content using a free model...")

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    combined_text = " ".join(search_results)
    
    # Hugging Face models have a max token limit, so we truncate if too long
    if len(combined_text.split()) > 500:
        combined_text = " ".join(combined_text.split()[:500])

    summary_list = summarizer(combined_text, max_length=120, min_length=30, do_sample=False)
    summary = summary_list[0]['summary_text']

    # -------------------------------
    # 4. Overview / Dashboard
    # -------------------------------
    st.subheader("AI Summary (Free)")
    st.write(summary)

    # Optional: Simple keyword visualization
    st.subheader("Keyword Frequency (Demo)")
    keywords = ["AI", "LLM", "automation", "Python", "research"]
    freq = [combined_text.count(k) for k in keywords]
    keyword_df = pd.DataFrame({"Keyword": keywords, "Frequency": freq})
    st.bar_chart(keyword_df.set_index("Keyword"))
