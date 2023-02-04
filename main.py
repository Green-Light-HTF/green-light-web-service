from fastapi import FastAPI
import uvicorn
from api.api_v1.api import router as api_router

app = FastAPI(
    title="GreenLight",
    description="Green Corridor for every ambulance")

app.include_router(api_router)


@app.get("/ping", include_in_schema=False)
async def ping_server():
    return {"result": "OK"}

print("Service started at http://localhost:{}".format(9000))
print("Checkout openapi document at http://localhost:{}/docs".format(9000))
print("Checkout analytics dashboard at http://localhost:{}/dashboard".format(9000))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
