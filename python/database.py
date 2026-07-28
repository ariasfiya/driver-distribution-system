import psycopg

def connect_db():
    connection = psycopg.connect(
        host="localhost",
        port="5432",
        dbname="driver_distribution",
        user="postgres",
        password="postgres"
    )
    return connection

def get_first_driver(connection):
    cursor = connection.cursor()

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
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id_kendaraan,
            nomer_polisi,
            jenis,
            kapasitas_ton
        FROM kendaraan
        WHERE aktif = TRUE
        ORDER BY id_kendaraan    
    """)
    vehicles = cursor.fetchall()
    cursor.close()
    return vehicles

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
        VALUES (%s, %s, %s, CURRENT_DATE);
    """, (id_driver, pilih_kendaraan, rute))

    cursor.close()



def update_status_driver(connection, id_driver, status):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE driver
    SET status_driver = %s
    WHERE id_driver = %s;
    """, (status,id_driver))

    cursor.close()

def get_max_urutan(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(MAX(urutan), 0) AS urutan_terbesar
        FROM driver
    """)
    max_urutan = cursor.fetchone()[0]
    cursor.close()

    return max_urutan

def update_urutan_driver(connection, id_driver, urutan_baru):
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


#orchestrator
def dispatch_shipment(
    connection,
    id_driver,
    pilih_kendaraan,
    rute,
    urutan_driver
    
    ):

    try:
        create_pengiriman(
            connection,
            id_driver,
            pilih_kendaraan,
            rute
            )
        update_status_driver(connection, id_driver, "LUAR_KOTA")
        max_urutan = get_max_urutan(connection)
        update_urutan_driver(connection, id_driver, max_urutan + 1)
        keluarkan_urutan_driver_sementara(connection, urutan_driver)
        geser_antrian_driver(connection)

        connection.commit()

    except Exception:

        connection.rollback()

        raise
    