import { useState, useEffect } from 'react'




function DriverList({ drivers, onEdit}) {
    return (
        <section className="driver-list">
            <div className="driver-list-header">
                <div>
                    <h2>Daftar Driver</h2>
                    <p>Kelola driver dan urutan antrean.</p>
                </div>

                <span className="driver-count">
                    {drivers.length} Driver
                </span>
            </div>

            <div className="driver-table">
                <div className="driver-row driver-table-header">
                    <span>Urutan</span>
                    <span>Nama Driver</span>
                    <span>Status</span>
                    <span>Aksi</span>
                </div>

                {drivers.map((driver) => (
                    <div
                        className="driver-row"
                        key={driver.id_driver}
                    >
                        <div className="driver-order">
                            {driver.urutan ?? "—"}
                        </div>

                        <div className="driver-name">
                            {driver.nama}
                        </div>

                        <div>
                            <span
                                className={`driver-status status-${(
                                    driver.status_driver ?? ""
                                ).toLowerCase().replaceAll("_", "-")}`}
                            >
                                {driver.status_driver}
                            </span>
                        </div>

                        <div>
                            <button
                                className="driver-edit-button"
                                type="button"
                                onClick={() => onEdit(driver)}
                            >
                                Edit
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </section>
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

function EditDriver({
    selectedDriver,
    namaDriver,
    setNamaDriver,
    onClose,
    getDrivers,
    getFirstDriver
}) {
    const [urutanDraft, setUrutanDraft] = useState("")
    const [statusDraft, setStatusDraft] = useState("")
    const [aktifDraft, setAktifDraft] = useState(false)

    // menentukan tampilan form edit driver apa yang di sembunyikan dan saat kondisi seperti apa
    const driverLuarKota = selectedDriver?.status_driver === "LUAR_KOTA"
    const driverAktif = selectedDriver?.aktif
    const drafSiap = statusDraft === "SIAP"

    const bolehEditStatus = aktifDraft && !driverLuarKota && driverAktif
    const bolehEditUrutan = aktifDraft && !driverLuarKota && driverAktif && drafSiap

    const bolehEditAktif = !driverLuarKota

    useEffect(() => {
    if (!selectedDriver) {
        setUrutanDraft("")
        setStatusDraft("")
        setAktifDraft(false)
        setNamaDriver("")
        return
    }

    setNamaDriver(selectedDriver.nama ?? "")
    setUrutanDraft(selectedDriver.urutan ?? "")
    setStatusDraft(selectedDriver.status_driver ?? "")
    setAktifDraft(selectedDriver.aktif ?? false)
}, [selectedDriver, setNamaDriver])

    const namaBerubah =
        namaDriver !== (selectedDriver?.nama ?? "")

    const urutanBerubah =
        selectedDriver != null &&
        (
            urutanDraft === ""
                ? selectedDriver.urutan != null
                : Number(urutanDraft) !== selectedDriver.urutan
        )

    const statusBerubah =
        statusDraft !== (selectedDriver?.status_driver ?? "")

    const aktifBerubah =
        aktifDraft !== selectedDriver?.aktif

    // mendeteksi minimal ada 1 perubahan
    // misal nama berubah maka adaPerubahan bernilai true
    const adaPerubahan =
        namaBerubah ||
        (bolehEditUrutan && urutanBerubah) ||
        (bolehEditStatus && statusBerubah) ||
        (bolehEditAktif && aktifBerubah)

    const perubahan = {}

    // 1. Perubahan nama
    if (namaBerubah) {
        perubahan.nama = namaDriver.trim()
    }

    // 2. Perubahan status aktif
    if (bolehEditAktif && aktifBerubah) {
        perubahan.aktif = aktifDraft
    }

    // 3. Perubahan urutan dan status driver
    // Hanya dikirim jika status aktif tidak berubah
    // dan driver tetap aktif.
    else if (aktifDraft) {
        if (bolehEditUrutan && urutanBerubah && urutanDraft !== "") {
            perubahan.urutan = Number(urutanDraft)
        }

        if (bolehEditStatus && statusBerubah) {
            perubahan.status_driver = statusDraft
        }
    }

    async function handleSave(event) {
        event.preventDefault()

        // Pastikan ada driver yang sedang diedit
        if (!selectedDriver) return

        // Jangan kirim request jika tidak ada perubahan
        if (!adaPerubahan) return

        try {
            const response = await fetch("http://127.0.0.1:8000/edit_driver", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id_driver: selectedDriver.id_driver,
                    perubahan: perubahan
                })
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.detail || "Gagal mengedit driver")
            }

            // Ambil ulang data driver dari database
            await getDrivers()
            await getFirstDriver()

            // Tutup form edit
            onClose(null)

            alert(data.message)

        } catch (error) {
            console.error("Error edit driver:", error)
            alert(error.message)
        }
    }


    return (
        <div>
            {selectedDriver && (
                <div className="edit-modal-backdrop">
                    <section className="edit-modal">
                        <div className="edit-modal-header">
                            <div>
                                <h2>Edit Driver</h2>
                                <p>Perbarui informasi driver.</p>
                            </div>

                            <button
                                type="button"
                                onClick={() => onClose(null)}
                            >
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleSave}>
                            <div className="edit-form-group">
                                <label htmlFor="nama-driver">Nama Driver</label>
                                <input
                                    id="nama-driver"
                                    type="text"
                                    value={namaDriver}
                                    onChange={(event) => setNamaDriver(event.target.value)}
                                />
                            </div>
                            
                            {bolehEditUrutan && (
                                <div className="edit-form-group">
                                    <label htmlFor="urutan-driver">Urutan Antrean</label>
                                    <input
                                        id="urutan-driver"
                                        type="number"
                                        value={urutanDraft}
                                        onChange={(event) => setUrutanDraft(event.target.value)}
                                    />
                                    <small>Pengaturan urutan dilakukan melalui operasi antrean.</small>
                                </div>
                            )}

                            {bolehEditStatus && (
                                <div className="edit-form-group">
                                    <label htmlFor="status-driver">Status Driver</label>
                                    <select
                                        id="status-driver"
                                        value={statusDraft}
                                        onChange={(event) => setStatusDraft(event.target.value)}
                                    >
                                        <option value="SIAP">SIAP</option>
                                        <option value="IZIN">IZIN</option>
                                        <option value="SAKIT">SAKIT</option>
                                        <option value="BERTUGAS">BERTUGAS</option>
                                    </select>
                                    <small>Perubahan status mengikuti aturan antrean.</small>
                                </div>
                            )}

                            {bolehEditAktif && (
                                <div className="edit-form-group">
                                    <label htmlFor="aktif-driver">Driver Aktif</label>
                                    <input
                                        id="aktif-driver"
                                        type="checkbox"
                                        checked={aktifDraft}
                                        onChange={(event) => setAktifDraft(event.target.checked)}
                                    />
                                </div>
                            )}

                            <div className="edit-form-actions">
                                <button
                                    type="button"
                                    onClick={() => onClose(null)}
                                >
                                    Batal
                                </button>

                                <button type="submit" disabled={!adaPerubahan}>
                                    Simpan Perubahan
                                </button>
                            </div>
                        </form>
                    </section>
                </div>
            )}
        </div>
    )
}

function Drivers({
    drivers,
    getDrivers,
    getFirstDriver
}){
    const [selectedDriver, setSelectedDriver] = useState(null)
    const [namaDriver, setNamaDriver] = useState("")

    return (
        <div>
            <AddDriver getDrivers={getDrivers}/>
            <DriverList
                drivers={drivers}
                onEdit={(driver) =>{
                    setSelectedDriver(driver)
                    setNamaDriver(driver.nama)
                }}
            />
            <EditDriver
                onClose={setSelectedDriver}
                selectedDriver={selectedDriver}
                setNamaDriver={setNamaDriver}
                namaDriver={namaDriver}
                getDrivers={getDrivers}
                getFirstDriver={getFirstDriver}
            />
        </div>

    )
}

export default Drivers