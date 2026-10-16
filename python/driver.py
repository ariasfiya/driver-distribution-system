from database import (
    get_max_urutan,
    update_status_driver,
    geser_antrian_driver
)

# Function untuk menambahkan driver baru
def add_driver(
        connection,
        nama,
    ):
    try:
        max_urutan = get_max_urutan(connection)
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO driver (nama, urutan, aktif, status_driver)
        VALUES
        (%s,%s,%s,%s);
        """, (nama, max_urutan + 1, True, "SIAP"))

        cursor.close()

        connection.commit()

    except Exception:

        connection.rollback()

        raise

# ---------
# proses unbah urutan akibat edit baik status maupun ubah urutan langsung
# ---------

# geser urutan semula ke urutan edit 
def update_urutan_target(connection, urutan_edit, id_driver):
    cursor=connection.cursor()

    cursor.execute("""
        UPDATE driver
        SET urutan = %s
        WHERE id_driver = %s;
    """, (urutan_edit, id_driver))

    cursor.close()


# update uurtan between
# urutan_semula (n) < urutan_edit (m) = geser negatif (-)
# urutan_semua (n) > urutan_edit (m) = geser positif (+)

def geser_urutan_between(connection, urutan_semula, urutan_edit):
    cursor = connection.cursor()

    if urutan_semula < urutan_edit:

        cursor.execute("""
            UPDATE driver
            SET urutan = urutan - 1
            WHERE urutan > %s
            AND urutan <= %s;
        """, (urutan_semula, urutan_edit))

    elif urutan_semula > urutan_edit:

        cursor.execute("""
            UPDATE driver
            SET urutan = urutan + 1
            WHERE urutan >= %s
            AND urutan < %s;
        """, (urutan_edit, urutan_semula))

    cursor.close()

# edit urutan
def edit_urutan(
    connection,
    urutan_semula,
    urutan_edit,
    id_driver
):
    try:
        geser_urutan_between(connection, urutan_semula, urutan_edit)
        update_urutan_target(connection, id_driver, urutan_edit)
        
        connection.commit()

    except Exception:

        connection.rollback()

        raise


# ---------
# Edit driver out (status) dan mengeluarkannya dari urutan
# 1. save urutan semula
# 2. update status driver
# 3. hapus urutan
# ---------

# simpan urutan sebelum keluar urutan
def save_urutan(connection, urutan):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE driver
        SET urutan_sebelumnya = urutan
        WHERE urutan = %s;
    """, (urutan,))

    cursor.close()

# keluarkan driver dari urutan (NULL)
def null_urutan(connection, id_driver):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE driver
        SET urutan = NULL
        WHERE id_driver = %s;
    """, (id_driver,))

    cursor.close()

# orchestrator edit status out
def update_driver_status_out(
    connection,
    urutan,
    status,
    id_driver
):
    try:
        save_urutan(connection, urutan)
        update_status_driver(connection, id_driver, status)
        null_urutan(connection, id_driver)
        geser_antrian_driver(connection, urutan)

        connection.commit()

    except Exception:

        connection.rollback()

        raise

# ---------
# Edit driver in (status) mengembalikan status menjadi SIAP dan memasukkan ke urutan
# 1. geser urutan diatas urutan driver yang masuk
# 2. update status driver menjadi SIAP
# 3. update urutan dari urutan semula sebellum update status
# 4. hapus urutan tersimpan
# ---------

# ambil urutan driver sebelumnya
def urutan_tersimpan(connection, id_driver):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT urutan_sebelumnya
        FROM driver
        WHERE id_driver = %s;
    """, (id_driver,))

    urutan_tersimpan = cursor.fetchone()[0] 
    cursor.close()
    
    return urutan_tersimpan

# geser urutan > in
def geser_urutan_in(connection, urutan):
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE driver
    SET urutan = urutan + 1
    WHERE status_driver = 'SIAP'
    AND urutan >= %s;
    """, (urutan,))

    cursor.close()


# hapus urutan sebelumnya
def null_urutan_sebelumnya(connection, id_driver):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE driver
        SET urutan_sebelumnya = NULL
        WHERE id_driver = %s;
    """, (id_driver,))


# orchestrator edit status in
def update_driver_status_in(
    connection,
    id_driver,
    status
):
    try:
        urutan_lama = urutan_tersimpan(connection, id_driver)
        geser_urutan_in(connection, urutan_lama)
        update_status_driver(connection, id_driver, status)
        update_urutan_target(connection, urutan_lama, id_driver)
        null_urutan_sebelumnya(connection, id_driver)

        connection.commit()
        
    except Exception:
        
        connection.rollback()
        
        raise