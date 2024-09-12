import streamlit as st
import os

def main():
    st.header("🔻 Upload Page")
    
    # Display a file uploader widget
    uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt"])

    # Check if a file has been uploaded
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        # Create a directory named "upload" if it does not exist
        upload_dir = "upload"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Save the uploaded file to the "upload" directory
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

if __name__ == "__main__":
    main()
