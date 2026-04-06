import sqlite3

koneksi = sqlite3.connect('kuliah.db')
kursor = koneksi.cursor()

# Buat tabel jadwal
kursor.execute(''' 
    CREATE TABLE IF NOT EXISTS jadwal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matkul TEXT NOT NULL,
        dosen TEXT NOT NULL,
        hari TEXT NOT NULL,
        jam TEXT NOT NULL,
        sks INTEGER NOT NULL,
        ruang TEXT NOT NULL,
        semester INTEGER NOT NULL
    )
    ''')

# Suntikkan beberapa data awal sesui jawal Semester 2
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Pendidikan Agama', 'Amar Maruf', 'Senin', '08:20-10:00', 2, 'E-learning', 2))
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Pemrograman Berbasis Objek', 'Muhammad Rezki', 'Selasa', '07:30-10:50', 4, '301', 2))
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Bahasa Inggris II', 'Yeni Mustika', 'Selasa', '15:50-17:30', 2, 'E-learning', 2))
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Sistem Operasi', 'Erni', 'Rabu', '07:30-10:00', 3, '301', 2))
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Arsitektur Komputer', 'Eka Rahmawati', 'Rabu', '15:00-17:30', 3, 'E-learning', 2))
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Struktur Data', 'Windi Irmayani', 'Kamis', '07:30-10:00', 3, '305', 2))
kursor.execute('INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)', ('Kalkulus', 'Deasy Purwaningtias', 'Kamis', '12:30-15:30', 3, '305', 2))

koneksi.commit()
koneksi.close()

print('Tabel Jadwal sukses dibangun di brankas!')