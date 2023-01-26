import streamlit as st
import altair as alt
from vega_datasets import data
import pandas as pd

# Since the data is more than 5,000 rows we'll import it from a URL
df = pd.read_csv('zipcodes.csv')

st.title("US Zip codes segmented with leading digit")

if st.sidebar.checkbox("Show Dataset"):
    st.write(df)

c = alt.Chart(df).transform_calculate(
    "leading digit", alt.expr.substring(alt.datum.zip_code, 0, 1)
).mark_circle(size=3).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    color='leading digit:N',
    tooltip=['state:N', 'county:N', 'zip_code:N']
).project(
    type='albersUsa'
).properties(
    width=650,
    height=400
)

st.altair_chart(c, use_container_width=True)

# 2
st.title("Seattle weather analysis by date")
source = data.seattle_weather()

scale = alt.Scale(domain=['sun', 'fog', 'drizzle', 'rain', 'snow'],
                  range=['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4', '#9467bd'])
color = alt.Color('weather:N', scale=scale)

# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=['x'])
click = alt.selection_multi(encodings=['color'])

# Top panel is scatter plot of temperature vs time
points = alt.Chart().mark_point().encode(
    alt.X('monthdate(date):T', title='Date'),
    alt.Y('temp_max:Q',
        title='Maximum Daily Temperature (C)',
        scale=alt.Scale(domain=[-5, 40])
    ),
    color=alt.condition(brush, color, alt.value('lightgray')),
    size=alt.Size('precipitation:Q', scale=alt.Scale(range=[5, 200]))
).properties(
    width=550,
    height=300
).add_selection(
    brush
).transform_filter(
    click
).interactive()

# Bottom panel is a bar chart of weather type
bars = alt.Chart().mark_bar().encode(
    x='count()',
    y='weather:N',
    color=alt.condition(click, color, alt.value('lightgray')),
).transform_filter(
    brush
).properties(
    width=550,
).add_selection(
    click
).interactive()

point_bar = alt.vconcat(
    points,
    bars,
    data=source,
    title="Seattle Weather: 2012-2015"
)

if st.sidebar.checkbox("Show Seattle weather Data"):
    st.write(source)
st.write(point_bar)