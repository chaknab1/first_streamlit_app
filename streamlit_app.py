
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My Mom's new healty diner")

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# read CSV file from S3 bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# lets create a pick list to pick the required fruits 
#streamlit.multiselect("Pick some fruits : ", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits : ", list(my_fruit_list.index),['Avocado','Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# display the items in the page
streamlit.dataframe(fruits_to_show)
#streamlit.dataframe(my_fruit_list)

# Create function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #streamlit.dataframe(fruityvice_normalized)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.write('The user entered ', fruit_choice)

#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
#streamlit.text(fruityvice_response.json()) # writes the data on screen

# normalized the json 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display the dataframe
#streamlit.dataframe(fruityvice_normalized)

# don't run anything from here for now
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")

my_data_row = my_cur.fetchall()
streamlit.text("The Fruit Load List contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', add_my_fruit)
streamlit.write('Thanks for adding', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

