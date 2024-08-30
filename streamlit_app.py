import streamlit as st
import time
from utils import generate_data_info_in_natural_language, generate_optimization
from supply_chain_scenarios.custom_order_fullfilment import generate_customer_order_fulfillment_predictions
from supply_chain_scenarios.demand_supply_matching import generate_demand_supply_matching_predictions
from supply_chain_scenarios.supplier_risk_management import generate_supplier_risk_predictions
from supply_chain_scenarios.demand_forecasting import generate_demand_forecasting_predictions
from langgraph_crew import generate_report_for_scenario


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


# Function to generate a problem statement
def generate_problem_statement():
    return "This is the generated problem statement based on the selected scenario."


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
    st.markdown('<div class="center"><img src="systemsltd.png" width="150" /></div>', unsafe_allow_html=True)
    st.header("Supply Chain Scenario")

    # Scenario Dropdown
    scenario = st.selectbox(
        "Select Scenario:",
        ["", "Customer Order Fulfillment", "Demand-Supply Matching", "Supplier Risk Assessment", "Demand Forecasting"],
        key="scenario"
    )

# Main Content Area
if scenario:
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
    # st.subheader("ML Model Predictions in Natural Language Format")
    # st.text_area("Predictions", predictions, height=200)

    # Display Problem Statement and Report Text Areas
    st.subheader("Generated Problem Statement")
    problem_statement_area = st.text_area("Problem Statement", problem_statement, height=300)

    st.subheader("Code")
    report = st.session_state.get("report", "")
    code = st.session_state.get("code", "")
    # report_area = st.text_area("Report", report, height=300)
    st.code(code, language='python')
    st.subheader("Optimization Report")
    st.markdown(
        """
        <div style="
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
            <p style="font-size: 16px; color: #34495e;">
                {}</p>
        </div>
        """.format(str(report)),
        unsafe_allow_html=True
    )

    # Button to trigger optimization (generating the report)
    if st.button("Optimize"):
        statement_for_scenario = problem_statement_area
        report, code = generate_report_for_scenario(scenario, statement_for_scenario)
        st.session_state["report"] = report  # Store the generated report in session state
        st.session_state["code"] = code
        st.rerun()  # Rerun the script to update the report text area with the new report
