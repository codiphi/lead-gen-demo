import streamlit as st
from streamlit_chat import message # type: ignore
import vector_db
import intent_chain as ic
import question_chain as qc

def generate_response(prompt):
    if st.session_state['intent'][0] == '0':
        name = ic.extract_name(prompt)
        if name != 'None':
            st.session_state['name'] = [name]
            response = qc.investment_question(st.session_state['name'][0], conversation_hist())
            st.session_state['intent'] = ['1']
        else:
            response  = vector_db.get_answer(prompt)
            st.session_state['intent'] = ['99']
            
    elif st.session_state['intent'][0] == '1':
        strategy = ic.investment_response(prompt)
        if strategy == '0':
            st.session_state['strategy'] = ['investment']
        elif strategy == '1':
            st.session_state['strategy'] = ['to_live']
        else:
            st.session_state['strategy'] = ['not_sure']
        response = qc.property_type_question(st.session_state['name'][0], conversation_hist())
        st.session_state['intent'] = ['2']
    
    elif st.session_state['intent'][0] == '2':
        off_plan = ic.off_plan_response(prompt)
        if off_plan == '0':
            st.session_state['property_type'] = ['off_plan']
        elif off_plan == '1':
            st.session_state['property_type'] = ['ready_to_move']
        else:
            st.session_state['property_type'] = ['not_sure']
        response = qc.budget_question(st.session_state['name'][0], conversation_hist())
        st.session_state['intent'] = ['3']
        
    elif st.session_state['intent'][0] == '3':
        budget = ic.budget_response(prompt)
        if budget != 'None':
            st.session_state['budget'] = [budget]
        else:
            st.session_state['budget'] = ['not_sure']
        response = qc.contact_question(st.session_state['name'][0], conversation_hist())
        st.session_state['intent'] = ['4']
    
    elif st.session_state['intent'][0] == '4':
        st.session_state['email'] = [ic.extract_email(prompt)]
        st.session_state['number'] = [ic.extract_number(prompt)]
        response = 'Awesome, feel free to ask me anything!'
        st.session_state['intent'] = [99]
        
    elif st.session_state['intent'][0] == '99':
        response = vector_db.get_answer(prompt)
    return response

def conversation_hist():
    temp = [st.session_state['all_messages'][-2],st.session_state['all_messages'][-1]]
    return temp

def update_message_state(role, message):
    all_message_template = {'role':role,'content':message}
    if role == 'user':
        st.session_state['user_messages'].append(message)
    elif role == 'assistant':
        st.session_state['ai_messages'].append(message)
    st.session_state['all_messages'].append(all_message_template)


response_container = st.container() #chat history
container = st.container() #text box
init_message = "Hello! I'm AVA - your personal realtor. \nBefore we get started, what is your good name?"


if 'user_messages' not in st.session_state:
    st.session_state['user_messages'] = []
if 'ai_messages' not in st.session_state:
    st.session_state['ai_messages'] = []
if 'all_messages' not in st.session_state:
    st.session_state['all_messages'] = []
    update_message_state('assistant', init_message)
if 'intent' not in st.session_state:
    st.session_state['intent'] = ['0']
if 'name' not in st.session_state:
    st.session_state['name'] = []
if 'email' not in st.session_state:
    st.session_state['email'] = []
if 'number' not in st.session_state:
    st.session_state['number'] = []
if 'strategy' not in st.session_state:
    st.session_state['strategy'] = []
if 'budget' not in st.session_state:
    st.session_state['budget'] = []
if 'property_type' not in st.session_state:
    st.session_state['property_type'] = []


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
                # print(i, ':', len(st.session_state['user_messages']))
            message(st.session_state['ai_messages'][-1], key=str(-1))
            