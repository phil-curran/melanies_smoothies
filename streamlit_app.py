# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

# Get the Snowpark session object from the Streamlit connection
cnx = st.connection("snowflake")
session = cnx.session() 

session.use_database("SMOOTHIES")
session.use_schema("PUBLIC")

# Query the fruit options table
my_dataframe = session.table("fruit_options").select(col('FRUIT_NAME'))

# Create the multiselect widget
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe, 
    max_selections=5
)

if ingredients_list:
    # Join the list of selected fruits into a single space-separated string
    ingredients_string = " ".join(ingredients_list)

    # Use %s placeholders for values
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                         values (%s, %s)"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Pass the actual values in the 'params' argument
        session.sql(my_insert_stmt, params=[ingredients_string, name_on_order]).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
