import torch

import Directory

# if multiprocessing is required...
#from pages import...

if __name__ == '__main__':
    torch.multiprocessing.freeze_support()

    import sys
    sys.path.append("")
    import streamlit as st
    from pages import summary_page, neurodiversity, reading_ease, gendered_language, gender_test, analogies_idioms
    from streamlit_extras.let_it_rain import rain
    import tensorflow
    from streamlit.script_run_context import get_script_run_ctx
    # page config
    st.set_page_config(page_title='CITYZEN', page_icon=':capital_abcd:')

    # about
    st.sidebar.markdown("**_CITYZEN AI_** is developing an app that utilizes AI technologies to automatically evaluate "
        + "the accessibility, inclusivity and cultural intelligence of learning material documents.  This "
        + "Proof-of-Concept dashboard was developed by the **_GM AI Foundry_**.")

    # sidebar navigation
    options = st.sidebar.radio('Select a page:', 
        ['Dashboard', 'Neurodiversity', 'Reading Ease', 'Gendered Language', 'Test for Gender', 'Analogies & Idioms'])

    if options == "Dashboard":
        summary_page.show()
    elif options == "Neurodiversity":
        neurodiversity.show()
    elif options == 'Reading Ease':
        reading_ease.show()
    elif options == 'Gendered Language':
        gendered_language.show()
    elif options == 'Test for Gender':
        gender_test.show()
    elif options == 'Analogies & Idioms':
        analogies_idioms.show()

