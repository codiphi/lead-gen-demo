from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import streamlit as st

def affirmmation_response(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("If message below is affirmation reply with the word 'yes' and if it is not then reply with the word 'no' \n message:{response}.")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response.lower()


def off_plan_response(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("Based on the conversation, decide if the user wants an off-plan property or ready to move \n if off-plan reply with '0' \n if ready to move reply with '1' \n conversation:{response} \n\n only reply with '0' or '1'")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response


def budget_response(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("Based on the conversation, echo how much money is the users budget in AED currency \n conversation:{response}")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response


def investment_response(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("Based on the conversation, decide if the user wants to buy a property to invest or to live in \n if intention is to invest then reply with '0' \n if intention is to live in it reply with '1' \n conversation:{response} \n\n only reply with '0' or '1'")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response


def extract_name(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("Based on the conversation, extract the name of the user \n conversation:{response} \n\n only reply with the name of the user, if there is no name reply 'None'")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response


def extract_email(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("Based on the conversation, extract the email of the user \n conversation:{response} \n\n only reply with the email of the user, if there is no name reply 'None'")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response


def extract_number(prompt):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("Based on the conversation, extract the email of the phone number of the user \n conversation:{response} \n\n only reply with the phone number of the user, if there is no name reply 'None'")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"response":prompt})
    return response
