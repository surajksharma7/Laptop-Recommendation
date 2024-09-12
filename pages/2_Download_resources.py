import streamlit as st

# Set page configuration
st.set_page_config("Download Resources", "🔻", "centered", "expanded")

# Header
st.header("🔻 Download Resources of this Project", divider="red")

# Define a function to create a download link
def create_download_link(filename, text):
    with open(filename, "rb") as file:
        content = file.read()
    st.download_button(
        label=text,
        data=content,
        file_name=filename,
        mime="application/octet-stream"
    )

# List of files to download with their corresponding button text
files_to_download1 = [
    ("data/Dataset.csv", "Laptop Dataset"),
    ("data\LaptopRecommendation.ipynb", "jupyter file"),
    # Add empty placeholders to make the length of both lists equal
    ("", ""),
]

files_to_download2 = [
    ("data/upload_Page.py", "Upload page"),
    ("data/Prediction_page.py", "Prediction Page"),
]

# Split the layout into two columns
col1, col2 = st.columns(2)

# Display download buttons for Dataset 1, 2, and 3 in the first column
with col1:
    for file, text in files_to_download1:
        if file:  # Check if the file path is not empty
            create_download_link(file, text)

# Display download buttons for Dataset 4 and 5 in the second column
with col2:
    for file, text in files_to_download2:
        create_download_link(file, text)
