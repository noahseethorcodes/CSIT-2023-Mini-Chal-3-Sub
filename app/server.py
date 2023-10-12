from fastapi import FastAPI, HTTPException
from datetime import datetime
from .database import get_cheapest_return_flights, get_cheapest_hotel

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400,  detail=message)

@app.get("/")
def read_root():
    ret_str = [
        "Hi Mighty Saver Rabbit! The API is ready for you and your friends to use! " 
        "Use /flight or /hotel to access what you need!"
    ]
    return (ret_str)

@app.get("/flight")
def get_flights(departureDate: str, returnDate: str, destination: str):
    #Preparing the given arguments
    #Date Validation
    try: 
        departureDate = datetime.strptime(departureDate, '%Y-%m-%d')
        returnDate = datetime.strptime(returnDate, '%Y-%m-%d')
    except ValueError:
        raise_bad_request("Date in incorrect format. Please use YYYY-MM-DD.")
    
    return (get_cheapest_return_flights(departureDate=departureDate, 
                                        returnDate=returnDate, 
                                        destination=destination))

@app.get("/hotel")
def get_hotels(checkInDate: str, checkOutDate: str, destination: str):
    #Preparing the given arguments
    #Date Validation
    try: 
        checkInDate = datetime.strptime(checkInDate, '%Y-%m-%d')
        checkOutDate = datetime.strptime(checkOutDate, '%Y-%m-%d')
    except ValueError:
        raise_bad_request("Date in incorrect format. Please use YYYY-MM-DD.")
    return (get_cheapest_hotel(checkInDate=checkInDate, 
                               checkOutDate=checkOutDate, 
                               destination=destination))