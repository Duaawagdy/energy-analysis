import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
# Display the charts in Streamlit
st.title('Energy Production Analysis')

# Load the provider data from the Excel sheet
provider_file_path = r'C:\Users\DELL\energy Analysis\D.W.xlsx'
provider_data = pd.read_excel(provider_file_path, header=0)

# Clean the data: Drop any rows with NaN values in the 'Hours' column
provider_data.dropna(subset=['Hours'], inplace=True)

# Convert the 'Hours' column to integers
provider_data['Hours'] = provider_data['Hours'].astype(int)

# Ensure the columns are numeric
provider_data['PV'] = pd.to_numeric(provider_data['PV'], errors='coerce').fillna(0)
provider_data['Wind'] = pd.to_numeric(provider_data['Wind'], errors='coerce').fillna(0)
provider_data['Hydro'] = pd.to_numeric(provider_data['Hydro'], errors='coerce').fillna(0)
provider_data['non-renewable'] = pd.to_numeric(provider_data['non-renewable'], errors='coerce').fillna(0)
provider_data['price offer $/MWH (weighted average)'] = pd.to_numeric(provider_data['price offer $/MWH (weighted average)'], errors='coerce').fillna(0)
provider_data['load MW'] = pd.to_numeric(provider_data['load MW'], errors='coerce').fillna(0)
provider_data['user']=pd.to_numeric(provider_data['user'], errors='coerce').fillna(0)
# Create the first stacked area chart using Plotly
fig1 = go.Figure()

fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['PV'],
    mode='lines',
    name='PV',
    stackgroup='one',
    line=dict(width=0.5, color='#ff0000'),
    hoverinfo='x+y'
))

fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['Hydro'],
    mode='lines',
    name='Hydro',
    stackgroup='one',
    line=dict(width=0.5, color='rgb(179, 222, 105)'),
    hoverinfo='x+y'
))
fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['Wind'],
    mode='lines',
    name='Wind',
    stackgroup='one',
    line=dict(width=0.5, color='rgb(183, 178, 175)'),
    hoverinfo='x+y'
))
fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['price offer $/MWH (weighted average)'],
    mode='lines',
    name='Price Offer $/MWH',
    line=dict(width=2, color='rgb(0, 0, 255)'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['non-renewable'],
    mode='lines',
    name='non-renewable',
    stackgroup='one',
    line=dict(width=0.5, color='#ff9a00'),
    hoverinfo='x+y'
))

shapes = []
y_max = provider_data[['PV', 'Wind', 'Hydro', 'non-renewable']].sum(axis=1).max()
for y in range(0, int(y_max) + 1, 2000):  # Adjust the step size as needed
    if y != 0:  # Exclude the shape that creates the dashed line
        shapes.append(dict(
            type='line',
            x0=1,
            x1=24,
            y0=y,
            y1=y,
            line=dict(
                color="gray",
                width=0.5,
            ),
        ))
# Customize the layout for the first figure
fig1.update_layout(
    title='Energy Production Types Over 24 Hours',
    xaxis=dict(
        title='Hour',
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title='Power (MW)',
        tickformat=','
    ),
    yaxis2=dict(
        title='Price Offer $/MWH',
        overlaying='y',
        side='right'
        
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified',
    shapes=shapes 
)

# Display the first chart
st.plotly_chart(fig1)

# Create the second chart for coal load MW
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['load MW'],
    mode='lines+markers',
    name='Coal Load MW',
    line=dict(width=1, color='#cc0000'),
    hoverinfo='x+y'
))

fig2.update_layout(
    title=' Load Over 24 Hours',
    xaxis_range=[1,24],
    xaxis=dict(
        title='Hour',
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title=' Load (MW)',
        tickformat=','
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the second chart
st.plotly_chart(fig2)

# Inputs from user
st.sidebar.header("buy Parameters")
start_hour = st.sidebar.number_input("Start Hour", min_value=1, max_value=24, step=1)
end_hour = st.sidebar.number_input("End Hour", min_value=1, max_value=24, step=1)
min_price = st.sidebar.number_input("Minimum Price Offer $/MWH")
electricity_amount = st.sidebar.number_input("Minimum Amount of Electricity (MW)")

# "Buy Now" button
if st.sidebar.button('Buy Now'):
    if start_hour > end_hour:
        st.sidebar.error("End hour must be greater than or equal to start hour.")
    else:
        # Create a new column with the specified electricity amount for the specified hours
        #provider_data['user'] = ''
        provider_data.loc[(provider_data['Hours'] >= start_hour) & (provider_data['Hours'] <= end_hour), 'user'] = electricity_amount
        provider_data.loc[(provider_data['Hours'] >= start_hour) & (provider_data['Hours'] <= end_hour), 'price selled'] = min_price
        # Save the updated DataFrame back to the Excel file
        provider_data.to_excel(provider_file_path, index=False)
        fig3 = go.Figure()
        user_trace = go.Scatter(
            x=provider_data['Hours'],
            y=provider_data['user'],
              # Line chart for user data
            name='User Purchase',
            stackgroup='one',
            line=dict(width=2, color='green'),  # Customize line style
            hoverinfo='x+y'
        )
        user_trace2=go.Scatter(
            x=provider_data['Hours'], 
            y=provider_data['price selled'],
            mode='lines',
           name='Priceselled',
           yaxis='y2',
            line=dict(width=2, color='rgb(0, 0, 255)'),
             
             hoverinfo='x+y'
       )
        fig3.add_trace(user_trace)
        fig3.add_trace(user_trace2)
        fig3.update_layout(
    title=' Load Over 24 Hours',
    xaxis_range=[1,24],
    xaxis=dict(
        title='Hour',
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title=' Load (MW)',
        tickformat=','
    ),
    yaxis2=dict(
        title='Price Offer $/MWH',
        overlaying='y',
        side='right'
        
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)
        st.plotly_chart(fig3)
        st.sidebar.success("Data updated with the user's specified electricity amount.")
        st.write(provider_data)
        
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
