ALTER TABLE kendaraan
ADD COLUMN status_kendaraan VARCHAR(20)
    NOT NULL
    DEFAULT 'SIAP'
    CHECK (status_kendaraan in ('SIAP', 'DIPAKAI', 'PERBAIKAN'));