import uvicorn
from fastapi import FastAPI
import os
from functions import colector, ruta_local

app = FastAPI()


@app.get("/")
async def colectar() -> None:
    colector(ruta_local)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)