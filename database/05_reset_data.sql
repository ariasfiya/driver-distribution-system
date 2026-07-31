-- Hapus seluruh data pengiriman
DELETE FROM pengiriman;

-- Kembalikan seluruh driver menjadi siap
UPDATE driver
SET status_driver = 'SIAP';

-- Pindahkan sementara ke angka negatif
-- agar tidak melanggar UNIQUE saat reset urutan
UPDATE driver
SET urutan = -urutan;

-- Kembalikan urutan sesuai id_driver
UPDATE driver
SET urutan = id_driver;

-- kembalikan status pengiriman dan tgl kembali
UPDATE pengiriman
SET 
	status = 'ON_PROGRESS',
	tanggal_kembali = NULL
WHERE 
	status = 'DONE'
AND tanggal_kembali IS NOT NULL;