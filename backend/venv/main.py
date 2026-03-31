from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Mobiliza-Plus": "Backend Ativo"}