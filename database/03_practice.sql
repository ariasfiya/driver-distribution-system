SELECT *
FROM driver
WHERE aktif = TRUE
AND status_driver = 'SIAP'
ORDER BY urutan
LIMIT 1;

INSERT INTO pengiriman (
    id_driver,
    id_kendaraan,
    rute,
    tanggal_keberangkatan
)
SELECT
    id_driver,
    2,
    JBR-BWI,
    CURRENT_DATE
FROM driver
WHERE aktif = TRUE
  AND status_driver = 'SIAP'
ORDER BY urutan,
LIMIT 1;

-- menampilkan kendaraan yang sktif
SELECT
    id_kendaraan,
    nomer_polisi,
    jenis,
    kapasitas_ton
FROM kendaraan
WHERE aktif = TRUE
ORDER BY nomer_polisi;