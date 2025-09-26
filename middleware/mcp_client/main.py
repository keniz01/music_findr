from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.api import router as hello_router

app = FastAPI()

# Allow requests from Vite's dev server
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(hello_router)
