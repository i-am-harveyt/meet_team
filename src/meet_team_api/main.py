"""main"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from .api.routes import router
from .api.routes import router, routes_message

app = FastAPI()
app.include_router(router)
app.include_router(routes_message.message_router)

origins = ["http://localhost",
           "http://localhost:5173", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """This is the default route to the root"""
    return {"message": "Hello World"}
