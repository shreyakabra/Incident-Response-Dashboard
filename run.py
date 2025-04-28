import os
import streamlit as st

# Example of custom setup before running the Streamlit app
def main():
    # Set any environment variables, custom logging, etc.
    os.environ['MY_APP_CONFIG'] = 'value'

    # Run the Streamlit app
    st.set_page_config(page_title="Incident Response Dashboard", page_icon=":guardsman:", layout="wide")
    # Import and run your Streamlit code
    import Dashboard  # Your main app file (e.g., Dashboard.py)

if __name__ == "__main__":
    main()
