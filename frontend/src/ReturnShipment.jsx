import {useState, useEffect} from 'react';
import ActiveShipment from './ActiveShipment';

function ReturnShipment( {
    driver,
    activeShipment,
    getVehicles,
    getDrivers,
    getFirstDriver,
    getActiveShipment
}) {
   
    const [message, setMessage] = useState("")

    function returnShipment(id_pengiriman) {

        fetch("http://127.0.0.1:8000/shipment/return", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({id_pengiriman})
        })
        .then(response => response.json())
        .then(result =>{
            console.log("Respondari FasAPI:", result)
            setMessage(result.message)

            setTimeout(() => {
                setMessage("")
            }, 3000);
            
            getActiveShipment()
            getVehicles()
            getDrivers()
            getFirstDriver()
        })      
    }

    // useEffect(() => {
    //     getActiveShipment()
    //     getVehicles()
    //     getDrivers()
    //     getFirstDriver()
    // }, [])

    return(
        <div>

            <p>{message}</p>
            
            <ActiveShipment 
                activeShipment={activeShipment}
                returnShipment={returnShipment}
            />
        </div>

        
    )
}

export default ReturnShipment