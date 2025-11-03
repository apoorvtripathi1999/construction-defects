from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def root():
    return("Hello World")