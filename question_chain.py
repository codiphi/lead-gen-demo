from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import streamlit as st


def investment_question(prompt, conversation):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("You're a realtor and you are mid conversation with a client named {name}.\nFrame a question and continue the conversation to ask if the client is looking to buy a property as an investment or to live in. \n\n conversation:{conversation}")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"name":prompt, "conversation":conversation})
    return response


def budget_question(prompt, conversation):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("You're a realtor and you are mid conversation with a client named {name} and below is the conversation so far.\nFrame a question and continue the conversation to ask the client what is their budget. \n\n conversation:{conversation}")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"name":prompt, "conversation":conversation})
    return response


def property_type_question(prompt, conversation):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("You're a realtor and you are mid conversation with a client named {name} and they just gave you valuble information.\nFrame a question and continue the conversation to ask the client if they want a ready property or if they want an off-plan property, Give a one line description of each. \n\n conversation:{conversation}")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"name":prompt, "conversation":conversation})
    return response



def contact_question(prompt, conversation):
    model = ChatOpenAI(openai_api_key = st.secrets["OPENAI_API_KEY"] )
    prompt = ChatPromptTemplate.from_template("You're a realtor and you are mid conversation with a client named {name} and they just gave you valuble information.\nFrame a question and continue the conversation to ask the client for their email address and phone number to contaact them. \n\n conversation:{conversation}")
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"name":prompt, "conversation":conversation})
    return response