import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_navigation_bar import st_navbar

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
navbar_html = '''
<style>
    .st-emotion-cache-h4xjwg{
        z-index: 100;
    }
    .css-hi6a2p {padding-top: 0rem;}
    .navbar {
        background-color: #007BFF;
        padding: 0.3rem;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar .logo {
        display: flex;
        align-items: center;
    }
    .navbar .logo img {
        height: 40px;
        margin-right: 10px;
    }
    .navbar .menu {
        display: flex;
        gap: 1.5rem;
    }
    .navbar .menu a {
        color: white;
        font-size: 1.2rem;
        text-decoration: none;
    }
    .content {
        padding-top: 5rem;  /* Adjust this based on navbar height */
    }
</style>

<nav class="navbar">
    <div class="logo">
        <h3>Antimicrobial Resistant Dashboard</h3>
    </div>
    <div class="menu">
        <a href="">Dashboard</a>
        <a href="mvp">Multi Variable Plots</a>
        <a href="chatbot">ChatBot</a>
        <a href="mlp">ML Predictions</a>
        <a href="ml-predictions">About Us</a>
    </div>
</nav>

<div class="content">
'''



# Injecting the navigation bar and content padding into the Streamlit app
st.markdown(navbar_html, unsafe_allow_html=True)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#plot 1
import pandas as pd
import plotly.graph_objects as go
df = pd.read_csv('../venatorx.csv')
df_ecoli = df[df['Organism'] == 'Escherichia coli']
df_ecoli = df_ecoli.dropna(subset=['CAZ_MIC', 'Year'])
df_ecoli['CAZ_MIC'] = pd.to_numeric(df_ecoli['CAZ_MIC'], errors='coerce')
df_ecoli['Year'] = pd.to_numeric(df_ecoli['Year'], errors='coerce')
yearly_data = df_ecoli.groupby('Year').agg(
    avg_caz_mic=('CAZ_MIC', 'mean'),
    case_count=('CAZ_MIC', 'count')
).reset_index()
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=yearly_data['Year'],
        y=yearly_data['avg_caz_mic'],
        mode='lines+markers',
        name='Average CAZ_MIC',
        marker=dict(color='rgba(255, 0, 0, 1)'),
        hoverinfo='x+y'
    )
)
fig.add_trace(
    go.Bar(
        x=yearly_data['Year'],
        y=yearly_data['case_count'],
        name='Case Count',
        yaxis='y2',
        marker=dict(color='rgba(0, 123, 255, 0.4)'),
        hoverinfo='x+y'
    )
)
fig.update_layout(
    title="Antibiotic Resistance (CAZ_MIC) Trends Over Time with Case Counts",
    xaxis=dict(title='Year'),
    yaxis=dict(title='Average CAZ_MIC'),
    yaxis2=dict(title='Case Count', overlaying='y', side='right'),
    hovermode='x unified',
    legend=dict(x=0.1, y=1.1, orientation='h'),
    bargap=0.2
)

#plot 2
df_ecoli = df[df['Organism'] == 'Escherichia coli']

# Remove any rows where CAZ_MIC or Year might be missing
df_ecoli = df_ecoli.dropna(subset=['CAZ_MIC', 'Age', 'Year'])

# Convert relevant columns to numeric
df_ecoli['CAZ_MIC'] = pd.to_numeric(df_ecoli['CAZ_MIC'], errors='coerce')
df_ecoli['Age'] = pd.to_numeric(df_ecoli['Age'], errors='coerce')

# Create age groups
age_groups = pd.cut(df_ecoli['Age'], bins=[0, 20, 40, 60, 80, 100], labels=["0-20", "21-40", "41-60", "61-80", "81-100"])

# Plot the box plot
fig2 = px.box(df_ecoli, x=age_groups, y='CAZ_MIC', color='Year', title='Distribution of CAZ_MIC by Age Group and Year')


#plot3
df = pd.read_csv('../venatorx.csv')

# Filter data for Escherichia coli
df_ecoli = df[df['Organism'] == 'Escherichia coli']

# Remove any rows where CAZ_MIC, Year, or Gender might be missing
df_ecoli = df_ecoli.dropna(subset=['CAZ_MIC', 'Year', 'Gender'])

# Convert columns to numeric
df_ecoli['CAZ_MIC'] = pd.to_numeric(df_ecoli['CAZ_MIC'], errors='coerce')
df_ecoli['Year'] = pd.to_numeric(df_ecoli['Year'], errors='coerce')

# Group data by year and gender to calculate average CAZ_MIC
gender_yearly_data = df_ecoli.groupby(['Year', 'Gender']).agg(
    avg_caz_mic=('CAZ_MIC', 'mean')
).reset_index()

# Create the figure
fig3 = go.Figure()

# Add line plot for average CAZ_MIC by gender
for gender in gender_yearly_data['Gender'].unique():
    gender_data = gender_yearly_data[gender_yearly_data['Gender'] == gender]
    
    fig3.add_trace(
        go.Scatter(
            x=gender_data['Year'],
            y=gender_data['avg_caz_mic'],
            mode='lines+markers',
            name=f'Average CAZ_MIC - {gender}',
            hoverinfo='x+y+text',
            text=gender_data['Gender'],  # Show the gender in the hover data
        )
    )
# Update layout
fig3.update_layout(
    title="Antibiotic Resistance (CAZ_MIC) Trends by Gender Over Time",
    xaxis=dict(title='Year'),
    yaxis=dict(title='Average CAZ_MIC'),
    hovermode='x unified',
    legend=dict(x=0.1, y=1.15, orientation='h')
)


#plot 4
df_ecoli = df[df['Organism'] == 'Escherichia coli']

# Remove any rows where CAZ_MIC, Year, or Gender might be missing
df_ecoli = df_ecoli.dropna(subset=['CAZ_MIC', 'Year', 'Gender'])

# Create a pivot table for the surface plot
pivot_df = df_ecoli.pivot_table(
    index='Year', columns='Gender', values='CAZ_MIC', aggfunc='mean'
).reset_index()

# Create the 3D surface plot
fig4 = go.Figure(data=[go.Surface(
    z=pivot_df.drop(columns='Year').values,
    x=pivot_df['Year'],
    y=pivot_df.columns[1:],
    colorscale='Viridis'
)])

# Update layout
fig4.update_layout(
    title="3D Surface Plot of Antibiotic Resistance by Gender and Year",
    scene=dict(
        xaxis_title='Year',
        yaxis_title='Gender',
        zaxis_title='CAZ_MIC (Antibiotic Resistance)'
    ),
    margin=dict(l=0, r=50, t=100, b=50)
)

#plot 5
df_ecoli = df[df['Organism'] == 'Escherichia coli']

# Aggregate the data by BodySite and get the top 10 sources
source_data = df_ecoli['BodySite'].value_counts().reset_index().head(10)
source_data.columns = ['BodySite', 'Counts']

# Create the Bar chart for the top 10 sources
fig5 = px.bar(
    source_data,
    x='BodySite',
    y='Counts',
    title="Top 10 Sources of E. coli Cases by Body Site",
    labels={'BodySite': 'Source (Body Site)', 'Counts': 'Number of Cases'},
    color_discrete_sequence=['#636EFA']  # A single color for simplicity
)

# Update layout
fig5.update_layout(
    xaxis_title="Source (Body Site)",
    yaxis_title="Number of Cases",
    hovermode='x unified',
    margin=dict(t=50, l=50, r=50, b=50),
)




a,b = st.columns([0.3,0.7])
with a:
    with st.container(border=True):
        from streamlit_option_menu import option_menu
        sel = option_menu("Multi-Variable Plots", ["Antibiotic Resistance - Region - Time", 'Antibiotic Resistance - Time - Case Counts','Antibiotic Resistance - Time - Gender','Antibiotic Resistance - Time - Gender (3D)',"Top 10 Sources of E. coli Cases by Body Site"], menu_icon="graph", default_index=0)
        if sel=="Antibiotic Resistance - Region - Time":
            with b:
                with st.container(border=True):
                    st.header("Antibiotic Resistance (CAZ_MIC) Trends by Region Over Time")
                    st.plotly_chart(fig2)
        elif sel=="Antibiotic Resistance - Time - Case Counts":
            with b:
                with st.container(border=True):
                    st.header("Antibiotic Resistance (CAZ_MIC) Trends by Time Over Case Counts")
                    st.plotly_chart(fig)
        elif sel=="Antibiotic Resistance - Time - Gender":
            with b:
                with st.container(border=True):
                    st.header("Antibiotic Resistance (CAZ_MIC) Trends by Time Over Gender")
                    st.plotly_chart(fig3)
        elif sel=="Antibiotic Resistance - Time - Gender (3D)":
            with b:
                with st.container(border=True):
                    st.header("Antibiotic Resistance (CAZ_MIC) Trends by Time Over Gender 3D")
                    st.plotly_chart(fig4)
        elif sel=="Top 10 Sources of E. coli Cases by Body Site":
            with b:
                with st.container(border=True):
                    st.header("Top 10 Sources of E. coli Cases by Body Site")
                    st.plotly_chart(fig5)


