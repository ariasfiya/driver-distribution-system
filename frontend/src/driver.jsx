import { useState } from 'react'


function DriverList({drivers}){
    // const [drivers, SetDrivers] = useState("")
    return (
        <div>
            <h1>Driver</h1>
            {drivers.map(driver => (
                <div key={driver.id_driver}>
                    <p>{driver.urutan +"-"+ driver.nama +"-"+ driver.status_driver}</p>
                </div>
            ))}
        </div>          
    )
}

function AddDriver({getDrivers}) {

    const [namaDriver, setNamaDriver] = useState("")
    const data = {
        "nama" : namaDriver
    }
    const [message, setMessage] = useState("")

    function ubahNama(event) {
        setNamaDriver(event.target.value)
    }

    function newDriver() {
        fetch("http://127.0.0.1:8000/add_driver", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
        })

        .then(pesan => pesan.json())
        .then(result => {
            console.log("Response dari FasAPI:",result)
            setMessage(result.message)
            console.log(result.message)
            
            getDrivers()
            setNamaDriver("")

            setTimeout(() => {
                setMessage("")
            }, 3000);
        })
    }


    return (
            <div>
                <h1>Add Driver</h1>
                <input
                    type ="text"
                    placeholder="Nama Driver"
                    value={namaDriver}
                    onChange={ubahNama}
                />

                <button onClick={newDriver}>
                    Add Driver
                </button>
                <p>{message}</p>

            </div>
        )
}


function Drivers({
    drivers,
    getDrivers
}){
    return (
        <div>
            <AddDriver getDrivers={getDrivers}/>
            <DriverList drivers={drivers}/>
        </div>

    )
}

export default Drivers