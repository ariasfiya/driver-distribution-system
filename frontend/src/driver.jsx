function DriverList({drivers}){
    return (
        <div>
            <h1>Dafter Driver</h1>

            {drivers.map(driver => (
                <div key={driver.id_driver}>
                    <p>{driver.urutan +"-"+ driver.nama +"-"+ driver.status_driver}</p>
                </div>
            ))}
        </div>
    )
}

export default DriverList