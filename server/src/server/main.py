from fastapi import FastAPI

from server.settings import settings
from server.view import routers


app = FastAPI()
app.include_router(routers)


@app.get("/")
def read_root():
	return {
		"message": "Welcome to the Personal Bug Tracker API!",
		"DEBUG": settings.DEBUG,
		"docs": "/docs",
		"redoc": "/redoc",
	}

