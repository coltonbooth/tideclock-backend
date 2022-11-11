from typing import Union
import json
from fastapi import FastAPI
from tide_functions import return_stations, get_high_low_prediction
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.2.97",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/find-stations")
def get_stations():
    station_list = return_stations()
    return JSONResponse(content=station_list)

@app.get("/tides/{station}")
def get_tides(station: str):
    tides = get_high_low_prediction(station)
    return JSONResponse(content=tides)