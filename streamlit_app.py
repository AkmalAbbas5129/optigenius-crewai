import streamlit as st
from streamlit_ace import st_ace
import pandas as pd
from utils import generate_optimization, explain_solution, solve_optimization_problem, generate_pulp_code_for_problem
from supply_chain_scenarios.custom_order_fullfilment import generate_customer_order_fulfillment_predictions
from supply_chain_scenarios.demand_supply_matching import generate_demand_supply_matching_predictions
from supply_chain_scenarios.supplier_risk_management import generate_supplier_risk_predictions
from supply_chain_scenarios.demand_forecasting import generate_demand_forecasting_predictions
from supply_chain_scenarios.inventory_optimization import generate_inventory_optimization_predictions
from supply_chain_scenarios.transportation_optimization import generate_transportation_optimization_predictions
from langgraph_crew import execute_code

# Load CSV into a pandas DataFrame
def load_scenario_data():
    return pd.read_csv('scenario_data.csv')

def get_scenario_details(scenario):
    df = load_scenario_data()
    scenario_row = df[df['Scenario'] == scenario]
    if not scenario_row.empty:
        problem_statement = scenario_row['Problem Statement'].values[0]
        objective = scenario_row['Objective'].values[0]
        constraint = scenario_row['Constraint'].values[0]
    else:
        problem_statement = objective = constraint = ""
    return problem_statement, objective, constraint

def get_dummy_predictions(scenario):
    problem = objective = constraint = ""
    data_in_format = {}

    with st.spinner('Predictions are being fetched...'):
        if scenario == "Customer Order Fulfillment":
            problem, objective, constraint, data_in_format = generate_customer_order_fulfillment_predictions()
        elif scenario == "Demand-Supply Matching":
            problem, objective, constraint, data_in_format = generate_demand_supply_matching_predictions()
        elif scenario == "Supplier Risk Assessment":
            problem, objective, constraint, data_in_format = generate_supplier_risk_predictions()
        elif scenario == "Demand Forecasting":
            problem, objective, constraint, data_in_format = generate_demand_forecasting_predictions()
        elif scenario == "Inventory Optimization":
            problem, objective, constraint, data_in_format = generate_inventory_optimization_predictions()
        elif scenario == "Transportation Optimization":
            problem, objective, constraint, data_in_format = generate_transportation_optimization_predictions()

    return problem, objective, constraint, data_in_format

# Main function for handling custom scenario
def handle_custom_scenario():
    st.subheader("Upload CSV files for Custom Scenario")

    scenario_name = st.text_input("Enter Custom Scenario Name")
    uploaded_files = st.file_uploader("Upload CSV files", accept_multiple_files=True, type=["csv"])

    if scenario_name and uploaded_files:
        custom_dataframes = {}
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file)
            custom_dataframes[uploaded_file.name] = df
        return scenario_name, custom_dataframes

    return None, pd.DataFrame([])

# Set up the layout
st.set_page_config(layout="wide")

# Sidebar with Logo and Scenario Dropdown
with st.sidebar:
    st.image("system_nobg.png", caption="System LTD.", width=300)
    st.header("Supply Chain Scenario")

    # Scenario Dropdown with Custom Scenario Option
    scenario = st.selectbox(
        "Select Scenario:",
        ["Select Optimization Scenario", "Customer Order Fulfillment", "Demand-Supply Matching", "Supplier Risk Assessment", "Inventory Optimization", "Transportation Optimization", "Custom Scenario"],
        key="scenario"
    )
    # "Demand Forecasting"

# Main Content Area
st.markdown(
    "<h2 style='text-align: center;'>Opti<span style='color: orange;'>Genius</span></h2>",
    unsafe_allow_html=True
)

if not scenario:
    st.markdown(
        """
        <div style='display: flex; justify-content: center;'>
            <img src='https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/001/809/881/datas/original.gif' 
                 style='width: 50%; max-width: 600px;' />
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ### How to Use the Application:
    1. **Select a Scenario** from the dropdown in the sidebar.
    2. The application will fetch data and generate predictions.
    3. Review the data and generated problem statement.
    4. Click on **Optimize** to generate a detailed report and code.
    """)
else:
    if "selected_scenario" in st.session_state and st.session_state["selected_scenario"] != scenario:
        st.session_state["report"] = ""
        st.session_state["code"] = ""

    if scenario != "Custom Scenario":
        if "data" not in st.session_state or st.session_state["selected_scenario"] != scenario:
            with st.spinner('Fetching predictions...'):
                st.session_state["problem_statement"], st.session_state["objective"], \
                    st.session_state["constraints"], st.session_state["data_in_format"] = get_dummy_predictions(scenario)
            st.session_state["selected_scenario"] = scenario

        st.title(f"Scenario: {scenario}")

    else:
        if "data_in_format" not in st.session_state:
            st.warning("Please upload CSVs and name the scenario to proceed.")

    problem_statement = st.session_state.get("problem_statement", "")
    objective = st.session_state.get("objective", "")
    constraints = st.session_state.get("constraints", "")
    data_in_format = st.session_state.get("data_in_format", "")

    with st.expander("Click here to view the predicted data"):
        if data_in_format:
            for name, df in data_in_format.items():
                st.subheader(f"{name}")
                st.dataframe(df)

    st.subheader("Optimization Problem")
    problem_statement_area = st.text_area("Problem Statement", problem_statement, height=200)
    objective_area = st.text_area("Objective", objective, height=200)
    constraint_area = st.text_area("Constraint", constraints, height=200)

    # Optimize button under the dropdown
    if scenario:
        if scenario == "Custom Scenario":
            custom_scenario_name, custom_data_in_format = handle_custom_scenario()

            if custom_scenario_name and custom_data_in_format and st.button("Optimize Custom Scenario"):
                # Store the custom scenario data in session state
                # st.session_state["scenario"] = custom_scenario_name
                st.session_state["data_in_format"] = custom_data_in_format

                problem_statement = st.session_state.get("problem_statement", "")
                objectives = st.session_state.get("objective", "")
                constraint = st.session_state.get("constraints", "")
                data_predicted = st.session_state.get("data_in_format", "")

                report = solve_optimization_problem(problem_statement, objectives, constraint, data_predicted)
                code = generate_pulp_code_for_problem(scenario, problem_statement, objectives, constraint,
                                                      data_predicted)

                st.session_state["report"] = report
                st.session_state["code"] = code
                st.rerun()

        else:
            if st.button("Optimize"):
                problem_statement = st.session_state.get("problem_statement", "")
                objectives = st.session_state.get("objective", "")
                constraint = st.session_state.get("constraints", "")
                data_predicted = st.session_state.get("data_in_format", "")

                report = solve_optimization_problem(problem_statement, objectives, constraint, data_predicted)
                code = generate_pulp_code_for_problem(scenario, problem_statement, objectives, constraint,
                                                      data_predicted)

                st.session_state["report"] = report
                st.session_state["code"] = code
                st.rerun()

    with st.expander("Code"):
        code = st.session_state.get("code", "")
        code = st_ace(value=code, language="python", theme="monokai", height=500)

        if st.button("Run Code"):
            code_execution = execute_code(code)
            explanation = explain_solution(problem_statement, code_execution)
            st.markdown(
                f"""
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                        <p style="font-size: 16px; color: #34495e;">{explanation}</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

    with st.expander("Optimization Report"):
        report = st.session_state.get("report", "")
        st.html(report)
