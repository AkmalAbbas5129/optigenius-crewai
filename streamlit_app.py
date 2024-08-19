import os
import streamlit as st
import base64
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from crewai import Agent, Task, Crew, Process
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

# Load environment variables
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

# Example problems
examples = {
    "Fly High Airlines": """
Fly High Airlines sells business class and tourist class seats for its charter flights. To charter a plane, at least 5 Business class tickets must be sold and at least 9 tourist class tickets must be sold. The plane does not hold more than 30 passengers. Fly-High makes $40 profit for each business class ticket sold and $45 profit for each tourist class ticket sold. For Fly-High Airlines to maximize profits, how many tourists class seats should they sell?

Objective:
How many tourist class seats should they sell to maximize the profits?

Constraints:
- Plane does not hold more than 30 passengers.
- At least 5 business class tickets must be sold.
- At least 9 tourist class tickets must be sold.
""",
    "ABC E-commerce Company": """
ABC E-commerce Company needs to determine the optimal number of ads to place on Social Media, Search Engines, and Display Ads to maximize the number of new customers, given budget constraints and platform-specific limits.

Objective:
Maximize the total number of new customers acquired from advertising.

Constraints:
- Budget Constraint: The total advertising budget is $50,000.
- Cost per Ad:
  - Social Media: $200 per ad.
  - Search Engines: $300 per ad.
  - Display Ads: $250 per ad.
- Expected New Customers per Ad:
  - Social Media: 50 new customers per ad.
  - Search Engines: 80 new customers per ad.
  - Display Ads: 60 new customers per ad.
- Non-Negativity Constraint: The number of ads placed on each platform must be non-negative.
"""
}

# Title and description
st.markdown(title_html, unsafe_allow_html=True)
st.write("OptiGenius, a multi-agent system powered by CrewAI and Streamlit. It uses a multi-agent approach and code execution tools incorporated in CrewAI to solve Resource Optimization Problems.")

# Dropdown menu for selecting an example problem
problem_selection = st.selectbox("Select an example problem:", ["", "Fly High Airlines", "ABC E-commerce Company"])

# Text input field
if problem_selection:
    user_input = st.text_area("Enter Problem Statement:", examples[problem_selection], height=300)
else:
    user_input = st.text_area("Enter Problem Statement:", height=300)

# Create two columns for the buttons
col1, col2 = st.columns(2)

### Create an agent with code execution enabled
coding_agent = Agent(
    role='Software Engineer',
    goal='Solve resource optimization problem using Pulp library and execute using code execution.',
    backstory='You are a helpful AI assistant. Solve tasks using your coding and language skills. You must ensure that the code is properly formatted and wrapped according to Python REPL executor. For Example: ```{"command": "from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value\n"}```.',
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
    goal='Generate a concise report based on the given solution.',
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
    expected_output='''A structured report in markdown format of the solution with the following headings as an Final Answer:
    1. Problem Statement
    2. Constraints
    3. Optimization Answer
    4. Conclusion'''
)

# Submit button
with col1:
    if st.button("Submit"):
        # Initialize progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

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

            # Update the status for starting the task
            progress_bar.progress(30)
            status_text.markdown("**Starting task execution...**")

            # Execute the crew
            result = analysis_crew.kickoff()

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

        # Display the result in a styled container
        st.markdown("## 🧠 Optimization Solution")
        st.markdown(
            """
            <div style="
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            ">
                <h3 style="color: #2c3e50;">Result:</h3>
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
