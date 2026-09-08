import CreateShipment from "./CreateShipment";
import DriverList from "./driver";
import VehicleList from "./vehicles";
import ReturnShipment from "./ReturnShipment";

function Dashboard({
    vehicles,
    drivers,
    firstDriver,
    activeShipment,
    getVehicles,
    getFirstDriver,
    getActiveShipment
}) {

    return (
        <div>
            <h2>Dashboard Admin DO</h2>

            <p>KENDARAAN SIAP</p>
            <p>Jumlah Kendaraan: {vehicles.length}</p>
            <VehicleList vehicles={vehicles}/>
            
            <p>DRIVER SIAP</p>
            <p>Jumlah Driver: {drivers.length}</p>
            <DriverList drivers= {drivers}/>

            <p>PENGIRIMAN</p>
            <p>Create Shipment</p>
            <CreateShipment 
                vehicles={vehicles} 
                firstDriver={firstDriver} 
                getVehicles = {getVehicles}
                getFirstDriver={getFirstDriver}
                getActiveShipment={getActiveShipment}
            />
            
            <p>Return Shipment</p>
            <ReturnShipment
                getVehicles={getVehicles}
                getFirstDriver={getFirstDriver}
                activeShipment={activeShipment}
                getActiveShipment={getActiveShipment}
            />
        </div>
    )
}

export default Dashboard