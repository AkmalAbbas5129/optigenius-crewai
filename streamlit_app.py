import streamlit as st
from streamlit_ace import st_ace
import time
from utils import generate_data_info_in_natural_language, generate_optimization, explain_solution
from supply_chain_scenarios.custom_order_fullfilment import generate_customer_order_fulfillment_predictions
from supply_chain_scenarios.demand_supply_matching import generate_demand_supply_matching_predictions
from supply_chain_scenarios.supplier_risk_management import generate_supplier_risk_predictions
from supply_chain_scenarios.demand_forecasting import generate_demand_forecasting_predictions
from langgraph_crew import generate_report_for_scenario, execute_code


# Function to simulate fetching predictions from an ML model
def get_dummy_predictions(scenario):
    problem_objective_constraint = ""
    data_predicted = ""

    with st.spinner('Predictions are being fetched...'):
        if scenario == "Customer Order Fulfillment":
            data_predicted = generate_customer_order_fulfillment_predictions()
            problem_objective_constraint = generate_optimization(scenario, data_predicted)
        elif scenario == "Demand-Supply Matching":
            data_predicted = generate_demand_supply_matching_predictions()
            problem_objective_constraint = generate_optimization(scenario, data_predicted)
        elif scenario == "Supplier Risk Assessment":
            data_predicted = generate_supplier_risk_predictions()
            problem_objective_constraint = generate_optimization(scenario, data_predicted)
        elif scenario == "Demand Forecasting":
            data_predicted = generate_demand_forecasting_predictions()
            problem_objective_constraint = generate_optimization(scenario, data_predicted)

    nl_formatted_data = "No Data"  # generate_data_info_in_natural_language(scenario, data_predicted)
    return nl_formatted_data, data_predicted, problem_objective_constraint


# Set up the layout
st.set_page_config(layout="wide")

# Sidebar with Logo and Scenario Dropdown
with st.sidebar:
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        </style>
        """,
        unsafe_allow_html=True
    )

    # Centered Logo
    st.image("systemsltd.png", caption="System LTD.", width=200)  # Replace with your logo
    st.header("Supply Chain Scenario")

    # Scenario Dropdown
    scenario = st.selectbox(
        "Select Scenario:",
        ["", "Customer Order Fulfillment", "Demand-Supply Matching", "Supplier Risk Assessment", "Demand Forecasting"],
        key="scenario"
    )

    # Optimize button under the dropdown
    if scenario:
        if st.button("Optimize"):
            statement_for_scenario = st.session_state.get("problem_statement", "")
            report, code = generate_report_for_scenario(scenario, statement_for_scenario)
            st.session_state["report"] = report  # Store the generated report in session state
            st.session_state["code"] = code
            st.rerun()  # Rerun the script to update the report and code areas with the new data

# Main Content Area
st.markdown("<h2 style='text-align: center;'>Supply Chain Dashboard</h2>", unsafe_allow_html=True)

if not scenario:
    # Display a large GIF and image with instructions when no scenario is selected
    st.image("https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/001/809/881/datas/original.gif",
             use_column_width=True)  # Replace with your GIF URL
    # st.image("supply_chain.png", caption="Supply Chain Overview", use_column_width=True)

    st.markdown("""
    ### How to Use the Application:
    1. **Select a Scenario** from the dropdown in the sidebar.
    2. The application will fetch data and generate predictions.
    3. Review the data and generated problem statement.
    4. Click on **Optimize** to generate a detailed report and code.
    """)
else:
    # Check if the selected scenario has changed
    if "selected_scenario" in st.session_state and st.session_state["selected_scenario"] != scenario:
        # Clear the report section when scenario changes
        st.session_state["report"] = ""
        st.session_state["code"] = ""

    # Check if data for the selected scenario is already in session state
    if "data" not in st.session_state \
            or "problem_statement" not in st.session_state \
            or st.session_state["selected_scenario"] != scenario:
        # Show spinner while fetching predictions
        with st.spinner('Fetching predictions...'):
            st.session_state["predictions"], st.session_state["data"], st.session_state[
                "problem_statement"] = get_dummy_predictions(scenario)
        st.session_state["selected_scenario"] = scenario

    # Display the scenario title
    st.title(f"Scenario: {scenario}")

    # Fetch and display dummy predictions in a text area
    predictions = st.session_state["predictions"]
    data = st.session_state["data"]
    problem_statement = st.session_state["problem_statement"]

    st.subheader("Data")
    st.text_area("Data", data, height=75)

    # Display Problem Statement and Report Text Areas
    st.subheader("Generated Problem Statement")
    problem_statement_area = st.text_area("Problem Statement", problem_statement, height=300)

    code = st.session_state.get("code", "")
    report = st.session_state.get("report", "")

    st.subheader("Code")
    code = st_ace(value=code, language="python", theme="monokai", height=500)
    # Centralize the "Run Code" button below the code editor
    # if st.button("Run Code"):
    #     code_execution = execute_code(code)
    #     explanation = explain_solution(problem_statement, code_execution)
    #     st.markdown(
    #         f"""
    #                 <div style="
    #                     background-color: #f9f9f9;
    #                     padding: 20px;
    #                     border-radius: 10px;
    #                     box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    #                 ">
    #                     <p style="font-size: 16px; color: #34495e;">
    #                         {explanation}</p>
    #                 </div>
    #                 """,
    #         unsafe_allow_html=True
    #     )

    st.subheader("Optimization Report")
    st.markdown(
        f"""
        <div style="
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
            <p style="font-size: 16px; color: #34495e;">
                {report}</p>
        </div>
        """,
        unsafe_allow_html=True
    )




