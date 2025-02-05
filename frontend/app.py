import streamlit as st
import requests
import json
from typing import Dict
import time

def extract_entities(filename: str) -> Dict:
    """Send request to backend API for entity extraction"""
    url = "http://localhost:8000/api/documents/extract_entities/"
    response = requests.post(url, json={"filename": filename})
    return response.json()

def display_entities(data: Dict):
    """Display entity extraction results in a structured way"""
    st.header("Extracted Entities")
    
    # Display metadata
    st.subheader("Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Entities", data['metadata']['total_entities'])
    with col2:
        st.metric("Categories", len(data['metadata']['categories']))
    
    # Display categories
    st.subheader("Categories Found")
    st.write(", ".join(data['metadata']['categories']))
    
    # Display entities table
    st.subheader("Entities")
    entities_data = [
        {
            "Name": entity['name'],
            "Type": entity['type'],
            "Mentions": entity['mentions']
        }
        for entity in data['characters']
    ]
    st.dataframe(entities_data)

def main():
    st.title("Entity Extraction Tool")
    st.write("Extract living entities from text documents")
    
    # File input
    filename = st.text_input("Enter the filename (e.g., bee-movie.txt):")
    
    if st.button("Extract Entities"):
        if filename:
            with st.spinner("Extracting entities..."):
                try:
                    result = extract_entities(filename)
                    if 'error' in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        display_entities(result)
                except Exception as e:
                    st.error(f"Failed to process request: {str(e)}")
        else:
            st.warning("Please enter a filename")

if __name__ == "__main__":
    main() 