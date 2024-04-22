from fastapi import FastAPI , WebSocket, WebSocketDisconnect
import signal

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text(f"Data received: {data}")
    except WebSocketDisconnect:
        await websocket.close()
        print("WebSocket connection closed")
        
