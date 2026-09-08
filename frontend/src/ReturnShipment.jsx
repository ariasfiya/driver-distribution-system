import {useState, useEffect} from 'react';

function ReturnShipment( {
    activeShipment,
    getVehicles,
    getFirstDriver,
    getActiveShipment
}) {
    const [selectedShipment, setSelectedShipment] = useState("")
    const [message, setMessage] = useState("")



    function selectShipment(event) {
        const id = Number(event.target.value)

        const shipment = activeShipment.find(
            (shipment) => shipment.id_pengiriman === id
        )

        setSelectedShipment(shipment)
    }

    function returnShipment() {
        console.log("Shipment yang akan dikembalikan:", selectedShipment.id_pengiriman)

        const data = {
            "id_pengiriman" : selectedShipment.id_pengiriman
        }

        fetch("http://127.0.0.1:8000/shipment/return", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result =>{
            console.log("Respondari FasAPI:", result)
            setMessage(result.message)
            
            getActiveShipment()
            getVehicles()
            getFirstDriver()
            setSelectedShipment("")
        })      
    }

    useEffect(() => {
        getActiveShipment()
        getVehicles()
        getFirstDriver()
    }, [])

    return(
        <div>
            <h3>Return Shipment</h3>

            <p>Active Shipment</p>
            
            <select onChange={selectShipment}>
                <option>Pilih Kiriman</option>

                {activeShipment.map((shipment) => (
                    <option 
                    key={shipment.id_pengiriman} 
                    value={shipment.id_pengiriman}
                    >
                        {shipment.rute} - {shipment.nama_driver} - {shipment.nomer_polisi}
                    </option>
                ))}
            </select>

            <p>Shipment dipilih: {selectedShipment.rute}</p>
            
            <button onClick={returnShipment}>
                Return Shipment
            </button>

            <p>{message}</p>

        </div>
    )
}

export default ReturnShipment