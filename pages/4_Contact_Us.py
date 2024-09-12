import streamlit as st

def main():
    st.title("Contact Us")

    # Collect user input
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Message", height=200)

    # Validate and process form submission
    if st.button("Submit"):
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        else:
            # Process the submitted form (e.g., send email, save to database)
            st.success("Message submitted successfully!")

if __name__ == "__main__":
    main()
