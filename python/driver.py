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

        if not nama or not nama.strip():
            raise ValueError("Nama driver tidak boleh kosong")

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

    geser_urutan_between(connection, urutan_semula, urutan_edit)
    update_urutan_target(connection, urutan_edit, id_driver)



# ---------
# Edit driver out (status) dan mengeluarkannya dari urutan
# 1. save urutan semula
# 2. update status driver
# 3. hapus urutan
# ---------

# simpan urutan sebelum keluar urutan
def save_urutan(connection, id_driver):
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE driver
        SET urutan_sebelumnya = urutan
        WHERE id_driver = %s;
    """, (id_driver,))

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

    save_urutan(connection, id_driver)
    update_status_driver(connection, id_driver, status)
    null_urutan(connection, id_driver)
    geser_antrian_driver(connection, urutan)


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

    cursor.close()

# orchestrator edit status in
def update_driver_status_in(
    connection,
    masuk_urutan,
    id_driver,
    status
):

    geser_urutan_in(connection, masuk_urutan)
    update_status_driver(connection, id_driver, status)
    update_urutan_target(connection, masuk_urutan, id_driver)
    null_urutan_sebelumnya(connection, id_driver)

# orchestrator untuk menjalankan edit driver

def edit_driver(
    connection,
    id_driver,
    perubahan
):
    try:
        cursor = connection.cursor()

        # Mencegah proses edit antrean lain berjalan bersamaan
        cursor.execute("""
            LOCK TABLE driver IN SHARE ROW EXCLUSIVE MODE;
        """)

        # Ambil data driver yang akan diedit
        cursor.execute("""
            SELECT
                id_driver,
                nama,
                urutan,
                aktif,
                status_driver,
                urutan_sebelumnya
            FROM driver
            WHERE id_driver = %s
            FOR UPDATE;
        """, (id_driver,))

        driver = cursor.fetchone()

        if driver is None:
             raise ValueError("Driver tidak ditemukan")

        # jika ada unpacking tuple
        (
            id,
            nama_lama,
            urutan_lama,
            aktif_lama,
            status_lama,
            urutan_sebelumnya
        ) = driver

        # Drivr dengan status LUAR KOTA tidak boleh diedit
        if status_lama == "LUAR_KOTA":
            raise ValueError("Driver LUAR KOTA tidak dapat diedit")

        # Ambil data baru. Jika key tidak ditemukan, gunakan nilai lama
        aktif_baru = perubahan.get("aktif",aktif_lama)
        urutan_baru = perubahan.get("urutan", urutan_lama)
        status_baru = perubahan.get("status_driver",status_lama)
        nama_baru = perubahan.get("nama",nama_lama)

        status_valid = ["SIAP", "IZIN", "SAKIT", "BERTUGAS", "OFF"]

        if status_baru not in status_valid:
            raise ValueError("Status driver tidak valid.")

        if not nama_baru or not nama_baru.strip():
            raise ValueError("Nama driver tidak boleh kosong.")

        # bandingkan data lama dengan data baru
        urutan_berubah = urutan_baru != urutan_lama
        nama_berubah = nama_baru != nama_lama
        aktif_berubah = aktif_baru != aktif_lama
        status_berubah = status_baru != status_lama

        # user melakukan atau mengirim urutan baru
        urutan_dikirim = "urutan" in perubahan

        # -------------------------------------------------
        # KONDISI 1: DRIVER AKTIF MENJADI NONAKTIF
        # -------------------------------------------------
        if aktif_lama and not aktif_baru:

            cursor.execute("""
                UPDATE driver
                SET aktif = FALSE
                WHERE id_driver = %s;
            """, (id_driver,))

            # Keluarkan driver dari antrean dan ubah status driver
            if status_lama == "SIAP":
                update_driver_status_out(
                    connection,
                    urutan_lama,
                    "OFF",
                    id_driver
                )

            else:
                # Driver sebelumnya sudah tidak berada di antrean
                cursor.execute("""
                    UPDATE driver
                        SET status_driver = 'OFF',
                        urutan = NULL
                    WHERE id_driver = %s;
                """, (id_driver,))

            cursor.execute("""
                UPDATE driver
                SET urutan_sebelumnya = NULL
                WHERE id_driver = %s;
            """,(id_driver,))

        # -------------------------------------------------
        # KONDISI 2: DRIVER NONAKTIF MENJADI AKTIF
        # -------------------------------------------------
        elif not aktif_lama and aktif_baru:

            # update aktif menjadi TRUE
            cursor.execute("""
                UPDATE driver
                SET aktif = TRUE
                WHERE id_driver = %s;
            """, (id_driver,))

            # Driver masuk ke posisi terakhir antrean
            cursor.execute("""
                SELECT COALESCE(MAX(urutan), 0)
                FROM driver
                WHERE aktif = TRUE
                  AND status_driver = 'SIAP';
            """)

            urutan_terakhir = cursor.fetchone()[0]

            masuk_urutan = urutan_terakhir +1
            status = "SIAP"
            update_driver_status_in(
                connection,
                masuk_urutan,
                id_driver,
                status
            )

        # -------------------------------------------------
        # KONDISI 3: DRIVER TETAP AKTIF
        # -------------------------------------------------
        else:
            # status awal adalah SIAP
            masuk_antrian_lama = status_lama == "SIAP"
            # status edit selain SIAP
            masuk_antrian_baru = status_baru == "SIAP"

            # Driver keluar dari antrean (SIAP ke status lain)
            if masuk_antrian_lama and not masuk_antrian_baru:

                # Jika urutan diminta berubah (user merubah status dan urutanya), uurtan pindahkan dahulu
                if urutan_dikirim and urutan_baru != urutan_lama:
                    edit_urutan(
                        connection,
                        urutan_lama,
                        urutan_baru,
                        id_driver
                    )

                    # urutan baru dijadaikan urtan yang tersimpan
                    urutan_keluar = urutan_baru
                else:
                    urutan_keluar = urutan_lama

                update_driver_status_out(
                    connection,
                    urutan_keluar,
                    status_baru,
                    id_driver
                )

            # Driver masuk kembali ke antrean (dari status selian SIAP ke SIAP)
            elif not masuk_antrian_lama and masuk_antrian_baru:

                urutan_masuk = urutan_tersimpan(connection, id_driver)
                max_urutan = get_max_urutan(connection)

                if urutan_masuk <= max_urutan:
                    masuk_urutan = urutan_masuk
                else:
                    masuk_urutan = max_urutan + 1

                update_driver_status_in(
                    connection,
                    masuk_urutan,
                    id_driver,
                    "SIAP"
                )

                # Jika pengguna menentukan posisi baru,
                # pindahkan setelah driver masuk antrean

                if urutan_dikirim:
                    # ambil urutan sebelum edit
                    cursor.execute("""
                        SELECT urutan
                        FROM driver
                        WHERE id_driver = %s;
                    """, (id_driver,))

                    urutan_sekarang = cursor.fetchone()[0]

                    if urutan_sekarang != urutan_baru:
                        edit_urutan(
                            connection,
                            urutan_sekarang,
                            urutan_baru,
                            id_driver
                        )

            # Driver tetap berada di antrean status drivrt tetap SIAP tidak diubah
            elif masuk_antrian_lama and masuk_antrian_baru:

                # driver merubah urutan
                # 1. melihat apakah ada kiriman perubahan
                # 2. melihat apakah kiriman perubahan sama atau tidak
                if urutan_dikirim and urutan_baru != urutan_lama:
                    edit_urutan(
                        connection,
                        urutan_lama,
                        urutan_baru,
                        id_driver
                    )

            # Driver tetap di luar antrean, hanya status yang berubah
            else:

                if status_baru != status_lama:
                    cursor.execute("""
                        UPDATE driver
                        SET status_driver = %s
                        WHERE id_driver = %s;
                    """, (status_baru, id_driver))

        # -------------------------------------------------
        # UPDATE NAMA
        # -------------------------------------------------
        if nama_berubah:
            cursor.execute("""
                UPDATE driver
                SET nama = %s
                WHERE id_driver = %s;
            """, (nama_baru.strip(), id_driver))

        connection.commit()

        return {
            "message": "Data driver berhasil diperbarui."
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()