import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# Streamlit UI
st.title("SQ Web Scraper")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Web"):
    if url:
        st.write("Scraping the website")

        # scrape the website
        dom_content = scrape_website(url)
        body_content = extract_body_content(html_content=dom_content)
        cleaned_content = clean_body_content(body_content=body_content)

        # store the content in streamlit session state
        st.session_state.dom_content = cleaned_content

        # display the dom_content in expandable text box
        with st.expander("View Document Content"):
            st.text_area("Document Content", cleaned_content, height=300)



# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            # parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks=dom_chunks, parse_description=parse_description)
            st.write(parsed_result)