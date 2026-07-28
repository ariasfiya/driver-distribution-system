from database import (
    connect_db,
    get_first_driver,
    get_active_vehicles,
    dispatch_shipment
)

print("=== DRIVER DISTRIBUTION SYSTEM ===")
print("1. Buat Pengiriman")
print("2. Lihat Pengiriman")
print("3. Keluar")

#cek koneksi database
connection = connect_db()
print("Berhasil terhubung ke PostgreSQL!")

#Ambil driver pertama yang siap
driver = get_first_driver(connection)

if driver is None:
    print("Tidak ada driver yang siap.")
else:
    id_driver, nama, urutan_driver = driver

    print("=== DRIVER TERPILIH ===")
    print(f"ID     : {id_driver}")
    print(f"Nama   : {nama}")
    print(f"Urutan : {urutan_driver}")

    # Ambil semua kendaraan aktif
    vehicles = get_active_vehicles(connection)

    if not vehicles:
        print("Tidak ada kendaraan aktif")
    else:
        print("\n=== KENDARAAN AKTIF ===")

        for id_kendaraan, nopol, jenis, kapasitas in vehicles:
            print(f"{id_kendaraan}. {nopol} ({jenis}, {kapasitas} ton)")

        #input atau pilih kendaraan oleh admin
        pilih_kendaraan = int(input("\nPilih ID kendaraan: "))
        print(f"ID kendaraan yang dipilih: {pilih_kendaraan}")

        #Input rute
        rute = input("Masukkan rute: ").strip().upper()

        #Simpan ke database
        dispatch_shipment(
            connection,
            id_driver,
            pilih_kendaraan,
            rute,
            urutan_driver
        )

        print ("pengiriman berhasil disimpan")
connection.close()