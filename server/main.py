from fastapi import FastAPI
from models import setup
from views.users import usersrouter
from views.products import productsrouter
from views.review import reviewrouter
from views.payments import paymentsrouter
from fastapi.middleware.cors import CORSMiddleware
from database.settings import engine

from env_config import Config

app = FastAPI()

# Allowed origins: support custom ALLOWED_ORIGINS env var, Vercel deployments, and localhost
raw_origins = Config.ALLOWED_ORIGINS
if raw_origins:
    origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://dropp-ten.vercel.app/",
        "dropp-ten.vercel.app/",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:\d+|https://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usersrouter)
app.include_router(productsrouter)
app.include_router(reviewrouter)
app.include_router(paymentsrouter)

setup.Base.metadata.create_all(bind=engine)
