from fastapi import FastAPI , WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

cache_data = []
timeline= {"date":0, "time":[]}
@app.get("/data")
def read_data():
    return {"items": cache_data}
  
@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
  return templates.TemplateResponse(request=request, name="index.html", context={"items": cache_data, "request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        if(len(json_data) > 0):
          sum_prices =  sum([float(data['price']) for data in json_data])
          average_prices = sum_prices/len(json_data)
          min_price=0 
          max_price= 0
          quantity =  sum([int(data['quantity']) for data in json_data])
          for data in json_data:
            if(max_price == 0 and min_price == 0):
              max_price = float(data['price'])
              min_price = float(data['price'])
            if(float(data['price'])>max_price):
              max_price = float(data['price'])
            if(float(data['price'])<min_price):
              min_price = float(data['price'])
            print(f"Data received: {data}")
        
        record_datetime = datetime.datetime.strptime(json_data[0]['datetime'], '%Y-%m-%d %H:%M:%S:%f')
        cache_data.append({"date": record_datetime.date(), "time": "{:d}:{:02d}:{:02d}".format(record_datetime.hour,record_datetime.minute,record_datetime.second), "datetime":json_data[0]['datetime']  ,"quantity_total": quantity, "average_price": "{:.2f}".format(average_prices), "min_price": min_price, "max_price": max_price})
        await websocket.send_text(f"Data received: {data}")
    except WebSocketDisconnect:
        await websocket.close()
        print("WebSocket connection closed")
        
