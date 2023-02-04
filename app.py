from fastapi import FastAPI, APIRouter
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.realtime_data_broadcast import RealTimeDataBroadcast

app = FastAPI()

router = APIRouter()



@app.get("/")
async def get():
    return "{'result': OK}"

@router.get('/')
def get_notes():
    return "return a list of note items"


@router.post('/', status_code=201)
def create_note():
    return "create note item"


@router.patch('/{noteId}')
def update_note(noteId: str):
    return f"update note item with id {noteId}"


@router.get('/{noteId}')
def get_note(noteId: str):
    return f"get note item with id {noteId}"


@router.delete('/{noteId}')
def delete_note(noteId: str):
    return f"delete note item with id {noteId}"


app.include_router(router, tags=['Notes'], prefix='/api/notes')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

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
