import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# Streamlit UI
st.sidebar.title("AI Web Scraper")
st.sidebar.markdown("This application scrapes a website and allows you to parse its content.")
url = st.sidebar.text_input("Enter Website URL", placeholder="https://example.com")

# Step 1: Scrape the Website
if st.sidebar.button("Scrape Website"):
    if url:
        with st.spinner("Scraping the website..."):
            try:
                # Scrape the website
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            except Exception as e:
                st.error(f"Error occurred while scraping the website: {e}")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse", placeholder="e.g., Extract all headings")

    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing the content..."):
                try:
                    # Parse the content with Ollama
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(parsed_result)
                except Exception as e:
                    st.error(f"Error occurred while parsing the content: {e}")
