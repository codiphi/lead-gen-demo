import streamlit as st
from streamlit_chat import message # type: ignore
import time
import vector_db

def generate_response(prompt):
    response  = vector_db.get_answer(prompt)
    return response


def update_message_state(role, message):
    all_message_template = {'role':role,'content':message}
    if role == 'user':
        st.session_state['user_messages'].append(message)
    elif role == 'assistant':
        st.session_state['ai_messages'].append(message)
    st.session_state['all_messages'].append(all_message_template)
    

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

init_message = "Hello! How can I help?"

if 'user_messages' not in st.session_state:
    st.session_state['user_messages'] = []
if 'ai_messages' not in st.session_state:
    st.session_state['ai_messages'] = []
if 'all_messages' not in st.session_state:
    st.session_state['all_messages'] = []
    update_message_state('assistant', init_message)

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:",placeholder='What are the requirements for a golden visa?', key='input', height=90)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        update_message_state('user', user_input)
        # time.sleep(4)
        # response = f"robot response to - {user_input}"
        response = generate_response(user_input)
        update_message_state('assistant', response)
        for item in st.session_state.items():
            item
        
        


if st.session_state['all_messages']:
    with response_container:
        if len(st.session_state['all_messages']) < 2:
            try:
                message(st.session_state['ai_messages'][0], key=0)
            except:
                pass
        elif len(st.session_state['all_messages']) % 2 == 0:
            for i in range(len(st.session_state['ai_messages'])):
                message(st.session_state['ai_messages'][i], key=str(i))
                message(st.session_state['user_messages'][i], is_user=True, key=str(i) + '_user')
        elif len(st.session_state['all_messages']) % 2 != 0:
            for i in range(len(st.session_state['user_messages'])):
                message(st.session_state['ai_messages'][i], key=str(i))
                message(st.session_state['user_messages'][i], is_user=True, key=str(i) + '_user')
                print(i, ':', len(st.session_state['user_messages']))
            message(st.session_state['ai_messages'][-1], key=str(-1))
            