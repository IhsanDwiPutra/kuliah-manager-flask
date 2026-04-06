import sqlite3

# 1. Membuat koneksi ke database (kalau filenya belum ada, otomatis akan dibuatkan)
koneksi = sqlite3.connect('kuliah.db')

# 2. Membuat kursor (ibarat 'tangan' yang akan mengetik perintah SQL ke dalam database)
kursor = koneksi.cursor()

# 3. Menulis perintah SQL untuk membuat tabel bernama 'tugas'
kursor.execute('''
    CREATE TABLE IF NOT EXISTS tugas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matkul TEXT NOT NULL,
        deskripsi TEXT NOT NULL,
        deadline TEXT NOT NULL,
        status TEXT NOT NULL
    )
''')

# 4. Mengunci (save) perubahan dan menutup brankasnya
koneksi.commit()
koneksi.close()

print("Mantap! Database kuliah.db dan tabel tugas berhasil dibuat!")