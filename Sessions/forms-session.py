import streamlit as st
import pandas as pd
import time

st.subheader("1) API LATENCY")

if st.button("Click to check the API latency"):
    with st.spinner("Checking the API latency..."):
        time.sleep(2)
        st.success("API latency checked successfully!")
    st.toast("API latency checked successfully!")
    st.write("Final answer")




st.subheader("2) Using Forms Session Example")
with st.expander("Click to see the expander content"):
    st.write("hi lol")

with st.form(key="form1"):
    st.write("This is a form session example.")
    input_1=st.slider("Enter the Temp",0,100,15)
    input_2=st.selectbox("Select an option",["Option 1","Option 2","Option 3"])

    submitted=st.form_submit_button("Submit the form.")


if submitted:
    st.success("Form submitted successfully!")

data=pd.DataFrame(
    {
        "Task":["Reading","Writing","Coding"],
        "Status":["Completed","In Progress","Not Started"],
        "Hours Spent":[5,3,10]
    }
)

edited_df=st.data_editor(data, num_rows="dynamic")

if st.button("Save the changes in dataframe"):
    st.write("Changes saved successfully!")
    st.dataframe(edited_df)
