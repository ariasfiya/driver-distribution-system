-- kolom untuk mengingat urutan driver sebelum dikeluarkan karena ijin atau tidak masuk
ALTER TABLE driver
ADD COLUMN urutan_sebelumnya INTEGER;

-- hapus NOT NULL pada urutan driver untuk driver yang ijin atau tidak masuk
ALTER TABLE driver
ALTER COLUMN urutan DROP NOT NULL;