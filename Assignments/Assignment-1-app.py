#ASSIGNMENT1-APP
import streamlit as st 
#Task 1: The UI Shell
st.title("Free Survey.")
st.write("Fill the respective fields below and then submit this free survey.")
#Task 2: Multi-Data Collection
user_name=st.text_input("Enter your Name.")
user_mssg=st.text_input("Enter your message for us.")
#Task 3: The Action Gate
if st.button("Submit Survey"):
    #Task 4: Conditional Routing (Edge Cases)
    if user_name.strip()=="":
        st.error("Name field can't be empty, please try again.")
    elif user_mssg.strip()=="":
        st.warning("Your message field is empty, please try again. NOTE:if you don't have any message for us, enter -- ")

    if user_name.strip() != "" and user_mssg.strip() != "":
        #Task 5: The Formatted Output
        st.success(f"Greetings, {user_name} with message: {user_mssg}.  \nSubmission Successful.We'll get back to you shortly.")
        length=len(user_mssg)
        #Advanced Challenge: Token Cost Estimator
        #token length=length/4
        st.info(f"System Check: Your message will consume approximately {length/4} tokens from our context window.")
