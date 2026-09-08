import {useEffect, useState} from 'react'

function CreateShipment({ 
    vehicles,
    firstDriver,
    getVehicles,
    getFirstDriver,
    getActiveShipment
}) {
    const [selectedVehicle, setSelectedVehicle] = useState([])
    const [rute, setRute] = useState("")
    const [message, setMessage] = useState("")

    function pilihKendaraan(event) {
        const id = Number(event.target.value)

        const chooseVahicle = vehicles.find(
            (vehicle) =>vehicle.id_kendaraan === id
        )

        setSelectedVehicle(chooseVahicle)
    }
    
    function ubahRute(event) {
        setRute(event.target.value)
    }

    function buatShipment(){
        const data = {
            "pilih_kendaraan" : selectedVehicle.id_kendaraan,
            "rute" : rute
        }

        fetch("http://127.0.0.1:8000/shipments", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("Response dari FasAPI:",result)
            setMessage(result.message)
            
            getVehicles()
            getFirstDriver()
            getActiveShipment()
            setRute("")
            setSelectedVehicle([])
        })
    }


    return (
        <div>
            <h3>CREATE SHIPMENT</h3>

            <p>Driver 1 : {firstDriver?.nama}</p>

            <select onChange={pilihKendaraan}>
                <option>Pilih Kendaraan</option>

                {vehicles.map((vehicle) => (
                    <option key={vehicle.id_kendaraan} value={vehicle.id_kendaraan}>
                        {vehicle.nomer_polisi} - {vehicle.jenis} - {vehicle.kapasitas_ton} ton
                    </option>
                ))}

            </select>

            <p>Kendaraan dipilih: {selectedVehicle.nomer_polisi}</p>

            <input
                type ="text"
                placeholder="Masukkan rute"
                value={rute}
                onChange={ubahRute}
            />
            <p>Rute: {rute}</p>

            <button onClick={buatShipment}>
                Buat Shipment
            </button>

            <p>{message}</p>
        </div>

    )
}

export default CreateShipment
