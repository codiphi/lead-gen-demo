
##################################################################################


################################
import os
import streamlit as st
from streamlit_chat import message # type: ignore
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from local import extract_and_validate_travel_details
from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from ocr import ocr
from rag import answer
from langchain.prompts import ChatPromptTemplate
from langchain import LLMChain
from router import init_router
import time
################################

# Loading the question-answering chain

################################

os.environ["OPENAI_API_KEY"] = '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'
llm = ChatOpenAI(model="gpt-4")

##################################################################################



def update_session_state(user_info, a):
    # Map keys from dictionary 'a' to keys in 'user_info'
    mapping = {
        'Passport_Name': 'Name',
        'Date_of_Birth': 'Date of birth',
        'How_many_days_are_you_visiting_for':'Number of days visiting', 
        'Destination_city':'Destination City',
        'email': 'Email'
    }


    # Update 'user_info' with values from 'a'
    for key_a, key_user_info in mapping.items():
        if key_a in a and a[key_a] != None:
            user_info[key_user_info] = a[key_a]
    
    # Update the session state variable
    st.session_state['user_info'] = [user_info]
    
    # Check for missing or empty keys in 'user_info'
    missing_or_empty_keys = [key for key, value in user_info.items() if not value]
    
    return missing_or_empty_keys

##################################################################################

def ask_for_info(ask_for = ['Passport Name','Date of Birth','Destination city','How many days are you visiting for?', 'Email']):
    len_ask_for = len(ask_for)
    # # prompt template 1
    # first_prompt = ChatPromptTemplate.from_template(
    #     "Below is are some things to ask the user for in a coversation way. you should only ask one question at a time even if you don't get all the info \
    #     don't ask as a list! Don't greet the user! Don't say Hi and Do not address anyone at the start.Explain you need to get some info. If the ask_for list is empty then thank them and ask how you can help them \n\n \
    #     ### ask_for list: {ask_for}"
    # )
    # prompt template 1
    first_prompt = ChatPromptTemplate.from_template(
        f"You are an assistant getting some information from future travellers, and this is in between an ongoing conversation so don't greet or say hi or address the person. and Don't start wth the word of Assistant: or anything else, just continue the conversation. \
            There are currently {len_ask_for} points of information that you have left to ask. \
            IF there are 5 points of information left to ask, that means you have just started the application process (don't mention what type of application it is, just application) and \
            so address and say that the application process is starting, ENSURE TO MENTION AT THIS STAGE THAT THEY CAN UPLOAD PASSPORT TO EXTRACT SOME INFORMATION and ask for one or two of these points of information: {ask_for} \
            IF there are less than 5 points of information (for reference - current points of information to collect:{len_ask_for}) \
            then make sure you are talking as if you already asked for something previously and ask for any one or two of those points. \
            Have a cheerful and polite personality and but don't say things that are unessecary to your goal and if there are less than 5 points of information ensure you are assuming you asked a question and you received an answer and you're asking the next question. "
    )


    # info_gathering_chain
    info_gathering_chain = LLMChain(llm=llm, prompt=first_prompt)
    ai_chat = info_gathering_chain.run(ask_for=ask_for)
    return ai_chat 
##################################################################################




def start_application():
    return "we are starting the application, will add confirmation later, type anything for now"


def complete_application(user_info: dict, missing_user_info):
    if len([key for key, value in user_info.items() if not value]) == 0:
        st.session_state['flow_state'] = ['1']
        return f"We will be sending in the following information for your application process \n \n {user_info} \n \n Thank you for your time, anything else I can help you with?"
    else:
        res = str(ask_for_info(missing_user_info))
        return res

router_chain = init_router()




# # Setting page title and header
# st.set_page_config(page_title="AVA", page_icon=":robot_face:")
# st.markdown("<h1 style='text-align: center;'>Virtual Assistant</h1>", unsafe_allow_html=True)



# if 'user_info' not in st.session_state:
#     st.session_state['user_info'] = [{"Name":"", "Date of birth":"", "Number of days visiting":"", "Destination City":"", "Email":""}]




# # Sidebar - Document Uploader and some buttons
# st.sidebar.title("Document Uploader")
# with st.sidebar:
#     uploaded_files = st.file_uploader(" ", accept_multiple_files=True, type=None)

# if uploaded_files:
#     # Load the data and perform preprocessing only if it hasn't been loaded before
#     if "processed_data" not in st.session_state:
#         # Load the data from uploaded PDF files
#         # documents = []
#         if uploaded_files:
#             for uploaded_file in uploaded_files:
#                 # Get the full file path of the uploaded file
#                 file_path = os.path.join(os.getcwd(), uploaded_file.name)

#                 # Save the uploaded file to disk
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getvalue())

#                 # Determine the file type based on its extension
#                 file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
#                 if file_extension in {'.jpg', '.png'}:
#                     # Use UnstructuredImageLoader to load image file
#                     # loader = UnstructuredImageLoader(file_path)
#                     pass
#                 else:
#                     # Handle unsupported file types here if needed
#                     st.warning(f"Unsupported file type: {file_extension}")
#                     continue
                
#                 ocr_extract = ocr(file_path)
#                 st.session_state['user_info'][0]["Date of birth"] = ocr_extract[0]
#                 st.session_state['user_info'][0]["Name"] = ocr_extract[1]
                



def generate_response(prompt):
    # print('sesh0')
    # if st.session_state['flow_state'][0] == '1':
    #     print('sesh1')
    #     intent = router_chain(prompt)
    #     if intent['destination'] == 'Visa Application':
    #         print('sesh1.3')
    #         st.session_state['flow_state'] = ['0']
    #     else:
    #         print('sesh1.5')
    #         ans = str(answer(prompt))
    #         response = ans
    # if st.session_state['flow_state'][0] == '0':
    #     print('sesh2')
    #     user_info = st.session_state['user_info'][0]
    #     a = vars(extract_and_validate_travel_details(prompt))
    #     missing_information = update_session_state(st.session_state['user_info'][0], a)
    #     response = complete_application(user_info, missing_information)
    # else:
    #     print("3")
    #     pass

    # st.session_state['messages'].append({"role": "assistant", "content": response})
    # return response
    return prompt


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
        time.sleep(4)
        response = f"robot response to - {user_input}"
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
            






# with st.sidebar:
#     uploaded_files = st.file_uploader(" ", accept_multiple_files=True, type=None)


# if uploaded_files:
#     # Load the data and perform preprocessing only if it hasn't been loaded before
#     if "processed_data" not in st.session_state:
#         # Load the data from uploaded PDF files
#         # documents = []
#         if uploaded_files:
#             for uploaded_file in uploaded_files:
#                 # Get the full file path of the uploaded file
#                 file_path = os.path.join(os.getcwd(), uploaded_file.name)

#                 # Save the uploaded file to disk
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getvalue())

#                 # Determine the file type based on its extension
#                 file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
#                 if file_extension in {'.jpg', '.png'}:
#                     # Use UnstructuredImageLoader to load image file
#                     # loader = UnstructuredImageLoader(file_path)
#                     pass
#                 else:
#                     # Handle unsupported file types here if needed
#                     st.warning(f"Unsupported file type: {file_extension}")
#                     continue
                
#                 ocr_extract = ocr(file_path)
#                 st.session_state['user_info'][0]["Date of birth"] = ocr_extract[0]
#                 st.session_state['user_info'][0]["Name"] = ocr_extract[1]