from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def hello():
    return {"answer":"Hola Mundo"}