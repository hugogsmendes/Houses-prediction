from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

limiter = Limiter(key_func = get_remote_address)
app = FastAPI(
    title = "Houses Predicition",
    version = "1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "https://houses-prediction.streamlit.app"
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes.user_routes import user_router
from api.routes.adm_routes import adm_router
from api.routes.model_routes import model_route

app.include_router(user_router)
app.include_router(adm_router)
app.include_router(model_route)