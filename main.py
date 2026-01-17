from fastapi import FastAPI

app = FastAPI()


from api.routes.user_routes import user_router
from api.routes.adm_routes import adm_router

app.include_router(user_router)
app.include_router(adm_router)