import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# Create buttons with st.button
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #00FF00;
        color: black;
    }""",
):
    button1_clicked = st.button("Button 1", key="button1")
    if button1_clicked:
        st.write("Button 1 pressed")
with stylable_container(
    "red",
    css_styles="""
    button {
        background-color: #FF0000;

    }""",
):
    button2_clicked = st.button("Button 2", key="button2")

# Check button states and print messages
file_path = 'transactions_data.json'
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
else:
    data = []

# Step 3: Add New Transaction Data
for i, transaction in enumerate(transactions, start=len(data) + 1):
    record = {
        "hour": start_hour,
        "transaction": transaction,
        "market_clearing_price": market_clearing_price
    }
    data.append(record)

# Step 4: Save the Updated Data to a JSON File
with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

st.write("Data saved successfully!")

# Step 5: Load and Display the Entire Accumulated Data
with open(file_path, 'r') as f:
    loaded_data = json.load(f)

st.write("Accumulated Data:")
st.write(loaded_data)