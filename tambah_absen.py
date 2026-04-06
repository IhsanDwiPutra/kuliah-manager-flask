import sqlite3

# Buka brankas kuliah.db yang sudah ada
koneksi = sqlite3.connect('kuliah.db')
kursor = koneksi.cursor()

# Buat tabel baru khusus untuk absen
kursor.execute('''
    CREATE TABLE IF NOT EXISTS absen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matkul TEXT NOT NULL,
        hadir INTEGER NOT NULL,
        total_pertemuan INTEGER NOT NULL
    )
    ''')

# Kita suntikkan 2 data pancingan dari mata kuliah semester ini
kursor.execute("INSERT INTO absen (matkul, hadir, total_pertemuan) VALUES (?, ?, ?)",('Pemrograman Berbasis Objek', 12, 14))
kursor.execute("INSERT INTO absen (matkul, hadir, total_pertemuan) VALUES (?, ?, ?)", ('Kalkulus', 7, 14))

koneksi.commit()
koneksi.close()

print("Mantap! Tabel Absen berhasil ditambahkan ke brankas!")