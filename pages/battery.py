import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Read data from Excel file
user_file_path = r'C:\Users\DELL\energy Analysis\Battery.xlsx'

user_data = pd.read_excel(user_file_path, header=0)
user_data.dropna(subset=['Hour'], inplace=True)
user_data['Hour']=user_data['Hour'].astype(int)
user_data['Excess energy'] = pd.to_numeric(user_data['Excess energy'], errors='coerce').fillna(0)
user_data['deficited energy'] = pd.to_numeric(user_data['deficited energy'], errors='coerce').fillna(0)
user_data['demand-supply'] = pd.to_numeric(user_data['demand-supply'], errors='coerce').fillna(0)
file_path = r'C:\Users\DELL\energy Analysis\operator.xlsx'  
offerdata = pd.read_excel(file_path, header=0)
# Streamlit app layout
st.title('Battery Levels Over 24 Hours')

# Interactive components
selected_hour = st.slider('Select hour', 0, 23, 0)
#if user_data.at[selected_hour,'demand-supply']<30:
    #st.error("you can't order at this hour,battery not avialable!")
st.write('Battery as provider')
energy_taken = st.number_input('Amount[MW]', min_value=0.0, value=0.0, step=0.1)
if user_data.at[selected_hour,'deficited energy'] <=energy_taken :
    st.error(f'maximum energy is :{user_data.at[selected_hour, "deficited energy"]}')
elif  user_data.at[selected_hour,'deficited energy']<=33:
       st.error("you can't order at this hour,battery not avialable!") 
price_taken = st.number_input('price[$/MWH]', min_value=0.0, value=0.0, step=0.1)
if st.button('Take Energy'):
     offerdata.loc[selected_hour, 'battery provider Energy'] = energy_taken
     offerdata.loc[selected_hour, 'battery provider price'] = price_taken
     offerdata.to_excel(file_path, index=False)
    #user_data.at[selected_hour, 'Excess energy'] = max(user_data.at[selected_hour, 'Excess energy'] - energy_taken, 0)
    #st.success(f'Energy taken at hour {selected_hour}. Updated battery level: {user_data.at[selected_hour, "Excess energy"]}')
st.write('Battery as user')
energy_taken_user = st.number_input('Amount[MW]', min_value=0.0, value=0.0, step=0.1,key="providerenergy")
if user_data.at[selected_hour,'Excess energy'] <=energy_taken_user:
    st.error(f'maximum energy is :{user_data.at[selected_hour, "Excess energy"]}')
elif  user_data.at[selected_hour,'Excess energy']<=33:
    st.error("you can't order at this hour,battery not avialable!")
price_taken_user = st.number_input('price[$/MWH]', min_value=0.0, value=0.0, step=0.1,key="providerprice")
if st.button('Take Energy',key="provider"):
    offerdata.loc[selected_hour, 'battery user Energy'] = energy_taken_user
    offerdata.loc[selected_hour, 'battery user price'] = price_taken_user
    offerdata.to_excel(file_path, index=False)
# Plot the data
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=user_data['Hour'],
    y=user_data['Excess energy'],
    mode='lines+markers',
    name='Battery Level'
))

fig.update_layout(
    title='Battery Levels Over 24 Hours',
    xaxis_title='Hour',
    yaxis_title='Battery Level'
)

#st.plotly_chart(fig)

# Display updated data
st.dataframe(offerdata.loc[selected_hour])
