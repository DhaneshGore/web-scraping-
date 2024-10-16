import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template for the Ollama model
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the Ollama model
model = OllamaLLM(model="llama3")

# Function to parse content with Ollama
def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        st.write(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)

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
                    # Split DOM content into chunks
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    
                    # Parse the content with Ollama
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    
                    # Display the parsed result
                    st.write(parsed_result)
                except Exception as e:
                    st.error(f"Error occurred while parsing the content: {e}")
