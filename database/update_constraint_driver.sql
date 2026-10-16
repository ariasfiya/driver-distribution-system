-- hapus unique di lomom uurtan
ALTER TABLE driver
DROP CONSTRAINT driver_urutan_key;

-- update logic unique agar diperiksa setelah semua baris diproses
ALTER TABLE driver
ADD CONSTRAINT driver_urutan_key
UNIQUE (urutan)
DEFERRABLE INITIALLY DEFERRED;