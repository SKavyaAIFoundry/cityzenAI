import streamlit as st

from utilities.extraction_utilities import get_file_content

# utility method to cache file content extraction results in streamlit dashboard
# for faster running of experiments after first run.

#@st.cache(show_spinner = False)
# https://github.com/streamlit/streamlit/issues/2275
@st.cache(hash_funcs={"builtins.SwigPyObject": lambda _: None})
def cache_file_content(file_name):        
    return_status, document_text, word_count, paragraph_count, bullet_count, image_count = get_file_content(file_name)
    return return_status, document_text, word_count, paragraph_count, bullet_count, image_count