import streamlit as st
import os
import pandas as pd
import numpy as np
from streamlit_chat import message
from chat_vertex import vertex_chat, vertex_create_request_statue, text_embedding, vertex_get_stock_code


st.markdown("""
    <style type="text/css">
        [data-testid=stSidebar] {
            background-color: rgb(129, 164, 182);
            color: #FFFFFF;
        }
        [aria-selected="true"] {
             color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)

def get_completion_from_messages(messages):
    request_status = vertex_create_request_statue(messages)
    if request_status == "news related to some stocks":
        search_vector = text_embedding(messages)
        return "TODO mongodb vector search search_vector."
        # TODO mongodb vector search
    elif request_status == "one specific stock":
        stock_code = vertex_get_stock_code(messages)
        return str(stock_code[0])
        # TODO mongodb search stock
    else:
        response = vertex_chat(messages)
        return response

def submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''
       
def hide_streamlit_header_footer():
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def get_tables():
    df = pd.DataFrame(
       np.random.randn(10, 5),
       columns=('col %d' % i for i in range(5)))

    st.table(df)

def get_graphs():
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    st.line_chart(chart_data)

if __name__ == '__main__':
    st.title("💬 StockSage AI Chatbox")
#     col1, col2 = st.columns((5, 2))
#     col2.image("assets/img.png", width=120)
    st.write("'An investment in knowledge pays the best interest.' — Benjamin Franklin")
    st.write("Ask any question related to stock.")
    st.sidebar.write('Welcome to StockSage AI! \n We\'re here to simplify your financial journey with personalized, real-time advice and data visualizations. Let\'s make informed financial decisions together!')
  
    action = st.sidebar.radio("Choose the format of stock prices", ("Graphs 📈", "Forms 📝", "Both 📂"))
    if action == "Graphs 📈":
        get_graphs()
    if action == "Forms 📝":
        get_tables()
    if action == "Both 📂":
        get_graphs()
        get_tables()
                              
        
                              
    with st.expander("--About the chatbox--"):
        st.write("You can ask any questions about stock news or a specific company.")
                              
    with st.container():
        st.text_input("User Input:", key='widget',on_change=submit)
    
    if 'context' not in st.session_state:
        st.session_state['context'] = ""

    if 'generated' not in st.session_state: 
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

    if st.session_state.user_input:
        st.session_state['context'] = f"{st.session_state['context']}'User Input:'{st.session_state.user_input}'AI Output:'"
        output=get_completion_from_messages(st.session_state['context'])
        st.session_state['context'] = f"{st.session_state['context']}{output}"
        st.session_state['past'].append(st.session_state.user_input)
        st.session_state['generated'].append(output)
    #     with open("context.txt", "w") as f:
    #         f.write(st.session_state['context'])
    if st.session_state['generated']:
    #     for i in range(len(st.session_state['generated'])-1, -1, -1): # reverse order
        for i in range(0, len(st.session_state['generated']), 1): # order
            message(st.session_state["generated"][i], key=str(i),avatar_style = "initials")
            message(st.session_state['past'][i], 
                    is_user=True, 
                    key=str(i)+'_user',avatar_style = "fun-emoji")