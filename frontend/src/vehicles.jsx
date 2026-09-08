function VehicleList({vehicles}) {
  return (
    <div>
      <h2>Daftar Kendaraan</h2>

      {vehicles.map(vehicle => (
        <div key={vehicle.id_kendaraan}>
          <p>{vehicle.nomer_polisi +"-"+ vehicle.jenis +"-"+ vehicle.status_kendaraan}</p>
          <hr />
        </div>
      ))}
    </div>
  )
}

export default VehicleList