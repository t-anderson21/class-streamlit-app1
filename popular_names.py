import pandas as pd
import plotly.express as px
import streamlit as st

st.title('Popular Name Trends (1910-2021)')
st.caption("Practice for my Stat 386 class")

st.divider()

url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
df = pd.read_csv(url)

name = st.text_input('Enter a name', value = 'John')
name_df = df[df['name'] == name]

st.header(f'{name} usage over the years')

st.caption("Toggle between Female & Male trends")
tab1, tab2 = st.tabs(['Female', 'Male'])

with tab1:
    plot_df = name_df[name_df['sex']=='F']
    fig_f = px.line(data_frame = plot_df, x ='year', y='n')
    st.plotly_chart(fig_f)

with tab2:
    plot_df = name_df[name_df['sex']=='M']
    fig_m = px.line(data_frame = plot_df, x ='year', y='n')
    st.plotly_chart(fig_m)

with st.sidebar:

    year = st.slider('Choose a year', 1910, 2021)
    st.header(f'Top names by {year}')
    year_df = df[df['year']==year]
    
    girls_names = year_df[year_df.sex=='F'].sort_values('n', ascending=False).head(5)['name']
    boys_names = year_df[year_df.sex=='M'].sort_values('n', ascending=False).head(5)['name']

    top_names = pd.concat([girls_names.reset_index(drop=True), boys_names.reset_index(drop=True)], 
          ignore_index=True, axis=1)
    top_names.columns = ['Girls','Boys']
    top_names.index = [1,2,3,4,5]
    st.dataframe(top_names)



# Aggregate data by name and sum up the occurrences
popular_names_df = df.groupby('name')['n'].sum().reset_index()
popular_names_df = popular_names_df.rename(columns={'name': 'first name','n': 'total'})

# Sort the DataFrame by the total occurrences to get the most popular names
popular_names_df = popular_names_df.sort_values(by='total', ascending=False)

# Select the top 10 most popular names
top_names_df = popular_names_df.head(10)

# Create the bar chart using Plotly Express
fig_top10 = px.bar(top_names_df, x='first name', y='total', title='Top 10 Most Popular Names', color_discrete_sequence=['green'])
fig_top10.update_layout(xaxis_title='Name', yaxis_title='Total Occurrences')

st.plotly_chart(fig_top10)

#name_df.groupby('year')['n'].sum().reset_index()  # sum of people named Arthur in the year
#fig = px.line(data_frame = name_df, x = 'year', y = 'n')

# Define the label for the button
button_label = "Visit SSA Baby Names"

# Define the URL to redirect to when the button is clicked
url = "https://www.ssa.gov/oact/babynames/limits.html"

# Create a clickable button
url = "https://www.ssa.gov/oact/babynames/limits.html"
if st.button("Go to Social Security Baby Names"):
    st.markdown(f"[Baby Names Website]({url})")

# https://class-app-app1-6wncbftxutalqdvzn5tsed.streamlit.app
st.caption("Source: popular_names.csv from Social Security website")