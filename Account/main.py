# In the name of GOD

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


from api.v1 import internal_users_api, external_users_api
from db.db import collections, databases, sess_db
from config.middlewares import InternalSecurityMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    account_db = await sess_db()
    collections["users_collection"] = account_db.database["users_collection"]
    yield
    collections.clear()
    account_db.client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(internal_users_api.router)
app.include_router(external_users_api.router)
app.add_middleware(InternalSecurityMiddleware)


@app.get("/")
def root():
    return JSONResponse({"message": "Hello..."}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    # uvicorn.run("main:app", host="localhost", port=8003, log_level="debug", reload=True)
    uvicorn.run(app, host="localhost", port=8003, log_level="debug")