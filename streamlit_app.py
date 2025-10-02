# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

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
session = cnx.session 

# Query the fruit options table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Create the multiselect widget
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe, 
    max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''

    # Build the ingredients string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Build the insert statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
