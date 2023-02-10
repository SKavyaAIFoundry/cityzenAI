import streamlit as st


# instructions output to user if a file has not yet been selected

def page_instructions_dashboard():
    st.subheader("Please select a document to analyse:")
    st.write("1. Click the 'Document selection' expander in the sidebar.")
    st.write("2. Select a document from the drop down list.")
    st.write("3. Click the 'Run experiments' button.")


def page_instructions_experiment():
    st.subheader("Please select a document to analyse:")
    st.write("1. Select 'Dashboard Page' in the sidebar.")
    st.write("2. Click the 'Document selection' expander in the sidebar.")
    st.write("3. Select a document from the drop down list.")
    st.write("4. Click the 'Run experiments' button.")