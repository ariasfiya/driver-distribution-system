import {useState, useEffect} from 'react'
import Dashboard from './dashboard'
import Drivers from './driver'
import './App.css'

function App() {
  const namaProject = "Driver Distribution System"
  const versi = 1
  const [page, setPage] = useState("dashboard")
  const [vehicles, setVehicles] = useState([])
  const [drivers, setDrivers] = useState([])
  const [firstDriver, setFirstDriver] = useState(null)
  const [activeShipment, setActiveShipment] = useState([])

  function getVehicles() {
    fetch('http://127.0.0.1:8000/vehicles')
    .then(response => response.json())
    .then(data => {
      console.log("Data vehicles dari FastAPI:", data)
      setVehicles(data)
    })
    .catch(error => {
      console.error("Error mengambil data:", error)
    })
  }

  function getFirstDriver() {
    fetch('http://127.0.0.1:8000/driver/first')
    .then(request => request.json())
    .then(data => {
      console.log("Data first driver dari FastAPI",data)
      setFirstDriver(data)
    })
  }

  function getActiveShipment() {
    fetch("http://127.0.0.1:8000/shipment/on-progress")
    .then(response => response.json())
    .then(data => {
      console.log("Data On Progres Shipment dari API", data)
      setActiveShipment(data)
    })
  }

  function getDrivers() {
        fetch('http://127.0.0.1:8000/drivers')
    .then(response => response.json())
    .then(data => {
      console.log("Data drivers dari FastAPI", data)
      setDrivers(data)
    })
  }

  useEffect(() =>{
    getVehicles()
    getDrivers()
    getFirstDriver()
    getActiveShipment()
  }, [])

  return (
    <div>

    <h1>{namaProject}</h1>
      <p>Sistem ini masih dalam pengambangan v{versi + 0.1}</p>
      <nav>
        <button onClick={() => setPage("dashboard")}>
          Dashboard
        </button>
          <button onClick={() => setPage("driver")}>
          Driver
        </button>
      </nav>
      {page === "dashboard" && (
        <Dashboard 
        vehicles = {vehicles} 
        drivers = {drivers} 
        firstDriver={firstDriver}
        activeShipment={activeShipment}
        getVehicles={getVehicles}
        getDrivers = {getDrivers}
        getFirstDriver={getFirstDriver}
        getActiveShipment={getActiveShipment}
        />
      )}

      {page === "driver" && (
        <Drivers
        drivers={drivers}
        getDrivers={getDrivers}
        />
      )}

    </div>

  )
}

export default App

