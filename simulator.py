import pandas as pd
import json
import asyncio
import websockets
import datetime
import time

async def send_message(message):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        # print(f">>> {message}")
        
        response = await websocket.recv()
        # print(f"<<< {response}")
        if(response != ""):
            print("Data sent successfully")
        

df = pd.read_csv('AAPL.csv')
processed_datetime = df["datetime"]

count = 0
# last_datetime = datetime.datetime(2020,7,1,4,0,0,0)
cache_data = []
for index, row in df.iterrows():
    count += 1
    timestamp = datetime.datetime.strptime(row["datetime"], '%Y-%m-%d %H:%M:%S:%f')
    price = row["price"]
    quantity = row["quantity"]
    venue = row["venue"]
    print(f"Timestamp: {timestamp}, Price: {price}, Quantity: {quantity}, Venue: {venue}")
    # if(type(last_datetime) == str):
    #     last_datetime = datetime.datetime.strptime(last_datetime, '%Y-%m-%d %H:%M:%S:%f')
    
    # time_diff = (timestamp -current__datetime).total_seconds()
    # print(time_diff)
    
    next_datetime = datetime.datetime.strptime(df.loc[index+1, "datetime"],'%Y-%m-%d %H:%M:%S:%f')
    
    cache_data.append({"timestamp":timestamp.strftime('%Y-%m-%d %H:%M:%S:%f'), "price":price, "quantity":quantity, "venue":venue})

    if(next_datetime == timestamp):
        print("Date time is same as previous data")
        time.sleep(1)
        continue
    else:
        print("Sending data to server")
        # send data here
        json_data = json.dumps(cache_data)
        print(json_data)
        asyncio.run(send_message(json_data))
        # time.sleep(time_diff)
        time.sleep(1)
        cache_data = []
    

