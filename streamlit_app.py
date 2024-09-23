import streamlit as st
import pandas as pd
from streamlit_ace import st_ace
from utils import generate_optimization, explain_solution, solve_optimization_problem, generate_pulp_code_for_problem
from supply_chain_scenarios.custom_order_fullfilment import generate_customer_order_fulfillment_predictions
from supply_chain_scenarios.demand_supply_matching import generate_demand_supply_matching_predictions
from supply_chain_scenarios.supplier_risk_management import generate_supplier_risk_predictions
from supply_chain_scenarios.demand_forecasting import generate_demand_forecasting_predictions
from supply_chain_scenarios.inventory_optimization import generate_inventory_optimization_predictions
from supply_chain_scenarios.transportation_optimization import generate_transportation_optimization_predictions
from langgraph_crew import execute_code


def get_dummy_predictions(scenario):
    # Check if predictions are already in session state
    if "predicted_data" not in st.session_state or st.session_state["selected_scenario"] != scenario:
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

        # Store the predictions in session state to avoid refetching on button press
        st.session_state["predicted_data"] = {
            "problem": problem,
            "objective": objective,
            "constraint": constraint,
            "data_in_format": data_in_format
        }
        st.session_state["selected_scenario"] = scenario

    return st.session_state["predicted_data"]["problem"], st.session_state["predicted_data"]["objective"], \
           st.session_state["predicted_data"]["constraint"], st.session_state["predicted_data"]["data_in_format"]


# Set up the layout
st.set_page_config(layout="wide")

# Sidebar with Scenario Dropdown
with st.sidebar:
    st.image("system_nobg.png", caption="", width=300)
    st.header("Supply Chain Scenario")

    scenario = st.selectbox(
        "Select Scenario:",
        ["Select Optimization Scenario", "Customer Order Fulfillment", "Demand-Supply Matching",
         "Supplier Risk Assessment", "Inventory Optimization", "Transportation Optimization", "Custom Scenario"],
        key="scenario"
    )

st.markdown(
    "<h2 style='text-align: center;'>Opti<span style='color: orange;'>Genius</span></h2>",
    unsafe_allow_html=True
)

if scenario == "Select Optimization Scenario":
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
    if scenario != "Custom Scenario":
        if "data_in_format" not in st.session_state or st.session_state["selected_scenario"] != scenario:
            problem_statement, objective, constraints, data_in_format = get_dummy_predictions(scenario)
            st.session_state["problem_statement"] = problem_statement
            st.session_state["objective"] = objective
            st.session_state["constraints"] = constraints
            st.session_state["data_in_format"] = data_in_format

        st.title(f"Scenario: {scenario}")

    else:
        st.warning("Please upload CSVs and name the scenario to proceed.")

    # Retrieve from session state
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

    # Add spinner on optimization
    if st.button("Optimize"):
        with st.spinner("Calculating... Please wait..."):
            report = solve_optimization_problem(problem_statement, objective, constraints, data_in_format)
            code = generate_pulp_code_for_problem(scenario, problem_statement, objective, constraints, data_in_format)

            st.session_state["report"] = report
            st.session_state["code"] = code
            st.rerun()

    with st.expander("Click Here To View Code"):
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

    with st.expander("Click Here To View Optimization Report"):
        report = st.session_state.get("report", "")
        st.html(report)
