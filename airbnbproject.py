import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymongo
import mysql.connector
import plotly.express as px
import os


st.set_page_config(page_title='Airbnb by Abin', layout="wide",initial_sidebar_state= "expanded")
page_icon_url = 'D:\GuviProjects\Airbnb Reff\airbnb_logo.png'
# title and position
st.markdown(f'<h1 style="text-align: center;color: Blue;; font-size: 55px;">Airbnb Analysis</h1>', unsafe_allow_html=True)
# st.sidebar.markdown("<h1 style='color: blue;  font-size: 30px;'>Select Your Option</h1>", unsafe_allow_html=True)    

class connection:    
    #Using the PyMongo library to connect to MongoDB database hosted on MongoDB Atlas.
    mydb = pymongo.MongoClient("mongodb+srv://abincbabu05:Guvi12345@cluster0.lasrtaa.mongodb.net/?retryWrites=true&w=majority")
    db = mydb['sample_airbnb']
    col = db['listingsAndReviews']

  


def air_main():
    data = []        
    for i in connection.col.find({}, {'_id': 1, 'listing_url': 1, 'name': 1, 'property_type': 1, 'room_type': 1, 'bed_type': 1,
                                        'minimum_nights': 1, 'maximum_nights': 1, 'cancellation_policy': 1, 'accommodates': 1,
                                        'bedrooms': 1, 'beds': 1, 'number_of_reviews': 1, 'bathrooms': 1, 'price': 1,
                                        'cleaning_fee': 1, 'extra_people': 1, 'guests_included': 1, 'images.picture_url': 1,
                                        'review_scores.review_scores_rating': 1}):
        data.append(i)
    df_main = pd.DataFrame(data)
    
    # check none values
    # contains_none = df_main['bedrooms'].isnull().any()
    # st.write(contains_none)

    # Filling the missing values        
    df_main['bedrooms'].fillna(0, inplace=True)
    df_main['beds'].fillna(0,inplace=True)
    df_main['bathrooms'].fillna(0,inplace=True)
    df_main['cleaning_fee'].fillna(0,inplace=True)        

    # check datatypes 
    # is_integer = df_main['beds'].dtype == 'int64'
    # st.write(is_integer)
    # is_numeric = df_main['beds'].dtype in ['float64']
    # st.write(is_numeric)

    #  Datatype convertion
    df_main['minimum_nights'] = df_main['minimum_nights'].astype(int)
    df_main['maximum_nights'] = df_main['maximum_nights'].astype(int)
    df_main['bedrooms'] = df_main['bedrooms'].astype(int)
    df_main['beds'] = df_main['beds'].astype(int)
    df_main['bathrooms'] = df_main['bathrooms'].astype(str).astype(float)
    df_main['price'] = df_main['price'].astype(str).astype(float).astype(int)        
    df_main['cleaning_fee'] = df_main['cleaning_fee'].astype(str).astype(float).astype(int)        
    df_main['extra_people'] = df_main['extra_people'].astype(str).astype(float).astype(int)
    df_main['guests_included'] = df_main['guests_included'].astype(str).astype(int)

    # Extracting the data from nested dictionary     
    df_main['images'] = df_main['images'].str.get('picture_url')       
    df_main['review_scores'] = df_main['review_scores'].str.get('review_scores_rating')

    return df_main


def streamlit_run():


    # page header transparent colorcd 
    background_color = "!Important"  # Replace this with your desired color code
    page_bg = f"""
        <style>
            .main {{
                background-color: {background_color};
            }}
        </style>
    """
    st.markdown(f""" <style>.stApp {{
                        
                            background-size: cover}}
                        </style>""", unsafe_allow_html=True)
    
    
    
def air_host():
    host_data=[]
    for i in connection.col.find({}, {'_id': 1, 'host': 1}):
        host_data.append(i)
    df_host = pd.DataFrame(host_data)
    
    host_keys = list(df_host.iloc[0, 1].keys())  
    host_keys.remove('host_about')
    # st.table(host_keys)
    
    
    for i in host_keys:
        if i == 'host_response_time':
            df_host['host_response_time'] = df_host['host'].apply(lambda x: x.get('host_response_time', 'Not Specified'))
        else:
            df_host[i] = df_host['host'].apply(lambda x: x.get(i, 'Not Specified') if x and i in x and x[i] != '' else 'Not Specified')
            
    df_host.drop(columns=['host'], inplace=True)
        
    #Converting string labels ('Yes' and 'No') instead of boolean values (True and False)
    df_host['host_is_superhost'] = df_host['host_is_superhost'].map({False: 'No', True: 'Yes'})
    df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map({False: 'No', True: 'Yes'})
    df_host['host_identity_verified'] = df_host['host_identity_verified'].map({False: 'No', True: 'Yes'})
    
    return df_host

def air_address():
    address = []
    for i in connection.col.find({}, {'_id': 1, 'address': 1}):
        address.append(i)

    df_address = pd.DataFrame(address)
    address_keys = list(df_address.iloc[0, 1].keys())
    
    #Extracting nested dicionary to separate dataframe columns
    for i in address_keys:
        if i == 'location':
            df_address['location_type'] = df_address['address'].apply(lambda x: x['location']['type'])
            df_address['longitude'] = df_address['address'].apply(lambda x: x['location']['coordinates'][0])
            df_address['latitude'] = df_address['address'].apply(lambda x: x['location']['coordinates'][1])
            df_address['is_location_exact'] = df_address['address'].apply(lambda x: x['location']['is_location_exact'])
        else:
            df_address[i] = df_address['address'].apply(lambda x: x[i] if x[i] != '' else 'Not Specified')  
    #Dropping column address   
    df_address.drop(columns=['address'], inplace=True)

        #Converting string labels ('Yes' and 'No') instead of boolean values (True and False)
    df_address['is_location_exact'] = df_address['is_location_exact'].map({False: 'No', True: 'Yes'})
    
    return df_address


def air_availability():
    availability = []
    for i in connection.col.find({}, {'_id': 1, 'availability': 1}):
        availability.append(i)

    df_availability = pd.DataFrame(availability)        
    availability_keys = list(df_availability.iloc[0, 1].keys())
    
    # nested dicionary to separate columns
    for i in availability_keys:
        df_availability['availability_30'] = df_availability['availability'].apply(lambda x: x['availability_30'])
        df_availability['availability_60'] = df_availability['availability'].apply(lambda x: x['availability_60'])
        df_availability['availability_90'] = df_availability['availability'].apply(lambda x: x['availability_90'])
        df_availability['availability_365'] = df_availability['availability'].apply(lambda x: x['availability_365'])

    df_availability.drop(columns=['availability'], inplace=True)
    return df_availability   

def air_amenities():
    
    amenities = []
    for i in connection.col.find({}, {'_id': 1, 'amenities': 1}):
        amenities.append(i)
    df_amenities = pd.DataFrame(amenities)       

    return df_amenities

def creating_dataframe():
    df_main = air_main()
    df_host =air_host()
    df_address = air_address()
    df_availability = air_availability()
    df_amenities = air_amenities()
    
    # Merging df_main and df_host
    merged_df = pd.merge(df_main, df_host, on='_id')

    # Merging df_address
    merged_df = pd.merge(merged_df, df_address, on='_id')

    # Merging df_availability
    merged_df = pd.merge(merged_df, df_availability, on='_id')

    # Merging df_amenities
    merged_df = pd.merge(merged_df, df_amenities, on='_id')
    st.write('')
    st.write('')
    st.write("Raw Data",merged_df)

    return merged_df
def data_to_sql():

    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="airbnb_analysis"
        )

        # Create a cursor object
    cursor = mydb.cursor()
    df_data = creating_dataframe()       
    column_names = df_data.columns.tolist()

    data_values = df_data.values
    df_data.replace('Not Specified', None, inplace=True)
    df_data.fillna(0, inplace=True)

    # Specify the column names for insertion
    column_names = [
        '_id', 'listing_url', 'name', 'property_type', 'room_type',
        'bed_type', 'minimum_nights', 'maximum_nights', 'cancellation_policy', 'accommodates',
        'bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price',
        'cleaning_fee', 'extra_people','guests_included','images','review_scores', 
        'host_id', 'host_url', 'host_name','host_location','host_response_time',
        'host_thumbnail_url', 'host_picture_url',    'host_neighbourhood', 'host_response_rate', 'host_is_superhost',
        'host_has_profile_pic', 'host_identity_verified', 'host_listings_count', 'host_total_listings_count','street',
        'suburb','government_area', 'market', 'country', 'country_code', 
        'location_type','longitude', 'latitude', 'is_location_exact', 'availability_30',
        'availability_60', 'availability_90', 'availability_365'
        ]

        


    # Insert data into MySQL table for the specified columns
    insert_query = """
        INSERT INTO airbnb (
            {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 
            {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 
            {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
            {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
            {}, {}, {}, {}, {}, {}, {}, {}  
            
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
            )
    """.format(*column_names)

    # Execute the query for each row in df_data
    for row in df_data[column_names].values:
        cursor.execute(insert_query, tuple(row))

    # Commit the changes
    st.success("Data inserted to Database")    
    mydb.commit()
    mydb.close()

def delete_table():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="airbnb_analysis"
                )
    cursor = mydb.cursor()
    cursor.execute(f"""delete from airbnb;""")
    mydb.commit()
    mydb.close()

streamlit_run()
def bgm():
    
    st.markdown(f""" <style>.stApp {{
                            background: ;
                            background-size: cover}}
                         </style>""", unsafe_allow_html=True)

bgm()

st.markdown(
    """
    <style>
        div[data-testid="stSidebarContent"] {
            background-color: #eddaec; 
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("<h1 style='color: #52aec4;  font-size: 25px;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
# Your Streamlit app content goes here

st.sidebar.header("Menu")

welcome_css = """
    <style>
            .welcome-message {
            font-size: 20px;
            color: white;
            text-align: center;
            padding: 05px;
            background-color: #759bd9 ;
            border-radius:100px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
"""

st.markdown(welcome_css, unsafe_allow_html=True)
 
st.markdown("<div class='welcome-message'>Welcome to Airbnb Analysis!</div>", unsafe_allow_html=True)

with st.sidebar:
    selected = st.selectbox(
        "SELECT AN OPTION",
        ["TRANSFER DATA TO DATABASE","RAW DATA"],
        index=0
        )
  
if selected == "TRANSFER DATA TO DATABASE" :
    with st.spinner("Please wait ..."):
        data_to_sql()
elif selected == "RAW DATA" :
    creating_dataframe()

        
