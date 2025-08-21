import streamlit as st
import pandas as pd
from datetime import date
from backend import (
    create_employee,
    read_employees,
    update_employee,
    delete_employee,
    get_employee_departments,
    get_total_employees,
    get_total_salary_sum,
    get_average_salary,
    get_min_salary,
    get_max_salary,
    get_department_salary_summary
)

st.set_page_config(layout="wide", page_title="HR Employee Directory & Analytics")

st.title("👨‍💼 HR Employee Directory & Analytics")

# --- BUSINESS INSIGHTS & METRICS ---
st.header("Business Insights & Metrics")

total_employees = get_total_employees()
total_salary_sum = get_total_salary_sum()
avg_salary = get_average_salary()
min_salary = get_min_salary()
max_salary = get_max_salary()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Employees", f"{total_employees if total_employees is not None else 0}")
with col2:
    st.metric("Total Monthly Salary Expense", f"${total_salary_sum if total_salary_sum is not None else 0:,.2f}")
with col3:
    st.metric("Average Salary", f"${avg_salary if avg_salary is not None else 0:,.2f}")
with col4:
    st.metric("Lowest Paid Employee", f"${min_salary if min_salary is not None else 0:,.2f}")
with col5:
    st.metric("Highest Paid Employee", f"${max_salary if max_salary is not None else 0:,.2f}")

st.markdown("---")

# --- VISUAL ANALYTICS ---
st.header("📊 Visual Analytics")

department_salary_data = get_department_salary_summary()
if department_salary_data:
    df_analytics = pd.DataFrame(department_salary_data, columns=["department", "avg_salary", "min_salary", "max_salary"])
    
    st.subheader("Average Salary by Department")
    st.bar_chart(df_analytics.set_index("department")['avg_salary'])
    
    st.subheader("Department Salary Range")
    st.dataframe(df_analytics, use_container_width=True)
else:
    st.info("No data available for visual analytics.")

st.markdown("---")

# --- CRUD FUNCTIONALITY: CREATE & UPDATE ---
with st.expander("➕ Add/Update Employee"):
    st.subheader("Add a New Employee")
    with st.form("employee_form", clear_on_submit=True):
        col_id, col_name = st.columns(2)
        with col_id:
            employee_id = st.text_input("Employee ID", help="Required for new entries.")
        with col_name:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")

        col_dept, col_hire = st.columns(2)
        with col_dept:
            department = st.text_input("Department")
        with col_hire:
            hire_date = st.date_input("Hire Date", date.today())
        
        salary = st.number_input("Salary", min_value=0.0, format="%f")
        
        submit_button = st.form_submit_button("Add New Employee")
        if submit_button:
            if employee_id and first_name and last_name and department and hire_date and salary is not None:
                if create_employee(employee_id, first_name, last_name, department, hire_date, salary):
                    st.success("Employee added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add employee. Make sure the Employee ID is unique.")
            else:
                st.warning("Please fill in all fields.")

    st.markdown("---")
    st.subheader("Update an Existing Employee")
    
    employees_data_all = read_employees()
    if employees_data_all:
        employees_df_all = pd.DataFrame(employees_data_all, columns=["employee_id", "first_name", "last_name", "department", "hire_date", "salary"])
        employee_to_update = st.selectbox("Select Employee to Update", options=employees_df_all['employee_id'].unique(), key="update_select")
        
        if employee_to_update:
            current_data = employees_df_all[employees_df_all['employee_id'] == employee_to_update].iloc[0]
            
            with st.form("update_employee_form", clear_on_submit=False):
                col_update_name, col_update_dept = st.columns(2)
                with col_update_name:
                    updated_first_name = st.text_input("First Name", value=current_data['first_name'])
                    updated_last_name = st.text_input("Last Name", value=current_data['last_name'])
                with col_update_dept:
                    updated_department = st.text_input("Department", value=current_data['department'])
                    updated_hire_date = st.date_input("Hire Date", value=current_data['hire_date'])
                
                updated_salary = st.number_input("Salary", value=float(current_data['salary']), min_value=0.0, format="%f")
                
                update_button = st.form_submit_button("Update Employee")
                if update_button:
                    if update_employee(employee_to_update, updated_first_name, updated_last_name, updated_department, updated_hire_date, updated_salary):
                        st.success(f"Employee {employee_to_update} updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update employee.")
    
# --- READ, FILTER, SORT & DELETE ---
st.header("🔍 Employee Directory")

col_filter, col_sort = st.columns(2)
with col_filter:
    all_departments = get_employee_departments()
    selected_department = st.selectbox("Filter by Department", options=["All"] + all_departments)

with col_sort:
    sort_option = st.selectbox("Sort by", options=["None", "salary", "hire_date"])

# Fetch data based on filters
employees_data_filtered = read_employees(department_filter=selected_department, sort_by=sort_option)

if employees_data_filtered:
    df_filtered = pd.DataFrame(employees_data_filtered, columns=["employee_id", "first_name", "last_name", "department", "hire_date", "salary"])
    st.dataframe(df_filtered, use_container_width=True)
    
    # DELETE functionality
    st.subheader("Delete Employee")
    employee_to_delete = st.selectbox("Select an employee ID to delete", options=df_filtered['employee_id'].unique(), key="delete_select_filtered")
    if st.button("Delete Selected Employee"):
        if delete_employee(employee_to_delete):
            st.success(f"Employee {employee_to_delete} deleted successfully.")
            st.rerun()
        else:
            st.error("Failed to delete employee.")

else:
    st.info("No employees found.") 