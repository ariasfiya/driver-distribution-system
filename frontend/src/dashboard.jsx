import CreateShipment from "./CreateShipment";
import DriverList from "./driver";
import VehicleList from "./vehicles";
import ReturnShipment from "./ReturnShipment";
import ActiveShipment from "./ActiveShipment";

function Dashboard({
    vehicles,
    drivers,
    firstDriver,
    activeShipment,
    getVehicles,
    getDrivers,
    getFirstDriver,
    getActiveShipment
}) {

    return (
        <div className="dashboard">
            <h2>Dashboard Admin DO</h2>

            {/* Summary card */}
            <div className="summary-cards">

                <div className="summary-card">
                    <span>Kendaraan Siap</span>
                    <strong>{vehicles.length}</strong>
                </div>

                <div className="summary-card">
                    <span>Driver Siap</span>
                    <strong>
                        {drivers.filter(driver =>
                            driver.aktif === true &&
                            driver.status_driver === "SIAP"
                        ).length}
                    </strong>
                </div>

                <div className="summary-card">
                    <span>Kiriman Aktif</span>
                    <strong>{activeShipment.length}</strong>
                </div>
            </div>

            <div className="shipment-section">

                <div className="create-shipment-section">
                    <p>PENGIRIMAN</p>
                    <p>Create Shipment</p>

                    <CreateShipment 
                        vehicles={vehicles}
                        getDrivers={getDrivers}
                        firstDriver={firstDriver}
                        getVehicles = {getVehicles}
                        getFirstDriver={getFirstDriver}
                        getActiveShipment={getActiveShipment}
                    />
                </div>

                <div className="active-shipment-section">
                    <div className="section-header">
                        <h3>Kiriman Aktif</h3>
                        <span>{activeShipment.length} kiriman</span>
                    </div>

                    <ReturnShipment
                        driver={drivers}
                        getVehicles={getVehicles}
                        getDrivers={getDrivers}
                        getFirstDriver={getFirstDriver}
                        activeShipment={activeShipment}
                        getActiveShipment={getActiveShipment}
                    />
                </div>
            </div>
        </div>
    )
}

export default Dashboard