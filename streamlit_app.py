# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Add page",
    page_icon="⭐"
)


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource()
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["patients_gsheets_url"]

rows = run_query(f'SELECT Subject_id FROM "{sheet_url}"')
subject_ids = [int(row[0]) for row in rows]

st.write(f"{subject_ids}")


# Specify the sheet you want to query ('Patients' in this case)




st.title("Add New Patient")

st.subheader("Personal Details")
st.write("This section is to input the patient's personal details.")
st.write("\n")



#### PLACEHOLDER ####
data = {'subject_id': subject_ids}
df = pd.DataFrame(data)

# Subject ID input
# Determine the latest subject_id if the DataFrame is not empty
if not df.empty:
    latest_id = df['subject_id'].max()
else:
    # If the DataFrame is empty, start from a default value (e.g., 1000)
    latest_id = 1001

# Create a new subject_id as +1 of the latest ID
subject_id = latest_id + 1
st.write("Subject_id:", subject_id)


# Input Full Name
full_name= st.text_input("Full Name:")

# Input gender
gender = st.radio("Gender:", ["M", "F"])

# date of birth
dob = st.date_input("Date of Birth:")

# date of death
death_applicable = st.checkbox("Is Date of Death Applicable?")

if death_applicable:
    dod = st.date_input("Date of Death:")

#Insurance
insurance = st.radio("Insurance:", ["Medicare", "Private"])

# Marital Status
marital_status = st.selectbox("Marital Status:", ["Single", "Married", "Divorced", "Widowed"])

# Ethnicity
ethnicity = st.text_input("Ethnicity:")

st.markdown("---")

st.subheader("Admission History")
st.write("This section is to input the patient's admission history and details of the admission.")
st.write("\n")

@st.cache_resource()
def get_existing_admissions():
    return []

diagnosis_d=[["123","lol"], ["321","lmao"]]

# Get existing admissions
existing_admissions = get_existing_admissions()

# Create a form to group input fields

# Collect admission details
admission_id = 1
admission_time = st.date_input("Admission Date:")
discharge_time = st.date_input("Discharge Date:")
admission_type = st.radio("Admission Type", ["Emergency", "Elective"])
admission_location = st.selectbox("Admission Location:", ["CLINIC REFERRAL/PREMATURE", "EMERGENCY ROOM ADMIT", "PHYS REFERRAL/NORMAL DELI", "TRANSFER FROM HOSP/ESTRAM", "TRANSFER FROM SKILLED NUR"])
discharge_location = st.selectbox("Discharge Location:", ["DEAD/EXPIRED", "DISCH-TRAN TO PSYCH HOSP", "HOME", "HOME HEALTH CARE", "HOME WITH HOME IV PROVIDR", "HOSPICE-HOME", "ICF", "LONG TERM CARE HOSPITAL", "REHAB/DISTINCT PART HOSP", "SNF"])
selected_diagnosis = st.selectbox("Select a Diagnosis:", [f"{icd_code} {long_desc}" for icd_code, long_desc in diagnosis_d])
icd_code, long_desc = selected_diagnosis.split(" ")
add_admission_button = st.button("Add Admission")

# Save admission details to the DataFrame when "Add Admission" button is clicked
if add_admission_button:
    
    new_admission = {"Admission ID": admission_id,
                     "Admission Time": admission_time,
                     "Discharge Time": discharge_time,
                     "Admission Type": admission_type,
                     "Admission Location": admission_location,
                     "Discharge Location": discharge_location,
                     "Diagnosis Code": icd_code,
                     "Diagnosis Description": long_desc}
    existing_admissions.append(new_admission)
    st.success("Admission details added successfully!")

# Display the list of admissions
if existing_admissions:
    
    df = pd.DataFrame(existing_admissions)
    st.dataframe(df)


@st.cache_resource()
def get_existing_lab_events():
    return []

# Get existing lab events
existing_lab_events = get_existing_lab_events()


# Define a dictionary mapping categories to their corresponding fluids
category_to_fluid = {
    "Blood Gas": ["Blood", "Other Bodily Fluid"],
    "Chemistry": ["Ascites", "Blood", "Cerebrospinal Fluid (CSF)", "Joint Fluid","Other Body Fluid","Pleural","Stool","Urine"],
    "Hematology": ["Ascites", "Blood", "Cerebrospinal Fluid (CSF)", "Joint Fluid","Other Body Fluid","Pleural","Stool","Urine"],
}

st.markdown("---")

st.subheader("Lab History")
st.write("This section is to input the patient's lab testing history.")
st.write("\n")

@st.cache_resource()
def get_category():
    return category

# Create a form to collect Lab Events data
category = st.selectbox("Category:", list(category_to_fluid.keys()))
lab_events_id=1
fluid = st.selectbox("Fluid:", category_to_fluid[category])
label=st.text_input("Label:")
flag = st.selectbox("Flag:", ["normal", "abnormal", "delta"])
add_lab_event_button = st.button("Add Lab Event")

# Save lab event details to the DataFrame when "Add Lab Event" button is clicked
if add_lab_event_button:
    new_lab_event = {
        "Lab Events ID": lab_events_id,
        "Category": category,
        "Fluid": fluid,
        "Label": label,
        "Flag": flag,
    }
    existing_lab_events.append(new_lab_event)
    st.success("Lab Event details added successfully!")

# Display the list of lab events
if existing_lab_events:
    df = pd.DataFrame(existing_lab_events)
    st.dataframe(df)


st.write("\n\n\n\n\n\n\n\n\n\n\n")
st.write("\n\n\n\n\n\n\n\n\n\n\n")
st.write("\n\n\n\n\n\n\n\n\n\n\n")
st.write("\n\n\n\n\n\n\n\n\n\n\n")
st.write("\n\n\n\n\n\n\n\n\n\n\n")

final_submit_button = st.button("Add Patient")
   

# Display the list of lab events
if final_submit_button:
    st.success("Patients details added successfully!")
    st.session_state.full_name = ""
    st.session_state.death_applicable = False
    st.session_state.ethnicity=""
    st.session_state.label=""
    existing_lab_events=[]
    existing_admissions=[]
