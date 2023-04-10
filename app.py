from fastapi import FastAPI, Depends
from sqlalchemy.orm import session
from database.schemas import *
from database.engine import *
from routes import auth_routes, organisation_routes, client_routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(auth_routes.router, prefix="/Auth", tags=['Auth'])
app.include_router(organisation_routes.router, prefix="/Organisation", tags=['Organisation'])
app.include_router(client_routes.router, prefix="/Client", tags=["Client"])

Base.metadata.create_all(bind=engine)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def start():
    return "Api work))"