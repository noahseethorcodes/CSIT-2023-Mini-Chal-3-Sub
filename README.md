# CSIT-2023-Mini-Chal-3-Sub
My submission for the CSIT 2023 Software Engineering Mini Challenge on Backend Development

## Problem Outline
* Provided is a a connection to a NoSQL database containing 2 tables: flights and hotels.
* The goal is to write an application that provides 2 WebAPI endpoints (GET /flights and GET /hotels) that return the cheapest options for the respective item.
* The request body will contain the relevant information such as:
  * Start and End Dates for travel
  * Origin and Destination City
 
## Solution Approach
1. In [database.py](https://github.com/noahseethorcodes/CSIT-2023-Mini-Chal-3-Sub/blob/main/app/database.py), write two functions that handle the respective requests. Functions will follow this general structure:
    1. Connect to the databse via a pymongo client
    2. Make the relevant query
    3. Convert the returned cursor to a dataframe for processing
    4. Format the relevant data and return it
2. In [server.py](https://github.com/noahseethorcodes/CSIT-2023-Mini-Chal-3-Sub/blob/main/app/server.py), write a simple FastAPI application that has the two required endpoints.
    1. Perform basic input validation (e.g. correct date formatting)
    2. Format the data in the given request body
    3. Call the respective [database.py](https://github.com/noahseethorcodes/CSIT-2023-Mini-Chal-3-Sub/blob/main/app/database.py) functions with the given arguments
    4. Return the results
