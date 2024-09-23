import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

os.environ["AZURE_OPENAI_API_KEY"] = st.secrets["openai_api_key"]
os.environ["AZURE_OPENAI_ENDPOINT"] = st.secrets["azure_endpoint"]
os.environ["AZURE_OPENAI_API_VERSION"] = st.secrets["api_version"]
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = st.secrets["deployment_name"]
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

# Initialize Azure OpenAI LLM
azure_llm = AzureChatOpenAI(
    openai_api_version=st.secrets["api_version"],
    azure_deployment=st.secrets["deployment_name"],
    model="gpt-4o"
)


def generate_pulp_code_for_problem(optimization_task, problem_statment, objective, constraint, data):
    sys_prompt = """
    Act as a Python developer. Write a code to solve optimization task using PuLP library.
    Must ensure that the code is properly formatted and wrapped according to Python REPL executor.
    Only use variables defined in the code and make sure there is no syntax/logical errors.
    Always recheck the code to fix error. 
    If there is an error arise in your code i will fine you 1000$ and will sue you.
    Just output code and nothing else.

    Following is the optimization task:
    Optimization Task:
    {optimization_task}
    
    Data:
    {data}

    Problem Statement:
    {problem_statement}
    
    Objective:
    {objective}
    
    Constraint:
    {constraint}

    Code:
    [Write code here]
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

    code = chain.invoke(
        {
            "optimization_task": optimization_task,
            "problem_statement": problem_statment,
            "objective": objective,
            "constraint": constraint,
            "data": data
        }
    )

    code = code.content

    return code


# then you will switch role to
# being an expert writer and will write the report and conclusion in such a way that layman can understand it.
# Please write your responses in concise and understandable way and no longer text.
def solve_optimization_problem(problem_statement, objective, constraints, data):
    # 4. There should be no calculations in the report just text writings.
    template_string = """I want you to act like an Expert Mathematics and Linear Programming Expert who solves 
    optimization problems computationally and the calculations are perfect everytime you solve something. Following 
    are the details of the optimization problem. Your job is to understand the problem with the help of problem 
    statement, objective to solve and constraints which needs to be followed. After understanding please perform the 
    calculation based on the provided data like an expert and find solution to the problem. Once the calculation and 
    optimal solution is found, You will output the results in html format. Keep the results on top and then explain 
    the solution. Don't write the problem statement, objetive and constraint in the solution just use them to solve 
    the problem. Never enclose the output with ```html and ```

    Provided Data:
    {data}
    
    Problem Statement: {problem_statement}
    Objective to solve: {objective}
    Constraints: {constraints}
    
    Please follow the following guidelines and you will be punished if you will not follow
    the guidelines

    1. Recheck the calculation 2-3 times and fix if there is any miscalculation.
    2. Your calculations will always be correct.
    3. Do not output anything extra from your own.
    4. Solution to the answer should be written in a format and language which is easy to understand by anyone.
    5. If there are table to be shown in the solution answer than format them with beautiful formatting with text as white and background transparent.


    Solution Answer in HTML format:
    [Result will be written here]
    [Solution Explanation here]
    """
    prompt_template = ChatPromptTemplate.from_template(template_string)

    chain = prompt_template | azure_llm

    generated_answer = chain.invoke({
        "problem_statement": problem_statement,
        "objective": objective,
        "constraints": constraints,
        "data": data
    })
    print(generated_answer.content)
    return generated_answer.content


def generate_optimization(scenario, data):
    sys_prompt = """
    I will give you a data which has been predicted based on a scenario. 
    Just Output data in html format and nothing else. Also don't enclose output in any quotes.
    
    Scenario:
    {problem}
    
    Data:
    {data}
    
    Markdown:
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


def explain_solution(problem_statement, result):
    system = """
    I will give you optimization problem which is solved by using linear programming python tool PuLP.
    Give answer to the objective and problem statement by looking at optimization results. Don't output anything extra.
    """

    # system = """
    # You are an expert in writing reports in such a way that any one who reads it can easily understand it.
    # Please use proper formatting and easy to understand vocabulary to write a report. Always use plain english and
    # not use any latex or other expressions to show calculations.
    #
    # Your job is to understand the result of the code execution according to the Problem Statements,Objective and Constraint,
    # and then give an answer to the user in the form of report.
    #
    # 1. Always end with conclusion with respect to objective by explaining problem statement and constraints.
    # 2. Give suggestions as an expert.
    # """
    #
    # human_message = """
    # Please write a report according to following.
    #
    # Problem Statements,Objective and Constraint:
    # {problem}
    #
    # Result of Code Execution according to problem:
    # {result}
    #
    # Report:
    # [Write report here to show beautifully compatible in markdown format]
    # """

    human_message = """
    Optimization Problem:
    {problem}

    Optimal Results:
    {result}
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", human_message)]
    )

    chain = prompt | azure_llm

    data_in_nl = chain.invoke(
        {
            "problem": problem_statement,
            "result": result
        }
    )

    return data_in_nl.content


def generate_data_info_in_natural_language(scenario, data):
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
