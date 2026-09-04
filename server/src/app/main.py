from fastapi import FastAPI

from app.settings import settings
from app.view import routers


app = FastAPI()
app.include_router(routers)


@app.get("/")
def read_root():
	return {
		"message": "Welcome to the Drop API!",
		"DEBUG": settings.DEBUG,
		"docs": "/docs",
		"redoc": "/redoc",
	}

