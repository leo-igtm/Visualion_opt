import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(  
    title="Visualion API",
)


database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/visualion_opt")

@app.get("/")
async def root():
    return {"message": "Welcome to the Visualion API!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)