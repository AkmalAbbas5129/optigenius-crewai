from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_experimental.utilities import PythonREPL
from langchain_core.pydantic_v1 import BaseModel, Field
import streamlit as st
import os

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

python_repl = PythonREPL()


class AgentState(TypedDict):
    optimization_task: str  # what is the task to perform e.g customer order fullfillment,
    problem_statement: str  # Full statement with problem,objective,constraint
    python_pulp_code: str  # Code in python pulp
    optimization_answer: str  # Answer to the statement
    report: str  # Report





# """
# You are a python expert who can write code to solve any optimization problem using Pulp library.
#     you only generate code and nothing else. Always include the needed libraries and write a perfect
#     code without any syntax and logical error. The code will always include print statements to print the
#     results of the optimization.
#
#     I will give you an optimization task, you will go by following pointers.
#
#     1. Understand the problem statement, objective and constraints.
#     2. Write Python code and nothing else.
# """

def generate_pulp_code_for_problem(state: AgentState) -> AgentState:
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
    
    Problem Statement, Objective, Constraint:
    {problem_statement}
    
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

    problem_statement = state["problem_statement"]
    optimization_task = state["optimization_task"]
    chain = prompt | azure_llm

    code = chain.invoke(
        {
            "optimization_task": optimization_task,
            "problem_statement": problem_statement
        }
    )

    state["python_pulp_code"] = code.content

    return state


def code_executor(state: AgentState) -> AgentState:
    try:
        from autogen import ConversableAgent
        from autogen.coding import LocalCommandLineCodeExecutor

        # Create a temporary directory to store the code files.
        temp_dir = "code_temp"

        # Create a local command line code executor.
        executor = LocalCommandLineCodeExecutor(
            timeout=10,  # Timeout for each code execution in seconds.
            work_dir=temp_dir,  # Use the temporary directory to store the code files.
        )

        # Create an agent with code executor configuration.
        code_executor_agent = ConversableAgent(
            "code_executor_agent",
            llm_config=False,  # Turn off LLM for this agent.
            code_execution_config={"executor": executor},  # Use the local command line code executor.
        )

        code = state["python_pulp_code"]
        reply = code_executor_agent.generate_reply(messages=[{"role": "user", "content": code}])
        state["optimization_answer"] = reply
        print(reply)
        return state
    except Exception as ex:
        print(f"Exception arised in code executer node: {ex}")

    # try:
    #     pulp_code = state["python_pulp_code"]
    #     answer = python_repl.run(pulp_code)
    #     state["optimization_answer"] = answer
    #     return state
    # except Exception as ex:
    #     print(f"Exception arised in code executer node: {ex}")


def report_writer(state: AgentState) -> AgentState:
    sys_prompt = """
    You are an expert in writing reports in such a way that any one who reads it can easily understand it.
    Please use proper formatting and easy to understand vocabulary to write a report. Always use plain english and 
    not use any latex or other expressions to show calculations.
    
    One of your sub ordinate has received an optimization problem and he has used the PuLP library to 
    solve the optimization problem. Now he is giving you the optimization problem, problem statement, objective and 
    constraints. Also he has given you the execution result of the code. 
    
    1. In report explain the Given data and what is intended by the given data
    2. Explain the solution and calculations.
    3. Write Conclusion with respect to objective by explaining problem statement and constraints.
    4. Give suggestions as an expert.
    
    Please write a report according to following.
    
    Optimization Problem:
    {optimization}
    
    Problem Statements,Objective and Constraint:
    {problem}
    
    Result of Code Execution according to problem:
    {code_execution_result}
    
    Report:
    [Write report here to show beautifully compatible in markdown format]
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

    problem_statement = state["problem_statement"]
    optimization_task = state["optimization_task"]
    code_result = state["optimization_answer"]
    chain = prompt | azure_llm

    code = chain.invoke(
        {
            "optimization": optimization_task,
            "problem": problem_statement,
            "code_execution_result": code_result
        }
    )

    state["report"] = code.content

    return state


class CodeReviewGrade(BaseModel):
    """Binary score for Reviewing Score."""

    # binary_score: str = Field(
    #     description="The article is about football transfers, 'yes' or 'no'"
    # )

    binary_score: str = Field(
        description="The code is correct and include all relevant libraries and there is no syntax and logical error, "
                    "'yes' or 'no'"
    )


def code_reviewer(state: AgentState) -> AgentState:
    system = """
    You are an expert in python code reviewer. I will give you a code which is solving an optimization
    problem using python and PuLP library. 
    
    Please review the code and check that if the code 
    
    1. includes all the relevant libraries.
    2. No syntax error in it.
    3. No logical error in it.
    5. Proper print statements are used to output.
    
    Provide a binary score 'yes' or 'no' to indicate if the code is reviewed or not."""

    human_message = """    
    Code:
    {code}
    
    Binary Score:
    """
    grade_prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", human_message)]
    )

    optimization_problem = state["optimization_task"]
    problem_statement = state["problem_statement"]
    code = state["python_pulp_code"]

    structured_llm_grader = azure_llm.with_structured_output(CodeReviewGrade)

    evaluator = grade_prompt | structured_llm_grader
    result = evaluator.invoke(
        {
            "optimization_problem": optimization_problem,
            "problem_statement": problem_statement,
            "code": code
        }
    )
    print(f"\nScore: {result.binary_score}\n")
    if result.binary_score == "yes":
        return "code_executor"
    else:
        # print("---" * 50)
        # print(code)
        # print("---" * 50)
        return "code_fixer"


def fix_code(state: AgentState) -> AgentState:
    # optimization_task: str  # what is the task to perform e.g customer order fullfillment,
    # problem_statement: str  # Full statement with problem,objective,constraint
    # python_pulp_code: str  # Code in python pulp
    # optimization_answer: str  # Answer to the statement
    # report: str  # Report

    optimization_task = state["optimization_task"]
    problem_statement = state["problem_statement"]

    system = """
    I want you to act like an Expert Mathematics and Linear Programming Expert who solves optimization 
    problems computationally and the calculations are perfect everytime you solve something.
    Following are the details of the optimization problem. Your job is to understand the problem
    with the help of problem statement, objective to solve and constraints which needs to be followed.
    After understanding please perform the calculation like an expert and find solution to the problem.
    you will output answer to the objective and nothing else."""

    human_message = """
    Optimization task:
    {task}
    
    Problem Statement,Objective and Constraint:
    {problem}
    
    Answer:
    """

    grade_prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", human_message)]
    )

    evaluator = grade_prompt | azure_llm

    result = evaluator.invoke(
        {
            "task": optimization_task,
            "problem": problem_statement
        }
    )

    # print(result.content)
    state["optimization_answer"] = result.content

    return state

    # system = """
    # As an expert programmer who can debug and fix the code."""
    #
    # human_message = """
    # Optimization task is about:
    # {optimization_problem}
    #
    # Problem Statement, Objective, Constraints:
    # {problem_statement}
    #
    # Code:
    # {code}
    #
    # Binary Score:
    # """
    # grade_prompt = ChatPromptTemplate.from_messages(
    #     [("system", system), ("human", human_message)]
    # )
    #
    # optimization_problem = state["optimization_task"]
    # problem_statement = state["problem_statement"]
    # code = state["python_pulp_code"]
    #
    # structured_llm_grader = azure_llm.with_structured_output(CodeReviewGrade)
    #
    # evaluator = grade_prompt | structured_llm_grader
    # result = evaluator.invoke(
    #     {
    #         "optimization_problem": optimization_problem,
    #         "problem_statement": problem_statement,
    #         "code": code
    #     }
    # )


def evaluator_node(state: AgentState) -> AgentState:
    print(f"Evaluating the Code.....")
    return state


def get_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("code_writer", generate_pulp_code_for_problem)
    workflow.add_node("code_executor", code_executor)
    workflow.add_node("expert_report_writer", report_writer)
    workflow.add_node("evaluator_node", evaluator_node)
    workflow.add_node("code_fixer", fix_code)

    workflow.set_entry_point("code_writer")

    workflow.add_edge("code_writer", "evaluator_node")
    # workflow.add_edge("code_writer", "code_executor")
    workflow.add_conditional_edges(
        "evaluator_node", code_reviewer, {"code_executor": "code_executor", "code_fixer": "code_fixer"}
    )

    workflow.add_edge("code_fixer", "expert_report_writer")
    workflow.add_edge("code_executor", "expert_report_writer")
    workflow.add_edge("expert_report_writer", END)
    app = workflow.compile()
    return app


def custom_order_fulfillment(secnario, problem_statement):
    graph = get_graph()
    initial_state = {"problem_statement": problem_statement,
                     "optimization_task": secnario}
    result = graph.invoke(initial_state)
    return result["report"]


def demand_supply_matching(secnario, problem_statement):
    graph = get_graph()
    initial_state = {"problem_statement": problem_statement,
                     "optimization_task": secnario}
    result = graph.invoke(initial_state)
    return result["report"]


def supplier_risk_optimization(secnario, problem_statement):
    graph = get_graph()
    initial_state = {"problem_statement": problem_statement,
                     "optimization_task": secnario}
    result = graph.invoke(initial_state)
    return result["report"]


def demand_forecasting_optimization(secnario, problem_statement):
    graph = get_graph()
    initial_state = {"problem_statement": problem_statement,
                     "optimization_task": secnario}
    result = graph.invoke(initial_state)
    return result["report"]


def generate_report_for_scenario(scenario, problem_statement):
    report = "Default Report"
    if scenario == "Customer Order Fulfillment":
        report = custom_order_fulfillment(scenario,problem_statement)
    elif scenario == "Demand-Supply Matching":
        report = demand_supply_matching(scenario,problem_statement)
    elif scenario == "Supplier Risk Assessment":
        report = supplier_risk_optimization(scenario,problem_statement)
    elif scenario == "Demand Forecasting":
        report = supplier_risk_optimization(scenario,problem_statement)

    return report


if __name__ == "__main__":
    # print(custom_order_fulfillment())
    # demand_supply_matching()
    print(demand_supply_matching())
    # print(supplier_risk_optimization())
