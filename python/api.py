from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import (
    connect_db,
    get_drivers,
    get_active_vehicles,
    get_first_driver,
    dispatch_shipment,
    get_pengiriman_on_progress,
    return_shipment
)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Mengizinkan frontend
    allow_credentials=True,
    allow_methods=["*"],              # Mengizinkan semua method (GET, POST, PUT, DELETE)
    allow_headers=["*"],              # Mengizinkan semua header
)

class CreateShipmentRequest(BaseModel):
    pilih_kendaraan : int
    rute : str

@app.post("/shipments")
def create_shipment(request: CreateShipmentRequest):
    connection = connect_db()

    try:
        dispatch_shipment(
            connection,
            request.pilih_kendaraan,
            request.rute
        )
        return{
            "message": "Shipment created successfully"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        connection.close()


@app.get("/")
def home():
    return {
        "message": "Driver Distribuiton"
    }


@app.get("/driver/first")
def driver_first():
    connection = connect_db()

    try:
        driver_first = get_first_driver(connection)
        return driver_first
    
    finally:
        connection.close()

@app.get("/vehicles")
def vehicles_active():

    connection = connect_db()

    try:
        vehicles_active = get_active_vehicles(connection)
        return vehicles_active

    finally:
        connection.close()

#return shipment
@app.get("/shipment/on-progress")
def pengiriman_on_progress():

    connection = connect_db()

    try:
        pengiriman_on_progress = get_pengiriman_on_progress(connection)

        return pengiriman_on_progress

    finally:
        connection.close()

class ReturnShipmentRequest(BaseModel):
    id_pengiriman: int

@app.post("/shipment/return")
def return_shipment_endpoint(request: ReturnShipmentRequest):
    connection = connect_db()

    try:
        return_shipment(
            connection,
            request.id_pengiriman
        )

        return {
            "message":"Shipment has been completed"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        connection.close()

@app.get("/drivers")
def get_all_drivers():

    connection = connect_db()

    try:
        all_drivers = get_drivers(connection)
        return all_drivers

    finally:
        connection.close()