from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Visualion API",
    docs="/api/docs",
    openapi_url="/api/openapi.json",

) 

@app.get("/api/health")
async def health_check():
    return {"status": "Front end and backend successfully connected"}


if __name__ == "__main__":
    uvicorn.run("api.index:app", host="127.0.0.1", port=5328,reload=True)
