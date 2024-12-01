from fastapi import FastAPI
from app.routers import app_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(app_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.__main__:app", reload=True)
