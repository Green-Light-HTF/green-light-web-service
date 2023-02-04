from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from starlette.websockets import WebSocket, WebSocketDisconnect
from api.api_v1.api import router as api_router
from src.realtime_data_broadcast import RealTimeDataBroadcast
import uvicorn

app = FastAPI()

ambulance_on_wheel = []


@app.get("/")
async def get():
    return "{'result': OK}"


notifier = RealTimeDataBroadcast()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    await notifier.push(f"! Push notification: {message} !")


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)


app.include_router(api_router, tags=['None'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@api_router.get('/')
def get_notes():
    return "return a list of note items"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10001)
