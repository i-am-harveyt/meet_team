"""main"""

from fastapi import FastAPI

from .api.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    """This is the default route to the root"""
    return {"message": "Hello World"}
