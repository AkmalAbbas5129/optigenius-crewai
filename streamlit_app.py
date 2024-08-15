### CrewAI Dependable Libraries
import os
from langchain_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

### Streamlit Dependable Libraries
import streamlit as st
import base64

# Getting Environment Variables
# from dotenv import load_dotenv
# load_dotenv()

os.environ["AZURE_OPENAI_API_KEY"] = st.secrets["openai_api_key"]
os.environ["AZURE_OPENAI_ENDPOINT"] = st.secrets["azure_endpoint"]
os.environ["AZURE_OPENAI_API_VERSION"] = st.secrets["api_version"]
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = st.secrets["deployment_name"]
os.environ["OPENAI_MODEL_NAME"]="gpt-35-turbo-16k"

# Initialize Azure OpenAI LLM
azure_llm = AzureChatOpenAI(
    openai_api_version=st.secrets["api_version"],
    azure_deployment=st.secrets["deployment_name"],
    model="gpt-35-turbo-16k"
)

# Initialize Python REPL tool
python_repl = PythonREPL()
coding_agent_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command in Python REPL dictionary format. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

# Set the layout to wide
st.set_page_config(layout="wide")

# Custom CSS to adjust the width of the markdown container
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{
        max-width: 100%;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        img_str = base64.b64encode(image_file.read()).decode()
    return img_str

# Paths to your local icons
icon1_path = "crewai.jpg"  # Replace with the path to your first icon
icon2_path = "streamlit.png"  # Replace with the path to your second icon
sidebar_logo_path = "systemsltd.png"  # Replace with the path to your sidebar logo

# Convert icons to base64
icon1_base64 = get_image_base64(icon1_path)
icon2_base64 = get_image_base64(icon2_path)
sidebar_logo_base64 = get_image_base64(sidebar_logo_path)

# Function to create image HTML tag
def image_html(base64_str, height="50px"):
    return f'<img src="data:image/png;base64,{base64_str}" style="height:{height}; margin-left:10px;">'

# Title with icons
title_html = f"""
<h1 style="display: flex; align-items: center;">
    OptiGenius  .  .  . {image_html(icon1_base64)} {image_html(icon2_base64)}
</h1>
"""

# Injecting the title with icons using markdown
st.markdown(title_html, unsafe_allow_html=True)

# Sidebar with logo
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{sidebar_logo_base64}" style="width: 100%; max-width: 150px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

# Description about the app
st.write("OptiGenius, a multi-agent system powered by CrewAI and Streamlit. It uses a multi-agentic approach and code execution tools incorporated in CrewAI to solve Resource Optimization Problems.")

# Text input field
user_input = st.text_area("Enter Problem Statement:")

# Create two columns for the buttons
col1, col2 = st.columns(2)

### Create an agent with code execution enabled
coding_agent = Agent(
    role='Software Engineer',
    goal='Solve resource optimization problem using Pulp library and execute using code execution.',
    backstory='''You are a helpful AI assistant. Solve tasks using your coding and language skills. You must ensure that the code is properly formatted and wrapped according to Python REPL executor.'
    # For Example: ```{"command": "from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value\n"}```.''',
    verbose=True,
    tools=[coding_agent_tool],
    allow_code_execution=True,
    llm=azure_llm
)

# Task for solving the optimization problem
cli_task = Task(
    description=user_input,
    agent=coding_agent,
    expected_output='Desired output in python formatted context',
)

report_agent = Agent(
    role='Technical Writer',
    goal='Generate a concise report based on the given solution.',# Use Executor tool for saving report in .md file.',
    backstory='You are an expert in creating structured and concise reports based on provided data. Your goal is to present the information in a clear and engaging manner.',
    memory=True,
    verbose=True,
    llm=azure_llm
)

# Task for generating the report
report_task = Task(
    description="""Generate a concise report based on the previous given solution with the following headings:
    1. Problem Statement
    2. Constraints
    3. Optimization Answer
    4. Conclusion
    """,
    agent=report_agent,
    expected_output='''A structured report in markdown format of the solution with the following headings as a Final Answer:

    1. Problem Statement
    2. Constraints
    3. Optimization Answer
    4. Conclusion'''
)

# Submit button
with col1:
    if st.button("Submit"):
        with st.spinner("OptiGenius is finding the solution..."):
            st.toast("OptiGenius is finding the solution...")

            # Create a crew and add the task
            analysis_crew = Crew(
                agents=[coding_agent, report_agent],
                tasks=[cli_task, report_task],
                process=Process.sequential,
            )

            # Execute the crew
            result = analysis_crew.kickoff()

        # Output box
        # st.markdown("### Final Answer:")
        # st.markdown(result)

        # Styled Output
        st.markdown("---")
        st.markdown("### Detailed Report")
        st.markdown(result, unsafe_allow_html=True)

        # Try to remove the saved data file if it exists
        try:
            os.remove('trained_agents_data.pkl')
        except Exception as ex:
            print("An exception has occurred:", ex)

# Clear button
with col2:
    if st.button("Clear"):
        # Clear the input field (refresh the page)
        st.rerun()
### CrewAI Dependable Libraries
import os
from langchain_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

### Streamlit Dependable Libraries
import streamlit as st
import base64

# Getting Environment Variables
# from dotenv import load_dotenv
# load_dotenv()

os.environ["AZURE_OPENAI_API_KEY"] = st.secrets["openai_api_key"]
os.environ["AZURE_OPENAI_ENDPOINT"] = st.secrets["azure_endpoint"]
os.environ["AZURE_OPENAI_API_VERSION"] = st.secrets["api_version"]
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = st.secrets["deployment_name"]
os.environ["OPENAI_MODEL_NAME"]="gpt-35-turbo-16k"

# Initialize Azure OpenAI LLM
azure_llm = AzureChatOpenAI(
    openai_api_version=st.secrets["api_version"],
    azure_deployment=st.secrets["deployment_name"],
)

# Initialize Python REPL tool
python_repl = PythonREPL()
coding_agent_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command in Python REPL dictionary format. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

# Set the layout to wide
# st.set_page_config(layout="wide")

# Custom CSS to adjust the width of the markdown container
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{
        max-width: 100%;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        img_str = base64.b64encode(image_file.read()).decode()
    return img_str

# Paths to your local icons
icon1_path = "crewai.jpg"  # Replace with the path to your first icon
icon2_path = "streamlit.png"  # Replace with the path to your second icon
sidebar_logo_path = "systemsltd.png"  # Replace with the path to your sidebar logo

# Convert icons to base64
icon1_base64 = get_image_base64(icon1_path)
icon2_base64 = get_image_base64(icon2_path)
sidebar_logo_base64 = get_image_base64(sidebar_logo_path)

# Function to create image HTML tag
def image_html(base64_str, height="50px"):
    return f'<img src="data:image/png;base64,{base64_str}" style="height:{height}; margin-left:10px;">'

# Title with icons
title_html = f"""
<h1 style="display: flex; align-items: center;">
    OptiGenius  .  .  . {image_html(icon1_base64)} {image_html(icon2_base64)}
</h1>
"""

# Injecting the title with icons using markdown
st.markdown(title_html, unsafe_allow_html=True)

# Sidebar with logo
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{sidebar_logo_base64}" style="width: 100%; max-width: 150px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

# Description about the app
st.write("OptiGenius, a multi-agent system powered by CrewAI and Streamlit. It uses a multi-agentic approach and code execution tools incorporated in CrewAI to solve Resource Optimization Problems.")

# Text input field
user_input = st.text_area("Enter Problem Statement:")

# Create two columns for the buttons
col1, col2 = st.columns(2)

### Create an agent with code execution enabled
coding_agent = Agent(
    role='Software Engineer',
    goal='Solve resource optimization problem using Pulp library and execute using code execution.',
    backstory='''You are a helpful AI assistant. Solve tasks using your coding and language skills. You must ensure that the code is properly formatted and wrapped according to Python REPL executor.'
    # For Example: ```{"command": "from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value\n"}```.''',
    verbose=True,
    tools=[coding_agent_tool],
    allow_code_execution=True,
    llm=azure_llm
)

# Task for solving the optimization problem
cli_task = Task(
    description=user_input,
    agent=coding_agent,
    expected_output='Desired output in python formatted context',
)

report_agent = Agent(
    role='Technical Writer',
    goal='Generate a concise report based on the given solution.',# Use Executor tool for saving report in .md file.',
    backstory='You are an expert in creating structured and concise reports based on provided data. Your goal is to present the information in a clear and engaging manner.',
    memory=True,
    verbose=True,
    llm=azure_llm
)

# Task for generating the report
report_task = Task(
    description="""Generate a concise report based on the previous given solution with the following headings:
    1. Problem Statement
    2. Constraints
    3. Optimization Answer
    4. Conclusion
    """,
    agent=report_agent,
    expected_output='''A structured report in markdown format of the solution with the following headings as a Final Answer:

    1. Problem Statement
    2. Constraints
    3. Optimization Answer
    4. Conclusion'''
)

# Submit button
with col1:
    if st.button("Submit"):
        with st.spinner("OptiGenius is finding the solution..."):
            st.toast("OptiGenius is finding the solution...")

            # Create a crew and add the task
            analysis_crew = Crew(
                agents=[coding_agent, report_agent],
                tasks=[cli_task, report_task],
                process=Process.sequential,
            )

            # Execute the crew
            result = analysis_crew.kickoff()

        # Output box
        # st.markdown("### Final Answer:")
        # st.markdown(result)

        # Styled Output
        st.markdown("---")
        st.markdown("### Detailed Report")
        st.markdown(result, unsafe_allow_html=True)

        # Try to remove the saved data file if it exists
        try:
            os.remove('trained_agents_data.pkl')
        except Exception as ex:
            print("An exception has occurred:", ex)

# Clear button
with col2:
    if st.button("Clear"):
        # Clear the input field (refresh the page)
        st.rerun()
