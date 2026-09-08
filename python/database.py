import psycopg
from psycopg.rows import dict_row

def connect_db():
    connection = psycopg.connect(
        host="localhost",
        port="5432",
        dbname="driver_distribution",
        user="postgres",
        password="postgres"
    )
    return connection

def get_drivers(connection):
    query = """
        SELECT *
        FROM driver
        ORDER BY urutan;
    """
    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(query)
        drivers = cursor.fetchall()

        return drivers

def get_first_driver(connection):
    cursor = connection.cursor(row_factory=dict_row)

    cursor.execute("""
        SELECT
            id_driver,
            nama,
            urutan
        FROM driver
        WHERE aktif = TRUE
          AND status_driver ='SIAP'
        ORDER BY urutan
        LIMIT 1;
    """)
    driver = cursor.fetchone()
    cursor.close()
    return driver

def get_active_vehicles(connection):
    query = """
        SELECT
            id_kendaraan,
            nomer_polisi,
            jenis,
            kapasitas_ton,
            status_kendaraan
        FROM kendaraan
        WHERE aktif = TRUE
        AND status_kendaraan = 'SIAP'
        ORDER BY id_kendaraan;
    """

    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(query)
        vehicles = cursor.fetchall()

        return vehicles

def get_vehicle_for_dispatch(connection, pilih_kendaraan):
    query = """
        SELECT
            id_kendaraan,
            nomer_polisi,
            jenis,
            kapasitas_ton
        FROM kendaraan
        WHERE id_kendaraan = %s
        AND aktif = TRUE
        AND status_kendaraan = 'SIAP';
    """

    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(query, (pilih_kendaraan,))
        truck = cursor.fetchone()

    return truck

#function buat kiriman
def create_pengiriman(
    connection,
    id_driver,
    pilih_kendaraan,
    rute
):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO pengiriman (
            id_driver,
            id_kendaraan,
            rute,
            tanggal_keberangkatan
        )
        VALUES (%s, %s, %s, CURRENT_DATE)
        RETURNING id_pengiriman;
    """, (id_driver, pilih_kendaraan, rute))
    id_pengiriman = cursor.fetchone()[0]

    cursor.close()

    return id_pengiriman

def update_status_driver(connection, id_driver, status):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE driver
    SET status_driver = %s
    WHERE id_driver = %s;
    """, (status,id_driver))

    cursor.close()
#get max urutan for all driver's status
def get_max_urutan(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(urutan), 0) AS urutan_terbesar
        FROM driver
    """)
    max_urutan = cursor.fetchone()[0]
    cursor.close()

    return max_urutan

def update_urutan_driver(connection,  urutan_baru, id_driver):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE driver
    SET urutan = %s
    WHERE id_driver = %s;
    """, (urutan_baru, id_driver))

    cursor.close()

def keluarkan_urutan_driver_sementara(connection, urutan_driver):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE driver
    SET urutan = -urutan
    WHERE status_driver = 'SIAP'
    AND urutan > %s;
    """, (urutan_driver,))

    cursor.close()

def geser_antrian_driver(connection):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE driver
    SET urutan = ABS(urutan) - 1
    WHERE status_driver = 'SIAP' 
    AND urutan < 0 ;
    """)

    cursor.close()

def change_shipment_status(connection, status, id_pengiriman):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE pengiriman
    SET status = %s
    WHERE id_pengiriman = %s;
    """, (status, id_pengiriman))

    cursor.close()

#update vehicles status
def update_vehicle_status(connection, status, id_kendaraan):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE kendaraan
    SET status_kendaraan = %s
    WHERE id_kendaraan = %s;
    """, (status, id_kendaraan))

    cursor.close()

#orchestrator for make shipment
def dispatch_shipment(
    connection,
    pilih_kendaraan,
    rute
):
    driver = get_first_driver(connection)

    if driver is None:
        raise ValueError("No available drivers.")

    vehicles = get_vehicle_for_dispatch(connection, pilih_kendaraan)

    if not vehicles:
        raise ValueError("No available vehicles")

    try:
        id_pengiriman = create_pengiriman(
            connection,
            driver["id_driver"],
            pilih_kendaraan,
            rute
            )
        update_vehicle_status(connection, "DIPAKAI", pilih_kendaraan)
        change_shipment_status(connection, "ON_PROGRESS", id_pengiriman)
        update_status_driver(connection, driver["id_driver"], "LUAR_KOTA")
        max_urutan = get_max_urutan(connection)
        update_urutan_driver(connection, max_urutan + 1, driver["id_driver"])
        keluarkan_urutan_driver_sementara(connection, driver["urutan"])
        geser_antrian_driver(connection)

        connection.commit()

    except Exception:

        connection.rollback()

        raise

#return_shipment
#mencari pengiriman yang statusnya masih ON PROGRESS

def get_pengiriman_on_progress(connection):
    query = """
    SELECT 
        p.id_pengiriman,
        d.nama AS nama_driver,
        k.nomer_polisi,
        p.rute,
        p.tanggal_keberangkatan
    FROM pengiriman p
    JOIN driver d
        ON p.id_driver = d.id_driver
    JOIN kendaraan k
        ON p.id_kendaraan=k.id_kendaraan
    WHERE p.status = 'ON_PROGRESS'
    ORDER BY p.id_pengiriman;
    """

    with connection.cursor(row_factory=dict_row) as cursor:
        cursor.execute(query)
        shipment_on_progress = cursor.fetchall()

    return shipment_on_progress

#cari pengiriman berdasarkan id_pengiriman
def get_shipment_by_id(connection, id_pengiriman):
    cursor = connection.cursor(row_factory=dict_row)

    cursor.execute("""
    SELECT *
    FROM pengiriman
    WHERE id_pengiriman = %s;
    """, (id_pengiriman,))

    shipment_by_id = cursor.fetchone()

    cursor.close()

    return shipment_by_id

def finish_shipment(connection, id_pengiriman):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE pengiriman
    SET 
        status = 'DONE',
        tanggal_kembali = CURRENT_DATE
    WHERE id_pengiriman = %s;
    """, (id_pengiriman,))

    cursor.close()

#get max urutan driver for status = SIAP
def get_max_urutan_siap(connection,id_driver):
    cursor = connection.cursor()

    cursor.execute("""
    SELECT COALESCE(MAX(urutan), 0) AS urutan_terbesar_siap
    FROM driver
    WHERE status_driver = 'SIAP'
    AND id_driver <> %s;
    """, (id_driver,))

    max_urutan_siap = cursor.fetchone()[0]

    cursor.close()

    return max_urutan_siap



def return_shipment(
    connection,
    id_pengiriman
):

    try :
        shipment = get_shipment_by_id(connection, id_pengiriman)

        if shipment is None:
            raise ValueError("Shipment not found.")

        if shipment["status"] != "ON_PROGRESS":
            raise ValueError("X!! Shipment already completed.")
        
        else:
            finish_shipment(connection, id_pengiriman)
            update_vehicle_status(connection, "SIAP", shipment["id_kendaraan"])
            update_status_driver(connection, shipment["id_driver"], "SIAP")
            max_urutan_siap = get_max_urutan_siap(connection, shipment["id_driver"])
            update_urutan_driver(connection, max_urutan_siap + 1, shipment["id_driver"])

            connection.commit()

    except Exception:
    
        connection.rollback()
    
        raise


    #reset data
def reset_system_data(connection):
    try:
        with connection.cursor() as cursor:

            # Hapus shipment yang masih berjalan
            cursor.execute("""
                DELETE FROM pengiriman
                WHERE status = 'ON_PROGRESS';
            """)

            # Reset driver
            cursor.execute("""
                UPDATE driver
                SET
                    status_driver = 'SIAP',
                    urutan = id_driver;
            """)

            # Reset kendaraan
            cursor.execute("""
                UPDATE kendaraan
                SET
                    aktif = TRUE,
                    status_kendaraan = 'SIAP';
            """)

        connection.commit()

    except Exception:
        connection.rollback()
        raise