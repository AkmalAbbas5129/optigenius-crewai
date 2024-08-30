import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

os.environ["AZURE_OPENAI_API_KEY"] = st.secrets["openai_api_key"]
os.environ["AZURE_OPENAI_ENDPOINT"] = st.secrets["azure_endpoint"]
os.environ["AZURE_OPENAI_API_VERSION"] = st.secrets["api_version"]
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = st.secrets["deployment_name"]
os.environ["OPENAI_MODEL_NAME"]="gpt-4o"

# Initialize Azure OpenAI LLM
azure_llm = AzureChatOpenAI(
    openai_api_version=st.secrets["api_version"],
    azure_deployment=st.secrets["deployment_name"],
    model="gpt-4o"
)

def generate_optimization(scenario, data):
    sys_prompt = """
    You are of supply chain who can generate problem statement, objective and constraints according to 
    {problem}.
    I will give you data in python dictionary and then you will only generate following information and nothing else.

    1. Given Data
    2. Problem statement
    3. Objective
    4. Constraints

    Data:
    {data}

    Output should follow this format

    Given Data:
    [Write data here in natural language]

    Problem Statement:
    [Please write problem statement according to given data which is being faced]

    Objective:
    [Objective to optimize in question format]

    Constraints:
    [List of Constraints]
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                sys_prompt,
            ),
            # ("human", "{input}"),
        ]
    )

    chain = prompt | azure_llm
    ans = chain.invoke(
        {
            "problem": scenario,
            "data": data,
            # "input": "I love programming.",
        }
    )

    return ans.content


def generate_data_info_in_natural_language(scenario,data):
    system = """
    I will give you predictions from Machine Learning Model for a Scenario. Write Predicted data in natural language. 
    """

    human_message = """    

    Predictions:
    {predictions}
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", human_message)]
    )

    chain = prompt | azure_llm

    data_in_nl = chain.invoke(
        {
            # "scenario": scenario,
            "predictions": data
        }
    )

    return data_in_nl.content
