import streamlit as st
from simple_chatbot import llm_chatbot
from streamlit_interact import interact_streamlit
from streamlit_option_menu import option_menu
from sql_box import sql_box
from constants import MENU_STYLE, MENU_STYLE_DICT

def main():
    st.markdown(MENU_STYLE, unsafe_allow_html=True)

    with st.sidebar:
        st.sidebar.title("Navigation")
        page = option_menu(
            "Go to",
            ["Basic SQL Chat", "Interactive Streamlit", "LLM Chatbot"],
            icons=["file", "house", "file"],
            menu_icon="cast",
            default_index=0,
            styles=MENU_STYLE_DICT,
        )
    if page == "Interactive Streamlit":
        interact_streamlit()
    elif page == "LLM Chatbot":
        llm_chatbot()
    elif page == "Basic SQL Chat":
        sql_box()

if __name__ == "__main__":
    main()
