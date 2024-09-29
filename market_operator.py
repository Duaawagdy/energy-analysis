import pandas as pd
import os
import plotly.graph_objects as go
import streamlit as st
import json
from streamlit_extras.stylable_container import stylable_container
st.set_page_config(page_title="AFT for Energy exchange", page_icon=":bar_chart:", layout="wide")
#st.page_link("home.py", label="Home", icon="🏠")
#st.page_link("pages/battery.py")
# Load the provider data from the Excel sheet
transaction_file_path = r'C:\Users\DELL\energy Analysis\transaction.xlsx'

transaction_data = pd.read_excel(transaction_file_path, header=0)
transaction_data.dropna(subset=['hours'], inplace=True)

# Convert the 'Hours' column to integers
transaction_data['hours'] = transaction_data['hours'].astype(int)

# Ensure the columns are numeric
transaction_data['total quantity'] = pd.to_numeric(transaction_data['total quantity'], errors='coerce').fillna(0)
transaction_data['price'] = pd.to_numeric(transaction_data['price'], errors='coerce').fillna(0)
def day_ahead_market(providers, users):
    providers.sort(key=lambda x: x['price'])
    users.sort(key=lambda x: x['price'], reverse=True)
    
    total_supply = 0
    total_demand = 0
    transactions = []

    for hour in range(24):  # Assuming `hours` represents a 24-hour period
        while providers and users:
            lowest_supply = providers[0]
            highest_demand = users[0]
            
            if lowest_supply['price'] <= highest_demand['price']:
                if lowest_supply['quantity'] >= highest_demand['quantity']:
                    transactions.append({
                        'provider': lowest_supply['provider'],
                        'user': highest_demand['user'],
                        'quantity': highest_demand['quantity'],
                        'price': lowest_supply['price']
                    })
                    lowest_supply['quantity'] -= highest_demand['quantity']
                    total_supply += highest_demand['quantity']
                    users.pop(0)
                else:
                    transactions.append({
                        'provider': lowest_supply['provider'],
                        'user': highest_demand['user'],
                        'quantity': lowest_supply['quantity'],
                        'price': lowest_supply['price']
                    })
                    highest_demand['quantity'] -= lowest_supply['quantity']
                    total_demand += lowest_supply['quantity']
                    providers.pop(0)
            else:
                break

    market_clearing_price = transactions[-1]['price'] if transactions else None
    return transactions, market_clearing_price
def highest_Price(providers, users):
    providers.sort(key=lambda x: x['price'], reverse=True)  # Sort providers by price descending
    users.sort(key=lambda x: x['price'], reverse=True)      # Sort users by price descending
    
    transactions = []

    for hour in range(24):                          # Assuming hours represent a 24-hour period
        for user in users[:]:                       # Iterate over a copy of the users list
            for provider in providers[:]:           # Iterate over a copy of the providers list
                if provider['price'] <= user['price']:
                    if provider['quantity'] >= user['quantity']:
                        transactions.append({
                            'provider': provider['provider'],
                            'user': user['user'],
                            'quantity': user['quantity'],
                            'price': provider['price']
                        })
                        provider['quantity'] -= user['quantity']
                        users.remove(user)   # Remove the user once they are fully served
                        break                # Move on to the next user
                    else:
                        transactions.append({
                            'provider': provider['provider'],
                            'user': user['user'],
                            'quantity': provider['quantity'],
                            'price': provider['price']
                        })
                        user['quantity'] -= provider['quantity']
                        providers.remove(provider)  # Remove the provider once it's exhausted

                        # Continue serving the user with the next available provider
                else:
                    continue  # Try the next provider

    market_clearing_price = transactions[-1]['price'] if transactions else None
    return transactions, market_clearing_price
def lowest_Quantity(providers, users):
    # Sort providers by price descending
    providers.sort(key=lambda x: x['price'], reverse=True)
    # Sort users by quantity ascending
    users.sort(key=lambda x: x['quantity'])
    
    transactions = []

    while users:  # While there are users to process
        user = users.pop(0)  # Get the next user to process
        for provider in providers[:]:  # Iterate over a copy of the providers list
            if provider['price'] <= user['price']:  # Check if provider's price is within the user's budget
                if provider['quantity'] >= user['quantity']:
                    transactions.append({
                        'provider': provider['provider'],
                        'user': user['user'],
                        'quantity': user['quantity'],
                        'price': provider['price']
                    })
                    provider['quantity'] -= user['quantity']
                    break  # Move on to the next user
                else:
                    transactions.append({
                        'provider': provider['provider'],
                        'user': user['user'],
                        'quantity': provider['quantity'],
                        'price': provider['price']
                    })
                    user['quantity'] -= provider['quantity']
                    providers.remove(provider)  # Remove the provider once it's exhausted
                    # Continue serving the user with the next available provider
            else:
                continue  # Try the next provider

    market_clearing_price = transactions[-1]['price'] if transactions else None
    return transactions, market_clearing_price
battery_file_path = r'C:\Users\DELL\energy Analysis\Battery.xlsx'
battery_data = pd.read_excel(battery_file_path, header=0)
battery_data.dropna(subset=['Hour'], inplace=True)
battery_data['Hour']=battery_data['Hour'].astype(int)
battery_data['Excess energy'] = pd.to_numeric(battery_data['Excess energy'], errors='coerce').fillna(0)
battery_data['deficited energy'] = pd.to_numeric(battery_data['deficited energy'], errors='coerce').fillna(0)
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
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
#st.plotly_chart(fig)

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
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
#st.plotly_chart(fig1)
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
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='x unified'
)

# Display the first chart
#st.plotly_chart(fig2)
# Create the second chart for coal load MW

# Inputs from user
start_hour = st.number_input("enter Hour", min_value=0, max_value=23, step=1)
#end_hour = st.number_input("End Hour", min_value=0, max_value=23, step=1)
row_data = offerdata[offerdata['hours'] == start_hour]
user_data = row_data[['user 1 Energy', 'user 2 Energy','user 3 Energy', 'user 4 Energy','user 5 Energy','battery user Energy' ]]
data_list = user_data.iloc[0].tolist()
rowprice_data = offerdata[offerdata['hours'] == start_hour]
userprice_data = rowprice_data[['user 1 price', 'user 2 price','user 3 price', 'user 4 price','user 5 price','battery user price' ]]
dataprice_list = userprice_data.iloc[0].tolist()
users = [{'user': f'user_{i+1}', 'quantity': data_list[i], 'price': dataprice_list[i]} for i in range(len(data_list))]
#dataprice_list.append(0)
#data_list.append(battery_data.at[start_hour,'Excess energy'])
st.write('at hour  '+str(start_hour)+' offers to buy energy')
#df = pd.DataFrame( columns=[" at hour "+str(start_hour),"Identifier", "Amount[MW]", "Price"])
df1=pd.DataFrame({
                   'Identifier': ['u1','u2','u3','u4','u5','Battery' ],
                   'Amount[MW]': data_list
                   ,'price[$/MWH]' : dataprice_list,
                   
                   
                   },
                   )
st.dataframe(df1)
prow_data = offerdata[offerdata['hours'] == start_hour]
prov_data = prow_data[['provider 1Energy', 'provider 2Energy','provider 3Energy','battery provider Energy']]
data_plist = prov_data.iloc[0].tolist()
rowpprice_data = offerdata[offerdata['hours'] == start_hour]
provprice_data = rowpprice_data[['provider 1price', 'provider 2price','provider 3price','battery provider price' ]]
datapprice_list = provprice_data.iloc[0].tolist()
providers = [{'provider': f'provider_{i+1}', 'quantity': data_plist[i], 'price': datapprice_list[i]} for i in range(len(data_plist))]
#datapprice_list.append(0)
#data_plist.append(battery_data.at[start_hour,'deficited energy'])
st.write('at hour  '+str(start_hour)+' bids to sell energy')
#df = pd.DataFrame( columns=[" at hour "+str(start_hour),"Identifier", "Amount[MW]", "Price"])
df2=pd.DataFrame({
                   'Identifier': ['p1','p2','p3', 'Battery'],
                   'Amount[MW]': data_plist
                   ,'price[$/MWH]' : datapprice_list,
                   
                   
                   },
                   )
st.dataframe(df2)
# Run the market function


# Output the results
col1, col2,col3 = st.columns(3)

with col1:
    providersselling=[]
    quantitiessolled=[]
    prices=[]
    if st.button('Day Ahead Market Lowest Price'):
        transactions, market_clearing_price = day_ahead_market(providers, users)
        st.write("Transactions:")
        container = st.container()  # Create a container for the transactions
        sumquantity=0
        for transaction in transactions:
            
            provider = transaction["provider"].replace("provider_", "Provider ")
            user = transaction["user"].replace("user_", "User ")
            quantity = transaction["quantity"]
            price = transaction["price"]
            providersselling.append(provider)
            quantitiessolled.append(quantity)
            prices.append(price)
        
            sentence = f"{provider} sells to {user} quantity {quantity} with price {price}."
            container.write(sentence)
            sumquantity=sumquantity+quantity
        container.write("Market Clearing Price: " + str(market_clearing_price))
        container.write("total: " + str(sumquantity))
        transaction_data.loc[  start_hour , 'total quantity']=sumquantity
        transaction_data.loc[  start_hour , 'price']=market_clearing_price
        transaction_data.to_excel(transaction_file_path, index=False)
        #st.write(transaction_data)
        
        

# Create figure
        fig7 = go.Figure()

# Add bar for quantities
        fig7.add_trace(go.Bar(
    x=providersselling,
    y=quantitiessolled,
    name='Quantity',
    marker_color='#00ff99',
    hoverinfo='text'
))

# Add line for prices with secondary y-axis
        fig7.add_trace(go.Scatter(
    x=providersselling,
    y=prices,
    name='Price',
    mode='lines+markers',
    line=dict(color='red', width=1),
    marker=dict(size=5),
    text=[f'Price: {p}' for p in prices],
    hoverinfo='text',
    yaxis='y2'  # Link this trace to yaxis2
))

# Update layout with secondary y-axis
        fig7.update_layout(
    title='Transaction Details',
    xaxis_title='Transaction',
    yaxis_title='Quantity',
    yaxis=dict(
        title='Quantity',
    ),
    yaxis2=dict(
        title='Price',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    barmode='group',
    template='plotly',
  )

# Show figure
        st.plotly_chart(fig7)

figtra = go.Figure()

figtra.add_trace(go.Scatter(
    x=transaction_data['hours'], y=transaction_data['total quantity'],
    mode='lines',
    name='total quantity',
    stackgroup='one',
    line=dict(width=0.5, color='#ff0000'),
    hoverinfo='x+y'
))
figtra.add_trace(go.Scatter(
    x=transaction_data['hours'], y=transaction_data['price'],
    mode='lines',
    name='Market Clearing Price',
    line=dict(width=2, color='#b30000'),
    yaxis='y2',
    hoverinfo='x+y'
))
figtra.update_layout(
    title='transaction  Over 24 Hours  ',
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
    hovermode='x unified'
)
st.plotly_chart(figtra)
with col2:
    if st.button('Day Ahead Market Highest Price'):
        transactions, market_clearing_price = highest_Price(providers, users)
        st.write("Transactions:")
        container = st.container()  # Create a container for the transactions
        for transaction in transactions:
            provider = transaction["provider"].replace("provider_", "Provider ")
            user = transaction["user"].replace("user_", "User ")
            quantity = transaction["quantity"]
            price = transaction["price"]
        
            sentence = f"{provider} sells to {user} quantity {quantity} with price {price}."
            container.write(sentence)
        container.write("Market Clearing Price: " + str(market_clearing_price))

with col3:
    if st.button('Day Ahead Market lowest Quantity'):
        transactions, market_clearing_price = lowest_Quantity(providers, users)
        st.write("Transactions:")
        container = st.container()  # Create a container for the transactions
        for transaction in transactions:
            provider = transaction["provider"].replace("provider_", "Provider ")
            user = transaction["user"].replace("user_", "User ")
            quantity = transaction["quantity"]
            price = transaction["price"]
        
            sentence = f"{provider} sells to {user} quantity {quantity} with price {price}."
            container.write(sentence)
        container.write("Market Clearing Price: " + str(market_clearing_price))        
#container.write(sentence)
# Hide Streamlit style elements
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
