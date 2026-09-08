from database import (
    connect_db,
    get_first_driver,
    get_active_vehicles,
    dispatch_shipment,
    get_pengiriman_on_progress,
    get_shipment_by_id,
    return_shipment,
    reset_system_data
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
print("3. reset")
print("4. Exit")

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

            while True:
                try: 

                    #input atau pilih kendaraan oleh admin
                    pilih_kendaraan = int(input("\nPilih ID kendaraan: "))

                    ## Validate user input against available options
                    truck = next (
                        (v for v in vehicles if v[0]==pilih_kendaraan),
                        None
                    )

                    if truck is None:
                        print("Truck not found")
                        continue
                    
                    break

                except ValueError:
                    print("Input must be e nummber")

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

        while True:
            try : 
                pilih_pengiriman = int(input("\nPilih ID pengiriman: "))

                shipment = get_shipment_by_id(connection, pilih_pengiriman)

                if shipment is None:
                    print("Shipment not found")
                    continue

                break
            
            except ValueError:
                print("Input must be e nummber")

        print("Oke")

        try:
            return_shipment(
                connection,
                pilih_pengiriman
            )

            print(f"Shipment #{pilih_pengiriman} to {shipment["rute"]} has been completed.")

        except ValueError as e:
            print(e)

        except Exception as e:
            print(f"Unexpected error: {e}")

            
elif menu == "3":
    def reset_data(connection):
        connection = connect_db()

        try:
            reset_system_data(connection)
            print("System data has been reset.")

        finally:
            connection.close()

    reset_data(connection)



elif menu == "4":
    print("Goodbye")

else:
    print("Invalid menu")

connection.close()