import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
#st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
#st.page_link("home.py", label="Home", icon="🏠")
#st.page_link("pages/battery.py")
# Load the provider data from the Excel sheet
user_file_path = r'C:\Users\DELL\energy Analysis\Battery.xlsx'

user_data = pd.read_excel(user_file_path, header=0)
user_data.dropna(subset=['Hour'], inplace=True)
user_data['Hour']=user_data['Hour'].astype(int)
user_data['user 1'] = pd.to_numeric(user_data['user 1'], errors='coerce').fillna(0)
user_data['user 2'] = pd.to_numeric(user_data['user 2'], errors='coerce').fillna(0)
user_data['user 3'] = pd.to_numeric(user_data['user 3'], errors='coerce').fillna(0)
user_data['user 4'] = pd.to_numeric(user_data['user 4'], errors='coerce').fillna(0)
user_data['user 5'] = pd.to_numeric(user_data['user 5'], errors='coerce').fillna(0)
file_path = r'C:\Users\DELL\energy Analysis\operator.xlsx'  
offerdata = pd.read_excel(file_path, header=0)
providerone_file_path = r'C:\Users\DELL\energy Analysis\provider one .xlsx'
providerone_data = pd.read_excel(providerone_file_path, header=0)

provider_file_path = r'C:\Users\DELL\energy Analysis\provider two.xlsx'
provider_data = pd.read_excel(provider_file_path, header=0)

providertree_file_path = r'C:\Users\DELL\energy Analysis\provider three.xlsx'
providerthree_data = pd.read_excel(providertree_file_path, header=0)


providerone_data.dropna(subset=['Hours'], inplace=True)

# Convert the 'Hours' column to integers
providerone_data['Hours'] = providerone_data['Hours'].astype(int)

# Ensure the columns are numeric
providerone_data['load MW'] = pd.to_numeric(providerone_data['load MW'], errors='coerce').fillna(0)
providerone_data['PV'] = pd.to_numeric(providerone_data['PV'], errors='coerce').fillna(0)
providerone_data['Wind'] = pd.to_numeric(providerone_data['Wind'], errors='coerce').fillna(0)
providerone_data['Hydro'] = pd.to_numeric(providerone_data['Hydro'], errors='coerce').fillna(0)
providerone_data['total non-renewable'] = pd.to_numeric(providerone_data['total non-renewable'], errors='coerce').fillna(0)
providerone_data['price offer $/MWH (weighted average)'] = pd.to_numeric(providerone_data['price offer $/MWH (weighted average)'], errors='coerce').fillna(0)
providerone_data['SELLING PRICE'] = pd.to_numeric(providerone_data['SELLING PRICE'], errors='coerce').fillna(0)
# Create the first stacked area chart using Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['PV'],
    mode='lines',
    name='PV',
    stackgroup='one',
    line=dict(width=0.5, color='#ff0000'),
    hoverinfo='x+y'
))

fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['Hydro'],
    mode='lines',
    name='Hydro',
    stackgroup='one',
    line=dict(width=0.5, color='rgb(179, 222, 105)'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['Wind'],
    mode='lines',
    name='Wind',
    stackgroup='one',
    line=dict(width=0.5, color='rgb(183, 178, 175)'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['price offer $/MWH (weighted average)'],
    mode='lines',
    name='Price Offer $/MWH',
    line=dict(width=2, color='rgb(0, 0, 255)'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['SELLING PRICE'],
    mode='lines',
    name='SELLING PRICE',
    line=dict(width=2, color='#b30000'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['total non-renewable'],
    mode='lines',
    name='total non-renewable ',
    stackgroup='one',
    line=dict(width=0.5, color='#ff9a00'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=providerone_data['Hours'], y=providerone_data['load MW'],
    mode='lines',
    name='total supply MW ',
    stackgroup='one',
    line=dict(width=0.5, color='#ffd966'),
    hoverinfo='x+y'
))
# Customize the layout for the first figure
fig.update_layout(
    title='Energy Production Types Over 24 Hours for provider 1 ',
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
    legend=dict(
        x=1.1,  # move the legend to the right, increase the value to add more space
        y=0.5,  # center the legend vertically
        xanchor='left',  # align the legend to the left
        yanchor='middle'
    ),
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
st.plotly_chart(fig)

# Clean the data: Drop any rows with NaN values in the 'Hours' column
provider_data.dropna(subset=['Hours'], inplace=True)

# Convert the 'Hours' column to integers
provider_data['Hours'] = provider_data['Hours'].astype(int)

# Ensure the columns are numeric
provider_data['total supply MW'] = pd.to_numeric(provider_data['total supply MW'], errors='coerce').fillna(0)
provider_data['PV'] = pd.to_numeric(provider_data['PV'], errors='coerce').fillna(0)
provider_data['Wind'] = pd.to_numeric(provider_data['Wind'], errors='coerce').fillna(0)
provider_data['Hydro'] = pd.to_numeric(provider_data['Hydro'], errors='coerce').fillna(0)
provider_data['total non-renewable'] = pd.to_numeric(provider_data['total non-renewable'], errors='coerce').fillna(0)
provider_data['price offer $/MWH (weighted average)'] = pd.to_numeric(provider_data['price offer $/MWH (weighted average)'], errors='coerce').fillna(0)
provider_data['SELLING PRICE'] = pd.to_numeric(provider_data['SELLING PRICE'], errors='coerce').fillna(0)
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
    x=provider_data['Hours'], y=provider_data['SELLING PRICE'],
    mode='lines',
    name='SELLING PRICE',
    line=dict(width=2, color='#b30000'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['total non-renewable'],
    mode='lines',
    name='total non-renewable ',
    stackgroup='one',
    line=dict(width=0.5, color='#ff9a00'),
    hoverinfo='x+y'
))
fig1.add_trace(go.Scatter(
    x=provider_data['Hours'], y=provider_data['total supply MW'],
    mode='lines',
    name='total supply MW ',
    stackgroup='one',
    line=dict(width=0.5, color='#ffd966'),
    hoverinfo='x+y'
))
# Customize the layout for the first figure
fig1.update_layout(
    title='Energy Production Types Over 24 Hours for provider 2 ',
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
    ),legend=dict(
        x=1.1,  # move the legend to the right, increase the value to add more space
        y=0.5,  # center the legend vertically
        xanchor='left',  # align the legend to the left
        yanchor='middle'
    ),
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
st.plotly_chart(fig1)
providerthree_data.dropna(subset=['Hours'], inplace=True)

# Convert the 'Hours' column to integers
providerthree_data['Hours'] = providerthree_data['Hours'].astype(int)

# Ensure the columns are numeric
providerthree_data['total supply MW'] = pd.to_numeric(providerthree_data['total supply MW'], errors='coerce').fillna(0)
providerthree_data['PV'] = pd.to_numeric(providerthree_data['PV'], errors='coerce').fillna(0)
providerthree_data['Wind'] = pd.to_numeric(providerthree_data['Wind'], errors='coerce').fillna(0)
providerthree_data['Hydro'] = pd.to_numeric(providerthree_data['Hydro'], errors='coerce').fillna(0)
providerthree_data['total non-renewable'] = pd.to_numeric(providerthree_data['total non-renewable'], errors='coerce').fillna(0)
providerthree_data['price offer $/MWH (weighted average)'] = pd.to_numeric(providerthree_data['price offer $/MWH (weighted average)'], errors='coerce').fillna(0)
providerthree_data['SELLING PRICE'] = pd.to_numeric(providerthree_data['SELLING PRICE'], errors='coerce').fillna(0)
# Create the first stacked area chart using Plotly
fig2 = go.Figure()


fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['Wind'],
    mode='lines',
    name='Wind',
    stackgroup='one',
    line=dict(width=0.5, color='rgb(183, 178, 175)'),
    hoverinfo='x+y'
))
fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['Hydro'],
    mode='lines',
    name='Hydro',
    stackgroup='one',
    line=dict(width=0.5, color='rgb(179, 222, 105)'),
    hoverinfo='x+y'
))


fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['price offer $/MWH (weighted average)'],
    mode='lines',
    name='Price Offer $/MWH',
    line=dict(width=2, color='rgb(0, 0, 255)'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['SELLING PRICE'],
    mode='lines',
    name='SELLING PRICE',
    line=dict(width=2, color='#b30000'),
    yaxis='y2',
    hoverinfo='x+y'
))
fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['total non-renewable'],
    mode='lines',
    name='total non-renewable ',
    stackgroup='one',
    line=dict(width=0.5, color='#ff9a00'),
    hoverinfo='x+y'
))
fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['PV'],
    mode='lines',
    name='PV',
    stackgroup='one',
    line=dict(width=0.5, color='#ff0000'),
    hoverinfo='x+y'
))
fig2.add_trace(go.Scatter(
    x=providerthree_data['Hours'], y=providerthree_data['total supply MW'],
    mode='lines',
    name='total supply MW ',
    stackgroup='one',
    line=dict(width=0.5, color='#ffd966'),
    hoverinfo='x+y'
))

# Customize the layout for the first figure
fig2.update_layout(
    title='Energy Production Types Over 24 Hours for provider 3 ',
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
    legend=dict(
        x=1.1,  # move the legend to the right, increase the value to add more space
        y=0.5,  # center the legend vertically
        xanchor='left',  # align the legend to the left
        yanchor='middle'
    ),
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
st.plotly_chart(fig2)
# Create the second chart for coal load MW

# Inputs from user
start_hour = st.sidebar.number_input("Start Hour", min_value=0, max_value=23, step=1)
end_hour = st.sidebar.number_input("End Hour", min_value=0, max_value=23, step=1)

#st.dataframe(offerdata[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour)])
        # Create a new chart to display the user's purchase data
st.sidebar.header("provider Details")
provideroffer_id = st.sidebar.selectbox("Select provider", ['provider 1', 'provider 2', 'provider 3'])
provider_amount = st.sidebar.number_input(" Amount of Electricity (MW)")
providerprice=st.sidebar.number_input("provider selling price $/MWH")
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #00b33c;
        color: black;
    }""",
):
    provider_butten=st.sidebar.button('Send Bids for provider ')
    if provider_butten:
      if start_hour > end_hour:
        st.sidebar.error("Start Hour cannot be greater than End Hour")
      
      else:
        offerdata.loc[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour), f'{provideroffer_id}Energy'] = provider_amount
        offerdata.loc[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour), f'{provideroffer_id}price'] = providerprice
        
        #offerdata.replace(0, pd.NA, inplace=True)
        # Save the updated data back to the Excel file
        offerdata.to_excel(file_path, index=False)
        
        
        
        # Display the updated data
        st.sidebar.success("provider data updated successfully.")
        
        st.write("### Updated Data")
        
        st.dataframe(offerdata[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour)])