from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from control.routers import company
from annoy import AnnoyIndex
from scipy.spatial.distance import cosine

app = FastAPI(
    title="Companies API", description="This is the API for the companies service."
)

origins = ["*"]
app.include_router(company.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
