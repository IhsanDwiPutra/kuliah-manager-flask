import sqlite3

koneksi = sqlite3.connect('kuliah.db')
kursor = koneksi.cursor()

# Tabel Manajemen Konten
kursor.execute('''
    CREATE TABLE IF NOT EXISTS konten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        status TEXT NOT NULL, -- Ide, Riset, Scripting, AI Process, Editing, Ready
        platform_yt INTEGER DEFAULT 0,
        platform_tt INTEGER DEFAULT 0,
        platform_ig INTEGER DEFAULT 0,
        prompt_ai TEXT,
        link_riset TEXT,
        tanggal_post TEXT
    )
    ''')

koneksi.commit()
koneksi.close()
print("Brankas Konten Kreator siap digunakan!")