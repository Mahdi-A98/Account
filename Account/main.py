@asynccontextmanager
async def lifespan(app: FastAPI):
    account_db = await sess_db()
    collections["users_collection"] = account_db.database["users_collection"]
    yield
    collections.clear()
    account_db.client.close()
