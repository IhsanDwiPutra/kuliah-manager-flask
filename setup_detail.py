import sqlite3

koneksi = sqlite3.connect('kuliah.db')
kursor = koneksi.cursor()

# Tabel jurnal perkeliahan
kursor.execute('''
    CREATE TABLE IF NOT EXISTS jurnal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jadwal_id INTEGER NOT NULL,
        pertemuan_ke INTEGER NOT NULL,
        tanggal TEXT NOT NULL,
        materi TEXT NOT NULL,
        FOREIGN KEY (jadwal_id) REFERENCES jadwal(id)
    )    
    ''')

# Tabel resources
kursor.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jadwal_id INTEGER NOT NULL,
        nama_link TEXT NOT NULL,
        url TEXT NOT NULL,
        FOREIGN KEY (jadwal_id) REFERENCES jadwal(id)
    )
    ''')

koneksi.commit()
koneksi.close()

print('Tabel Jurnal dan Resources sukses ditambahkan ke brankas!')