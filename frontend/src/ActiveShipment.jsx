function ActiveShipment ({activeShipment, returnShipment}) {
    return (
        <div>
            <p>Sedang dalam perjalann</p>

            {activeShipment.map((shipment) => (
                <div className ="shipment-card" key={shipment.id_pengiriman}>
                    <div className="shipment-header">
                        <p className="shipment-title">
                            Kiriman #{shipment.id_pengiriman}
                        </p>
                        <p>{shipment.status}</p>
                    </div>
                    
                    <div className="shipment-route">
                        <span>Rute</span>
                        <strong>{shipment.rute}</strong>
                    </div>
                    
                    <div className="shipment-detail">
                        <div className="shipment-info">
                            <span>Driver</span>
                            <strong>{shipment.nama_driver}</strong>
                        </div>
                        <div className="shipment-info">
                            <span>Kendaraan</span>
                            <strong>{shipment.nomer_polisi}</strong>
                        </div>
                        <div className="shipment-info">
                            <span>Tgl. Keberangkatan</span>
                            <strong>{shipment.tanggal_keberangkatan}</strong>
                        </div>

                    </div>
                    <div>
                        <button onClick={() => returnShipment(shipment.id_pengiriman)}>
                            Return Shipment
                        </button>
                    </div>
                </div>                
            ))}
        </div>
    )
    
}

export default ActiveShipment