import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
user_file_path = r'C:\Users\DELL\energy Analysis\Battery.xlsx'

user_data = pd.read_excel(user_file_path, header=0)
user_data.dropna(subset=['Hour'], inplace=True)
user_data['Hour']=user_data['Hour'].astype(int)
user_data['user 1'] = pd.to_numeric(user_data['user 1'], errors='coerce').fillna(0)
user_data['user 2'] = pd.to_numeric(user_data['user 2'], errors='coerce').fillna(0)
user_data['user 3'] = pd.to_numeric(user_data['user 3'], errors='coerce').fillna(0)
user_data['user 4'] = pd.to_numeric(user_data['user 4'], errors='coerce').fillna(0)
user_data['user 5'] = pd.to_numeric(user_data['user 5'], errors='coerce').fillna(0)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=user_data['Hour'], y=user_data['user 1'],
    mode='lines',
    name='user 1 load',
    #stackgroup='one',
    line=dict(width=2, color='#ffd966'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=user_data['Hour'], y=user_data['user 2'],
    mode='lines',
    name='user 2 load',
    #stackgroup='one',
    line=dict(width=2, color='#ff0000'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=user_data['Hour'], y=user_data['user 3'],
    mode='lines',
    name='user 3 load',
    #stackgroup='one',
    line=dict(width=2, color='#ff9a00'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=user_data['Hour'], y=user_data['user 4'],
    mode='lines',
    name='user 4 load',
    #stackgroup='one',
    line=dict(width=2, color='#b30000'),
    hoverinfo='x+y'
))
fig.add_trace(go.Scatter(
    x=user_data['Hour'], y=user_data['user 5'],
    mode='lines',
    name='user 5 load',
    #stackgroup='one',
    line=dict(width=2, color='rgb(179, 222, 105)'),
    hoverinfo='x+y'
))
fig.update_layout(
    title='users load Over 24 Hours ',
    xaxis=dict(
        title='Hour',
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    yaxis=dict(
        title='load (MW)',
        tickformat=','
    ),
    
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
st.plotly_chart(fig)
file_path = r'C:\Users\DELL\energy Analysis\operator.xlsx'  
offerdata = pd.read_excel(file_path, header=0)




# Create the second chart for coal load MW

# Inputs from user
start_hour = st.sidebar.number_input("Start Hour", min_value=0, max_value=23, step=1)
end_hour = st.sidebar.number_input("End Hour", min_value=0, max_value=23, step=1)
user_id = st.sidebar.selectbox("Select User ID", ['user 1', 'user 2', 'user 3', 'user 4','user 5'])
st.sidebar.header("Offer Details")

min_price = st.sidebar.number_input("Minimum Price Offer $/MWH")
electricity_amount = st.sidebar.number_input("Minimum Amount of Electricity (MW)")
max_energy=user_data.loc[(user_data['Hour'] >= start_hour) & (user_data['Hour'] <= end_hour), f'{user_id}']

# "Send Offer" button
if st.sidebar.button('Send Offer for user'):
    if start_hour > end_hour:
        st.sidebar.error("Start Hour cannot be greater than End Hour")
    elif (max_energy < electricity_amount).any():
        st.sidebar.error("Your required energy is more than your maximum value!")
    else:
        offerdata.loc[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour), f'{user_id} Energy'] = electricity_amount
        offerdata.loc[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour), f'{user_id} price'] = min_price
        
        
        #offerdata.replace(0, pd.NA, inplace=True)
        # Save the updated data back to the Excel file
        offerdata.to_excel(file_path, index=False)
        
        
        
        # Display the updated data
        st.sidebar.success("User data updated successfully.")
        #diffpriceprovider1=offerdata.loc[ start_hour &  end_hour, 'provider 1price']-min_price
        #diffpriceprovider2=offerdata.loc[start_hour &  end_hour, 'provider 2price']-min_price
        #diffpriceprovider3=offerdata.loc[start_hour &  end_hour, 'provider 3price']-min_price
        st.write("### Updated Data")
        
        st.dataframe(offerdata[(offerdata['hours'] >= start_hour) & (offerdata['hours'] <= end_hour)])
        # Create a new chart to display the user's purchase data
        fig3 = go.Figure()
        provider_trace = go.Scatter(
            x=offerdata['hours'],
            y=offerdata['provider 1Energy'],
            mode='lines',
            name='provider 1',
            stackgroup='one',
            line=dict(width=2, color='#ffd966'),
            hoverinfo='x+y'
        )
        user_trace = go.Scatter(
            x=offerdata['hours'],
            y=offerdata[f'{user_id} Energy'],
            mode='lines+markers',
            name='User needed energy',
            #stackgroup='one',
            line=dict(width=2, color='green'),
            hoverinfo='x+y'
        )
        provider_trace2 = go.Scatter(
            x=offerdata['hours'], 
            y=offerdata['provider 1price'],
            mode='lines',
            name='provider 1 price selled',
            yaxis='y2',
            line=dict(width=2, color='#b30000'),
         hoverinfo='x+y'
        )
        user_trace2 = go.Scatter(
            x=offerdata['hours'], 
            y=offerdata[f'{user_id} price'],
            mode='lines+markers',
            name='user Price offer',
            yaxis='y2',
            line=dict(width=2, color='rgb(0, 0, 255)'),
         hoverinfo='x+y'
        )
        fig3.add_trace(user_trace)
        fig3.add_trace(user_trace2)
        fig3.add_trace(provider_trace)
        fig3.add_trace(provider_trace2)
        fig3.update_layout(
            title='Offers Over 24 Hours',
            xaxis_range=[0,23],
            xaxis=dict(
                title='Hour',
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            yaxis=dict(
                title='Load (MW)',
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
        #st.write("      proviser 1 difference price: "+str(diffpriceprovider1)+" at hour "+str(start_hour))
        st.plotly_chart(fig3)
       
        fig4 = go.Figure()
        provider2_trace = go.Scatter(
            x=offerdata['hours'],
            y=offerdata['provider 2Energy'],
            mode='lines',
            name='provider 2',
            stackgroup='one',
            line=dict(width=2, color='#ffd966'),
            hoverinfo='x+y'
        )
        user_trace = go.Scatter(
            x=offerdata['hours'],
            y=offerdata[f'{user_id} Energy'],
            mode='lines+markers',
            name='User needed energy',
            #stackgroup='one',
            line=dict(width=2, color='green'),
            hoverinfo='x+y'
        )
        provider2_trace2 = go.Scatter(
            x=offerdata['hours'], 
            y=offerdata['provider 2price'],
            mode='lines',
            name='provider 2 price selled',
            yaxis='y2',
            line=dict(width=2, color='#b30000'),
         hoverinfo='x+y'
        )
        user_trace2 = go.Scatter(
            x=offerdata['hours'], 
            y=offerdata[f'{user_id} price'],
            mode='lines+markers',
            name='user Price offer',
            yaxis='y2',
            line=dict(width=2, color='rgb(0, 0, 255)'),
         hoverinfo='x+y'
        )
        fig4.add_trace(user_trace)
        fig4.add_trace(user_trace2)
        fig4.add_trace(provider2_trace)
        fig4.add_trace(provider2_trace2)
        fig4.update_layout(
           
            xaxis_range=[0,23],
            xaxis=dict(
                title='Hour',
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            yaxis=dict(
                title='Load (MW)',
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
        #st.write("      proviser 2 difference price: "+str(diffpriceprovider2)+" at hour "+str(start_hour))
        st.plotly_chart(fig4)
        fig5 = go.Figure()
        provider3_trace = go.Scatter(
            x=offerdata['hours'],
            y=offerdata['provider 3Energy'],
            mode='lines',
            name='provider 3',
            stackgroup='one',
            line=dict(width=2, color='#ffd966'),
            hoverinfo='x+y'
        )
        user_trace = go.Scatter(
            x=offerdata['hours'],
            y=offerdata[f'{user_id} Energy'],
            mode='lines+markers',
            name='User needed energy',
           
            line=dict(width=2, color='green'),
            hoverinfo='x+y'
        )
        provider3_trace2 = go.Scatter(
            x=offerdata['hours'], 
            y=offerdata['provider 3price'],
            mode='lines',
            name='provider 3 price selled',
            yaxis='y2',
            line=dict(width=2, color='#b30000'),
         hoverinfo='x+y'
        )
        user_trace2 = go.Scatter(
            x=offerdata['hours'], 
            y=offerdata[f'{user_id} price'],
            mode='lines+markers',
            name='user Price offer',
            yaxis='y2',
            line=dict(width=2, color='rgb(0, 0, 255)'),
         hoverinfo='x+y'
        )
        fig5.add_trace(user_trace)
        fig5.add_trace(user_trace2)
        fig5.add_trace(provider3_trace)
        fig5.add_trace(provider3_trace2)
        fig5.update_layout(
            
            xaxis_range=[0,23],
            xaxis=dict(
                title='Hour',
                tickmode='linear',
                tick0=1,
                dtick=1
            ),
            yaxis=dict(
                title='Load (MW)',
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
        #st.write("      proviser 3 difference price: "+str(diffpriceprovider3)+" at hour "+str(start_hour))
        st.plotly_chart(fig5)

        
        
        