from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from database import (
    connect_db,
    get_active_vehicles,
    get_first_driver,
    dispatch_shipment,
    get_pengiriman_on_progress,
    return_shipment
)

app = FastAPI()

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
            "message": "Shipment created succesfully"
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

@app.get("/vehicles")
def get_vehicles():
    connection = connect_db()

    try: 
        vehicles = get_active_vehicles(connection)
        return vehicles

    finally:
        connection.close()

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
            "massage":"Shipment has been completed"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        connection.close()
