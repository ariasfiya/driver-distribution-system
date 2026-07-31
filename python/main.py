from database import (
    connect_db,
    get_first_driver,
    get_active_vehicles,
    dispatch_shipment,
    get_pengiriman_on_progress,
    get_shipment_by_id,
    return_shipment
)

print("=== DRIVER DISTRIBUTION SYSTEM ===")
print("1. Buat Pengiriman")

#cek koneksi database
connection = connect_db()
print("Berhasil terhubung ke PostgreSQL!")

# ==========================================
# CREATE MENU
# ==========================================

print("=" * 30)
print(" Driver Distribution System")
print("=" * 30)

print("1. Create Shipment")
print("2. Return Shipment")
print("3. Exit")

menu = input("\nSelect menu: ")

if menu == "1":
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

elif menu == "2":
    # ==========================================
    # FEATURE: RETURN SHIPMENT
    # ==========================================

    # Display active/on-progress shipments
    on_progress_shipment = get_pengiriman_on_progress(connection)

    if not on_progress_shipment:
        print("No shipments in progress")

    else:
        print("\n=== ON PROGRESS SHIPMENT ===")

        for id_pengiriman,nama_driver, rute, tanggal_keberangkatan in on_progress_shipment:
            
            print(f"{id_pengiriman}. {nama_driver}. {rute}. {tanggal_keberangkatan} ")

        pilih_pengiriman = int(input("\nPilih ID pengiriman: "))
        shipment = get_shipment_by_id(connection, pilih_pengiriman)

        if shipment is None:
            print("Shipment not found")
        else:
            print("Oke")

            return_shipment(
                connection,
                pilih_pengiriman
            )

            print(f"Shipment #{id_pengiriman} to {rute} has been completed.")

            


elif menu == "3":
    print("Goodbye")

else:
    print("Invalid menu")

connection.close()