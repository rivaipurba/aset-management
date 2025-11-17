-- migrations_assets.sql
-- Postgres SQL for Asset Management (TI assets only)
-- Revised: removed purchase_date, warranty_until, image_url

BEGIN;

-- 1) Setup: extension (optional, for UUID if wanted later)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2) Tabel asset_types
CREATE TABLE IF NOT EXISTS asset_types (
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL, -- 'laptop','pc','printer','scanner','monitor'
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3) Tabel assets (common fields)
CREATE TABLE IF NOT EXISTS assets (
  id SERIAL PRIMARY KEY,
  asset_type_id INTEGER NOT NULL REFERENCES asset_types(id) ON DELETE RESTRICT,
  name VARCHAR(255) NOT NULL,
  serial_number VARCHAR(255) UNIQUE, -- nullable allowed; unique if present
  maker VARCHAR(255),
  owner VARCHAR(255),
  location VARCHAR(255),
  status VARCHAR(50) NOT NULL DEFAULT 'available', -- available / in_use / maintenance / retired
  condition VARCHAR(50),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4) Spesifikasi khusus per jenis
-- Computers (Laptop / PC)
CREATE TABLE IF NOT EXISTS computer_specs (
  id SERIAL PRIMARY KEY,
  asset_id INTEGER UNIQUE NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ram VARCHAR(50),
  storage VARCHAR(100),
  processor VARCHAR(255),
  os VARCHAR(100)
);

-- Printer specs
CREATE TABLE IF NOT EXISTS printer_specs (
  id SERIAL PRIMARY KEY,
  asset_id INTEGER UNIQUE NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  is_color BOOLEAN NOT NULL DEFAULT FALSE
);

-- Monitor specs
CREATE TABLE IF NOT EXISTS monitor_specs (
  id SERIAL PRIMARY KEY,
  asset_id INTEGER UNIQUE NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  size_inch NUMERIC(4,1) -- e.g., 24.0
);

-- Scanner specs (optional extra fields)
CREATE TABLE IF NOT EXISTS scanner_specs (
  id SERIAL PRIMARY KEY,
  asset_id INTEGER UNIQUE NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  dpi INTEGER,
  connection_type VARCHAR(50) -- e.g., usb, network
);

-- 5) Riwayat perpindahan / assignment
CREATE TABLE IF NOT EXISTS asset_movements (
  id SERIAL PRIMARY KEY,
  asset_id INTEGER NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  from_location VARCHAR(255),
  to_location VARCHAR(255) NOT NULL,
  performed_by VARCHAR(255),
  performed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  note TEXT
);

-- 6) Trigger untuk updated_at (update timestamp otomatis)
CREATE OR REPLACE FUNCTION trg_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_timestamp ON assets;
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON assets
FOR EACH ROW
EXECUTE FUNCTION trg_set_timestamp();

-- 7) Indexes for performance (common filters/searches)
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(asset_type_id);
CREATE INDEX IF NOT EXISTS idx_assets_location ON assets(location);
CREATE INDEX IF NOT EXISTS idx_assets_owner ON assets(owner);
CREATE INDEX IF NOT EXISTS idx_assets_status ON assets(status);
-- serial_number already UNIQUE -> index present

-- 8) Seed data: asset types
INSERT INTO asset_types (code, name)
VALUES
  ('laptop', 'Laptop'),
  ('pc', 'PC'),
  ('printer', 'Printer'),
  ('scanner', 'Scanner'),
  ('monitor', 'Monitor')
ON CONFLICT (code) DO NOTHING;

-- 9) Seed example assets + specs
-- Laptop example
INSERT INTO assets (asset_type_id, name, serial_number, maker, owner, location, status, condition, notes)
VALUES (
  (SELECT id FROM asset_types WHERE code='laptop'),
  'Laptop - A1',
  'LAP-2023-0001',
  'Lenovo',
  'IT Dept',
  'Gedung A - Lantai 2',
  'available',
  'good',
  'Diberikan untuk karyawan baru'
)
RETURNING id INTO TEMP TABLE tmp_laptop_id;

-- Insert laptop specs using returned id
-- Note: Use a SELECT to grab id
WITH lap AS (
  SELECT id FROM assets WHERE serial_number = 'LAP-2023-0001'
)
INSERT INTO computer_specs (asset_id, ram, storage, processor, os)
SELECT id, '16GB', '512GB SSD', 'Intel Core i5-1135G7', 'Windows 11' FROM lap
ON CONFLICT DO NOTHING;

-- PC example
INSERT INTO assets (asset_type_id, name, serial_number, maker, owner, location, status, condition, notes)
VALUES (
  (SELECT id FROM asset_types WHERE code='pc'),
  'PC - Workstation 01',
  'PC-2022-0101',
  'Dell',
  'Design Dept',
  'Gedung B - Lantai 1',
  'in_use',
  'good',
  'Workstation untuk desainer'
)
ON CONFLICT (serial_number) DO NOTHING;

WITH pc AS (
  SELECT id FROM assets WHERE serial_number = 'PC-2022-0101'
)
INSERT INTO computer_specs (asset_id, ram, storage, processor, os)
SELECT id, '32GB', '1TB SSD', 'Intel Xeon E-2236', 'Windows 10 Pro' FROM pc
ON CONFLICT DO NOTHING;

-- Printer example (color)
INSERT INTO assets (asset_type_id, name, serial_number, maker, owner, location, status, condition, notes)
VALUES (
  (SELECT id FROM asset_types WHERE code='printer'),
  'Printer - OfficeColor 1',
  'PRN-1001',
  'HP',
  'Office',
  'Gedung A - Lantai GF',
  'available',
  'good',
  'Printer kantor utama'
)
ON CONFLICT (serial_number) DO NOTHING;

WITH pr AS (SELECT id FROM assets WHERE serial_number = 'PRN-1001')
INSERT INTO printer_specs (asset_id, is_color)
SELECT id, TRUE FROM pr
ON CONFLICT DO NOTHING;

-- Monitor example
INSERT INTO assets (asset_type_id, name, serial_number, maker, owner, location, status, condition, notes)
VALUES (
  (SELECT id FROM asset_types WHERE code='monitor'),
  'Monitor - 24 inch IPS',
  'MON-2401',
  'Asus',
  'Design Dept',
  'Gedung B - Lantai 1',
  'in_use',
  'good',
  'Monitor untuk designer'
)
ON CONFLICT (serial_number) DO NOTHING;

WITH mo AS (SELECT id FROM assets WHERE serial_number = 'MON-2401')
INSERT INTO monitor_specs (asset_id, size_inch)
SELECT id, 24.0 FROM mo
ON CONFLICT DO NOTHING;

-- Scanner example
INSERT INTO assets (asset_type_id, name, serial_number, maker, owner, location, status, condition, notes)
VALUES (
  (SELECT id FROM asset_types WHERE code='scanner'),
  'Scanner - ADF 1',
  'SCN-9001',
  'Fujitsu',
  'Admin Dept',
  'Gedung A - Lantai 2',
  'available',
  'good',
  'Scanner ADF untuk dokumen'
)
ON CONFLICT (serial_number) DO NOTHING;

WITH sc AS (SELECT id FROM assets WHERE serial_number = 'SCN-9001')
INSERT INTO scanner_specs (asset_id, dpi, connection_type)
SELECT id, 600, 'usb' FROM sc
ON CONFLICT DO NOTHING;

-- 10) Sample movements
INSERT INTO asset_movements (asset_id, from_location, to_location, performed_by, performed_at, note)
VALUES
  (
    (SELECT id FROM assets WHERE serial_number = 'LAP-2023-0001'),
    'Gudang',
    'Gedung A - Lantai 2',
    'Admin IT',
    now() - interval '30 days',
    'Distribusi awal'
  ),
  (
    (SELECT id FROM assets WHERE serial_number = 'PC-2022-0101'),
    'Gudang',
    'Gedung B - Lantai 1',
    'Admin IT',
    now() - interval '200 days',
    'Dipindahkan ke Design Dept'
  );

-- 11) Clean up temp objects (if any)
-- (we used CTE approach; no temp tables should remain)

COMMIT;

-- Optional: basic SELECTs for quick check
-- SELECT a.id, at.code AS type, a.name, a.serial_number, a.owner, a.location FROM assets a JOIN asset_types at ON a.asset_type_id = at.id ORDER BY a.id;
