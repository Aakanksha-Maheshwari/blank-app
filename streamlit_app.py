import streamlit as st
from streamlit import session_state as state

# Define individual pages for lab 1 and lab 2
lab1_page = st.Page("lab1.py", title="lab1")
lab2_page = st.Page("lab2.py", title="lab2")
lab3_page = st.Page("lab3.py", title ="lab3")
lab4_page = st.Page("lab4.py", title ="lab4")
lab5_page = st.Page("lab5.py", title ="lab5")

# Initialize navigation with the pages
pg = st.navigation([lab1_page,lab2_page,lab3_page,lab4_page,lab5_page])

# Set page configuration (optional but helps with page title and icon)
st.set_page_config(page_title="Lab Manager", page_icon=":memo:")

# Run the navigation system
pg.run()
