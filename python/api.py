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
from driver import (
    add_driver,
    edit_urutan,
    update_driver_status_out,
    update_driver_status_in
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

# Tambahkan driver
class AddNewDriverRequest(BaseModel):
    nama : str

@app.post("/add_driver")
def add_new_driver(request: AddNewDriverRequest):

    connection = connect_db()

    try:
        add_driver(connection,request.nama)
        return{
            "message": "Add Driver successfully"
        }

    finally:
        connection.close()

# endpoint untuk edit urutan driver
class EditUrutanDriverRequest(BaseModel):
    urutan_semula : int
    urutan_edit : int
    id_driver : int

@app.post("/edit_urutan_driver")
def edit_urutan_driver(request: EditUrutanDriverRequest):

    connection = connect_db()

    try:
        edit_urutan(
            connection,
            request.urutan_semula,
            request.urutan_edit,
            request.id_driver
        )
        return{
            "message": "Driver order updated successfully"
        }

    finally:
        connection.close()

# endpoin edit status driver out
class EditStatusDriverOut(BaseModel):
    urutan : int
    status : str
    id_driver : int

@app.post("/edit_status_driver_out")
def edit_status_driver_out(request: EditStatusDriverOut):

    connection = connect_db()

    try:
        update_driver_status_out(
            connection,
            request.urutan,
            request.status,
            request.id_driver
        )
        return{
            "message": "Driver status updated successfully"
        }

    finally:
        connection.close()

# endpoin edit status driver in
class EditStatusDriverIn(BaseModel):
    status : str
    id_driver : int

@app.post("/edit_status_driver_in")
def edit_status_driver_in(request: EditStatusDriverIn):

    connection = connect_db()

    try:
        update_driver_status_in(
            connection,
            request.id_driver,
            request.status
        )

        return{
            "message": "Driver status updated successfully"
        }

    finally:
        connection.close()