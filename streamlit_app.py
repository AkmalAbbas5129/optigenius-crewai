### CrewAI Dependable Libraries
import os
from langchain_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

###Streamlit Dependable Libraries
import streamlit as st
import base64

# GEtting Environement Variables
from dotenv import load_dotenv
load_dotenv()

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
st.write("OptiGenius, a multi-agent systems powered by CrewAI and Streamlit. It uses multi-agentic approach and code execution tools incorporated in CrewAI to solve Resource Optimization Problems.")

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

# # Problem statement for the optimization problem
# problem_statement = """A snack bar cooks and sells hamburgers and hot dogs during football games. To stay in business, it must sell at least 10 hamburgers but can not cook more than 40. It must also sell at least 30 hot dogs, but can not cook more than 70. The snack bar can not cook more than 90 items total. The profit on a hamburger is 33 cents, and the profit on a hot dog is 21 cents. How many of each item should it sell to make the maximum profit?"""

# Task for solving the optimization problem
cli_task = Task(
    description=user_input,
    agent=coding_agent,
    expected_output='Desired output in python formatted context',
    # llm=azure_llm
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
    2. Optimization Answer
    3. Conclusion
    """,
    agent=report_agent,
    expected_output='''A structured report in markdown format of the solution with the following headings as an Final Answer:

    1. Problem Statement
    2. Constraints
    2. Optimization Answer
    3. Conclusion'''
)

# Submit button
with col1:
    if st.button("Submit"):
        # Initialize progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        output_text = st.empty()

        # Display a spinner while the solution is being generated
        with st.spinner("Processing your request... Please wait."):
            # Update the status for initializing the agent
            progress_bar.progress(10)
            status_text.markdown("**Initializing agents...**")

            # Create a crew and add the task
            analysis_crew = Crew(
                agents=[coding_agent, report_agent],
                tasks=[cli_task, report_task],
                process=Process.sequential,
            )

            # Define a function to capture and display agent output in real-time
            def stream_output(agent_output):
                output_text.markdown(f"**Agent Output:**\n\n{agent_output}")
                progress_bar.progress(50)  # Update progress based on task completion

            # Execute the crew with output streaming
            result = analysis_crew.kickoff(callback=stream_output)

            # Update the status during task execution
            progress_bar.progress(70)
            status_text.markdown("**Generating solution...**")

            try:
                os.remove('trained_agents_data.pkl')
            except Exception as ex:
                print("Exception has occurred")

            # Update the status when the task is complete
            progress_bar.progress(100)
            status_text.markdown("**Task completed successfully!**")

        # Display the final result in a styled container
        st.markdown("## 🧠 Optimization Solution")
        st.markdown(
            """
            <div style="
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            ">
                <h3 style="color: #2c3e50;">Final Result:</h3>
                <p style="font-size: 16px; color: #34495e;">
                    {}</p>
            </div>
            """.format(result),
            unsafe_allow_html=True
        )



# Clear button
with col2:
    if st.button("Clear"):
        # Clear the input field (refresh the page)
        st.rerun()
