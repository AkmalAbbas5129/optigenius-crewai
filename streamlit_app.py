import streamlit as st
from streamlit_ace import st_ace
import time
from utils import generate_data_info_in_natural_language, generate_optimization, explain_solution,solve_optimization_problem,generate_pulp_code_for_problem
from supply_chain_scenarios.custom_order_fullfilment import generate_customer_order_fulfillment_predictions
from supply_chain_scenarios.demand_supply_matching import generate_demand_supply_matching_predictions
from supply_chain_scenarios.supplier_risk_management import generate_supplier_risk_predictions
from supply_chain_scenarios.demand_forecasting import generate_demand_forecasting_predictions
from supply_chain_scenarios.inventory_optimization import generate_inventory_optimization_predictions
from supply_chain_scenarios.transportation_optimization import generate_transportation_optimization_predictions
from langgraph_crew import generate_report_for_scenario, execute_code
import pandas as pd


# Load CSV into a pandas DataFrame
def load_scenario_data():
    # Replace with the path to your CSV file
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


# Function to simulate fetching predictions from an ML model
def get_dummy_predictions(scenario):
    data_in_format = ""
    data_predicted = ""
    problem = objective = constraint = ""

    with st.spinner('Predictions are being fetched...'):
        if scenario == "Customer Order Fulfillment":
            # data_predicted = generate_customer_order_fulfillment_predictions()
            # data_in_format = generate_optimization(scenario, data_predicted)
            # problem, objective, constraint = get_scenario_details(scenario)
            problem, objective, constraint,data_in_format = generate_customer_order_fulfillment_predictions()
        elif scenario == "Demand-Supply Matching":
            # data_predicted = generate_demand_supply_matching_predictions()
            # data_in_format = generate_optimization(scenario, data_predicted)
            # problem, objective, constraint = get_scenario_details(scenario)
            problem, objective, constraint, data_in_format = generate_demand_supply_matching_predictions()
        elif scenario == "Supplier Risk Assessment":
            # data_predicted = generate_supplier_risk_predictions()
            # data_in_format = generate_optimization(scenario, data_predicted)
            # problem, objective, constraint = get_scenario_details(scenario)
            problem, objective, constraint, data_in_format = generate_supplier_risk_predictions()
        elif scenario == "Demand Forecasting":
            # data_predicted = generate_demand_forecasting_predictions()
            # data_in_format = generate_optimization(scenario, data_predicted)
            # problem, objective, constraint = get_scenario_details(scenario)
            problem, objective, constraint, data_in_format = generate_demand_forecasting_predictions()
        elif scenario == "Inventory Optimization":
            problem, objective, constraint, data_in_format = generate_inventory_optimization_predictions()
        elif scenario == "Transportation Optimization":
            problem, objective, constraint, data_in_format = generate_transportation_optimization_predictions()

    nl_formatted_data = "No Data"  # generate_data_info_in_natural_language(scenario, data_predicted)
    return nl_formatted_data, data_predicted, problem, objective, constraint, data_in_format


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
        ["", "Customer Order Fulfillment", "Demand-Supply Matching", "Supplier Risk Assessment", "Inventory Optimization","Transportation Optimization"],
        key="scenario"
    ) 
    # "Demand Forecasting",

    # Optimize button under the dropdown
    if scenario:
        if st.button("Optimize"):
            # problem_statement = "Problem Statement:\n"+st.session_state.get("problem_statement", "")
            # objectives = "\nObjective:\n" + st.session_state.get("objective", "")
            # constraint = "\nConstraints:\n" + st.session_state.get("constraints", "")
            # # data_predicted = "\nData:\n"+ str(st.session_state.get("data", ""))
            # data_predicted = "\nData:\n" + str(st.session_state.get("data_in_format", ""))
            #
            # statement_for_scenario = problem_statement + objectives + constraint + data_predicted
            # print(statement_for_scenario)

            problem_statement = st.session_state.get("problem_statement", "")
            objectives = st.session_state.get("objective", "")
            constraint = st.session_state.get("constraints", "")
            # data_predicted = "\nData:\n"+ str(st.session_state.get("data", ""))
            data_predicted = st.session_state.get("data_in_format", "")

            # report, code = generate_report_for_scenario(scenario, statement_for_scenario) # This is for Graph Workflow

            report = solve_optimization_problem(problem_statement,objectives,constraint,data_predicted)
            code = generate_pulp_code_for_problem(scenario,problem_statement,objectives,constraint,data_predicted)

            st.session_state["report"] = report  # Store the generated report in session state
            st.session_state["code"] = code
            st.rerun()  # Rerun the script to update the report and code areas with the new data

# Main Content Area
# st.markdown("<h2 style='text-align: center;'>Supply Chain Dashboard</h2>", unsafe_allow_html=True
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
    # Display a large GIF and image with instructions when no scenario is selected
    # st.image("https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/001/809/881/datas/original.gif",
    #          use_column_width=True)  # Replace with your GIF URL
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
            st.session_state["predictions"], st.session_state["data"], \
                st.session_state["problem_statement"], st.session_state["objective"], st.session_state["constraints"], \
            st.session_state["data_in_format"] = get_dummy_predictions(scenario)
        st.session_state["selected_scenario"] = scenario

    # Display the scenario title
    st.title(f"Scenario: {scenario}")

    # Fetch and display dummy predictions in a text area
    predictions = st.session_state["predictions"]
    data = st.session_state["data"]
    problem_statement = st.session_state["problem_statement"]
    objective = st.session_state["objective"]
    constraints = st.session_state["constraints"]
    data_in_format = st.session_state["data_in_format"]
    # print(data_in_format)

    # st.subheader("Data")
    # st.text_area("Data", data, height=75)

    with st.expander("Click here to view the predicted data"):
        # st.dataframe(data_in_format)
        # Display each DataFrame in the dictionary
        for name, df in data_in_format.items():
            st.subheader(f"{name}")
            st.dataframe(df)
        # st.subheader("Formatted Data")
        # st.text_area("Formatted Data", data_in_format, height=200)
        # st.markdown(
        #     f"""
        #                     <div style="
        #                         background-color: #f9f9f9;
        #                         padding: 20px;
        #                         border-radius: 10px;
        #                         box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        #                     ">
        #                         <p style="font-size: 16px; color: #34495e;">
        #                             {data_in_format}</p>
        #                     </div>
        #                     """,
        #     unsafe_allow_html=True
        # )

    # Display Problem Statement and Report Text Areas
    st.subheader("Optimization Problem")
    problem_statement_area = st.text_area("Problem Statement", problem_statement, height=200)
    objective_area = st.text_area("Objective", objective, height=200)
    constraint_area = st.text_area("Constraint", constraints, height=200)

    # Collapsible section for code
    with st.expander("Code"):
        code = st.session_state.get("code", "")
        code = st_ace(value=code, language="python", theme="monokai", height=500)

        # Run Code button
        if st.button("Run Code"):
            code_execution = execute_code(code)
            explanation = explain_solution(st.session_state["problem_statement"], code_execution)
            st.markdown(
                f"""
                    <div style="
                        background-color: #f9f9f9;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    ">
                        <p style="font-size: 16px; color: #34495e;">
                            {explanation}</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

    # Collapsible section for the report
    with st.expander("Optimization Report"):
        report = st.session_state.get("report", "")
        st.html(report)
        # st.markdown(
        #     f"""
        #         <div style="
        #             background-color: #f9f9f9;
        #             padding: 20px;
        #             border-radius: 10px;
        #             box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        #         ">
        #             <p style="font-size: 16px; color: #34495e;">
        #                 {report}</p>
        #         </div>
        #         """,
        #     unsafe_allow_html=True
        # )
