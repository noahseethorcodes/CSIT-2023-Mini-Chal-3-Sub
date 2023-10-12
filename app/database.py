from pymongo import MongoClient
from datetime import datetime
import pandas as pd

DB_URL = 'mongodb+srv://userReadOnly:7ZT817O8ejDfhnBM@minichallenge.q4nve1r.mongodb.net/'

def get_cheapest_return_flights(departureDate, returnDate, destination):
    visiting = destination.title()
    home = 'Singapore'

    #Querying the db
    client = MongoClient(DB_URL)
    flight_colls = client.get_database('minichallenge').get_collection('flights')
    
    send_flight_query = {'srccity': home, 'destcity': visiting, 'date': departureDate}
    send_flight_proj = {"_id": 0, "destcity": 1, "date": 1, "airline": 1, "price": 1}

    return_flight_query = {'srccity': visiting, 'destcity': home, 'date': returnDate}
    return_flight_proj ={"_id": 0, "date": 1, "airline": 1, "price": 1}

    send_flight_cursor = flight_colls.find(send_flight_query, send_flight_proj).sort('price', 1).limit(1) 
    return_flight_cursor = flight_colls.find(return_flight_query, return_flight_proj).sort('price', 1).limit(1) 
    

    #Checking if valid results were returned
    flights_exist = True
    try:
        send_flight_details = send_flight_cursor[0]
        return_flight_details = return_flight_cursor[0]
    except IndexError:
        flights_exist = False

    #Formatting the return value
    if flights_exist:
        response = {}
        response ['City'] = send_flight_details['destcity']
        response ['Departure Date'] = send_flight_details['date'].strftime('%Y-%m-%d')
        response ['Departure Airline'] = send_flight_details['airline']
        response ['Departure Price'] = send_flight_details['price']
        response ['Return Date'] = return_flight_details['date'].strftime('%Y-%m-%d')
        response ['Return Airline'] = return_flight_details['airline']
        response ['Return Price'] = return_flight_details['price']
        client.close()
        return([response])
    else: 
        client.close()
        return([])
    
def get_cheapest_hotel(checkInDate, checkOutDate, destination):
    num_days = (checkOutDate - checkInDate).days + 1
    destination = destination.title()
    print(destination)
    #Querying the db
    client = MongoClient(DB_URL)
    hotel_colls = client.get_database('minichallenge').get_collection('hotels')
    
    hotel_query = {'city': destination, 'date': {'$gte': checkInDate, '$lte': checkOutDate}}
    hotel_proj = {'_id': 0, 'hotelName': 1, 'price': 1}
    cursor = hotel_colls.find(hotel_query, hotel_proj).sort('hotelName', 1)

    index = 0
    hotel_names = ['']
    hotel_prices = [0]
    hotel_days = [0]
    curHotel = ''
    for doc in cursor:
        if not curHotel:
            curHotel = doc['hotelName']
            hotel_names[index] = doc['hotelName']
            hotel_prices[index] = doc['price']
            hotel_days[index] = 1
        elif curHotel != doc['hotelName']:
            curHotel = doc['hotelName']
            hotel_names.append(doc['hotelName'])
            index += 1
            hotel_prices.append(doc['price'])
            hotel_days.append(1)
        else:
            hotel_prices[index] += doc['price']
            hotel_days[index] += 1
    client.close()
    hotel_data = {'Name': hotel_names,
                  'Price': hotel_prices,
                  'Days': hotel_days}
    df = pd.DataFrame(hotel_data)
    cheapest_hotel_df = df.loc[(df['Days'] == num_days)].sort_values(by=['Price'])

    #Formatting the return value
    response = {}
    if not cheapest_hotel_df.empty:
        cheapest_hotel_df = cheapest_hotel_df.iloc[0]
        response ['City'] = destination
        response ['Check In Date'] = checkInDate
        response ['Check Out Date'] = checkOutDate
        response ['Hotel'] = cheapest_hotel_df['Name']
        response ['Price'] = cheapest_hotel_df['Price'].item()
        return([response])
    else:
        return([])