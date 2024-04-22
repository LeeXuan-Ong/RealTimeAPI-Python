from fastapi import FastAPI , WebSocket, WebSocketDisconnect
import signal
import json

app = FastAPI()

cache_data = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        print(type(json_data))
        print(data)
        
        await websocket.send_text(f"Data received: {data}")
    except WebSocketDisconnect:
        await websocket.close()
        print("WebSocket connection closed")
        
