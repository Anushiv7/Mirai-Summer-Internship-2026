import streamlit as st

st.title("Simple Calculator")

# 1. Take two numbers from the user using input boxes
number1 = st.number_input("Enter first number",step=1)
number2 = st.number_input("Enter second number",step=1)
if st.button("Current procedure is number1 'operator' number2, if you want to reverse it..click here."):
    number1,number2=number2,number1

# 2. Provide operation buttons
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Add",use_container_width=True):
            result = number1 + number2
            st.success(f"Result: {result}")

    with col2:
        if st.button("Subtract",use_container_width=True):
            result = number1 - number2
            st.success(f"Result: {result}")

    with col3:
        if st.button("Multiply",use_container_width=True):
            result = number1 * number2
            st.success(f"Result: {result}")

    with col4:
        if st.button("Divide",use_container_width=True):
            if number2 != 0:
                result = number1 / number2
                st.success(f"Result: {result}")
            else:
                st.error("Cannot divide by zero!")
    with col1:
        if st.button("Power(Exponent)",use_container_width=True):
            result=number1**number2
            st.success(f"Result: {result}")
    with col2:
        if st.button("Modulo(Remainder)",use_container_width=True):
            if number2 != 0:
                result=number1%number2
                st.success(f"Result: {result}")
            else:
                st.error("Cannot modulo by zero.")