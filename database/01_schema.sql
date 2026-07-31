-- ============================================
-- DRIVER DISTRIBUTION DATABASE
-- File : 01_schema.sql
-- Tujuan : Membuat struktur database
-- ============================================

-- ============================================
-- TABEL DRIVER
-- ============================================

CREATE TABLE driver (
    id_driver SERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    urutan INTEGER NOT NULL,
    aktif BOOLEAN DEFAULT TRUE,
    status_driver VARCHAR(20) NOT NULL DEFAULT 'SIAP'
);

-- ============================================
-- TABEL KENDARAAN
-- ============================================

CREATE TABLE kendaraan(
    id_kendaraan SERIAL PRIMARY KEY,
    nomer_polisi VARCHAR(20) NOT NULL UNIQUE,
    jenis VARCHAR(50),
    kapasitas_ton DECIMAL(5,2),
    aktif BOOLEAN DEFAULT TRUE
);

-- ============================================
-- TABEL PENGIRIMAN
-- ============================================

CREATE TABLE pengiriman (
    id_pengiriman SERIAL PRIMARY KEY,
    id_driver INTEGER REFERENCES driver(id_driver) NOT NULL,
    id_kendaraan INTEGER REFERENCES kendaraan(id_kendaraan) NOT NULL,
    rute VARCHAR(100) NOT NULL,
    tanggal_keberangkatan DATE NOT NULL,
    tanggal_kembali DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'MENUNGGU'
);