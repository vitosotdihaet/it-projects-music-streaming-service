from depends import lifespan
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from api.routers import user_activity
from configs.environment import get_environment_variables


print(f'settings = {get_environment_variables()}')


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_activity.router)
