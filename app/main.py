from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import user_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message":"Auth System running"}

app.include_router(user_routes.router)

