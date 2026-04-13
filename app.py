import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime

# Ini untuk menginisialisasi aplikasi Flask
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_portal_ihsan'

# Mesin login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['password']
        
        if username_input == 'ihsan' and password_input == '#admin123':
            session['sudah_login'] = True # Berikan stempel VIP
            return redirect(url_for('halaman_jadwal'))
        else:
            flash('Username atau Password salah, Bro!', 'danger')
            
    return render_template('login.html')

# Mesin logout
@app.route('/logout')
def logout():
    session.clear() # hapus stempel VIP
    flash('Kamu berhasil keluar. Aman!', 'success')
    return redirect(url_for('login'))

# Ini adalah fungsi khusus untuk membuka pintu brankas database
def get_db_connection():
    conn = sqlite3.connect('kuliah.db')
    
    # Fungsi data berbentuk seperti Dictionary Python
    conn.row_factory = sqlite3.Row
    return conn

# Route untuk halaman Jadwal (Halaman Utama)
@app.route('/')
def halaman_jadwal():
    # Satpam login
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    # Buka brankas dan ambil jadwal semester 2
    conn = get_db_connection()
    data_jadwal = conn.execute('SELECT * FROM jadwal WHERE semester = 2').fetchall()
    conn.close()
    
    # sensor hari: deteksi hari ini dalam bahasa inggris, lalu terjemahkan
    hari_inggris = datetime.now().strftime('%A')
    kamus_hari = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }
    hari_ini_indo = kamus_hari.get(hari_inggris)
    
    # Kirim data jadwal dan data hari ini ke HTML    
    return render_template('index.html', jadwal_kuliah=data_jadwal, hari_ini=hari_ini_indo)

# Route untuk halaman Tugas
@app.route('/tugas', methods=['GET', 'POST'])
def halaman_tugas():
    
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    # Buka koneksi ke database
    conn = get_db_connection()
    
    # Jika ada data yang dikirim dari Formulir (POST)
    if request.method == 'POST':
        # Tangkap datanya berdasarkan attribut 'name' di HTML
        matkul_baru = request.form['matkul']
        deskripsi_baru = request.form['deskripsi']
        deadline_baru = request.form['deadline']
        status_baru = request.form['status']
        
        # Masukkan ke dalam brankas database pakai SQL (INSERT)
        conn.execute('INSERT INTO tugas (matkul, deskripsi, deadline, status) VALUES (?, ?, ?, ?)', (matkul_baru, deskripsi_baru, deadline_baru, status_baru))
        conn.commit() # Kunci brankasnya
        conn.close()
        
        # Refresh halamannya secara otomatis biar datanya langsung muncul
        return redirect(url_for('halaman_tugas'))
    
    # Ambil semua data dari tabel 'tugas' menggunakan bahasa SQL
    tugas_dari_db = conn.execute('SELECT * FROM tugas').fetchall()
    
    # Tutup kembali pintunya agar aman
    conn.close()
    
    # Kirim data asli tersebut ke HTML
    return render_template('tugas.html', tugas_dikirim=tugas_dari_db)

# Route untuk menyimpan jadwal baru dari Modal
@app.route('/tambah_jadwal', methods=['POST'])
def tambah_jadwal():
    # satpam keamanan
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    matkul = request.form['matkul']
    dosen = request.form['dosen']
    hari = request.form['hari']
    jam = request.form['jam']
    sks = request.form['sks']
    ruang= request.form['ruang']
    semester = request.form['semester']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO jadwal (matkul, dosen, hari, jam, sks, ruang, semester) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (matkul, dosen, hari, jam, sks, ruang, semester))
    
    conn.commit()
    conn.close()
    
    flash('Mantap! Jadwal baru berhasil ditambahkan.', 'success')
    return redirect(url_for('halaman_jadwal'))

# Rute hapus jadwal
@app.route('/hapus_jadwal/<int:id_jadwal>')
def hapus_jadwal(id_jadwal):
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM jadwal WHERE id = ?', (id_jadwal,))
    conn.commit()
    conn.close()
    
    flash('Jadwal berhasil dihapus!', 'success')
    return redirect(url_for('halaman_jadwal'))

# Rute edit jadwal
@app.route('/edit_jadwal/<int:id_jadwal>', methods=['POST'])
def edit_jadwal(id_jadwal):
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    # Ambil data dari form Modal edit
    matkul_baru = request.form['matkul']
    dosen_baru = request.form['dosen']
    hari_baru = request.form['hari']
    jam_baru = request.form['jam']
    sks_baru = request.form['sks']
    ruang_baru = request.form['ruang']
    
    conn = get_db_connection()
    # update brankas
    conn.execute('''
        UPDATE jadwal
        SET matkul = ?, dosen = ?, hari = ?, jam = ?, sks = ?, ruang = ?
        WHERE id = ?
    ''', (matkul_baru, dosen_baru, hari_baru, jam_baru, sks_baru, ruang_baru, id_jadwal))
    
    conn.commit()
    conn.close()
    
    flash('Jadwal berhasil diperbarui!', 'success')
    return redirect(url_for('halaman_jadwal'))

# Rute detail kelas
@app.route('/detail/<int:id_jadwal>')
def detail_kelas(id_jadwal):
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # ambil info matkul ini
    matkul_info = conn.execute('SELECT * FROM jadwal WHERE id = ?', (id_jadwal,)).fetchone()
    
    # ambil data jurnal untuk matkul ini (diurutkan dari pertemuan terkecil)
    data_jurnal = conn.execute('SELECT * FROM jurnal WHERE jadwal_id = ? ORDER BY pertemuan_ke ASC', (id_jadwal,)).fetchall()
    
    # ambil data resources untuk matkul ini
    data_resources = conn.execute('SELECT * FROM resources WHERE jadwal_id = ?', (id_jadwal,)).fetchall()
    
    # trik cerdas: ambil tugas dari tabel 'tugas' yang nama matkulnya SAMA dengan nama matkul ini
    data_tugas = conn.execute('SELECT * FROM tugas WHERE matkul = ?', (matkul_info['matkul'],)).fetchall()
    
    conn.close()
    
    # kirim semuanya ke halaman detail_kelas.html
    return render_template('detail_kelas.html', matkul=matkul_info, jurnal=data_jurnal, resources=data_resources, tugas=data_tugas)

# Rute Tambah Jurnal
@app.route('/tambah_jurnal/<int:id_jadwal>', methods=['POST'])
def tambah_jurnal(id_jadwal):
    if not session.get('sudah_login'): return redirect(url_for('login'))
    
    pertemuan_ke = request.form['pertemuan_ke']
    tanggal = request.form['tanggal']
    materi = request.form['materi']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO jurnal (jadwal_id, pertemuan_ke, tanggal, materi) VALUES (?, ?, ?, ?)
    ''', (id_jadwal, pertemuan_ke, tanggal, materi))
    
    conn.commit()
    conn.close()
    
    flash('Mantap! Jurnal pertemuan berhasil dicatat.', 'success')
    return redirect(url_for('detail_kelas', id_jadwal=id_jadwal))

# Rute tambah link
@app.route('/tambah_link/<int:id_jadwal>', methods=['POST'])
def tambah_link(id_jadwal):
    if not session.get('sudah_login'): return redirect(url_for('login'))
    
    nama_link = request.form['nama_link']
    url = request.form['url']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO resources (jadwal_id, nama_link, url) VALUES (?, ?, ?)
    ''', (id_jadwal, nama_link, url))
    
    conn.commit()
    conn.close()
    
    flash('Referensi Link berhasil disimpan.', 'success')
    return redirect(url_for('detail_kelas', id_jadwal=id_jadwal))

# Route untuk halaman Absen
@app.route('/absen', methods=['GET', 'POST'])
def halaman_absen():
    
    # dua baris satpam
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Jika ada data baru dikirim dari form
    if request.method == 'POST':
        matkul_baru = request.form['matkul']
        total_baru = request.form['total_pertemuan']
        
        # cek apakah matkul ini sudah ada di brankas
        cek_matkul = conn.execute('SELECT * FROM absen WHERE matkul = ?', (matkul_baru,)).fetchone()
        
        # cek validasi
        if cek_matkul:
            # kalau datanya ditemukan, kasih pesan error merah
            flash('Gagal: Mata Kuliah tersebut sudah ada di daftar!', 'danger')
        else:
            # Kalau belum ada, baru simpan ke brankas
            conn.execute('INSERT INTO absen (matkul, hadir, total_pertemuan) VALUES (?, 0, ?)', (matkul_baru, total_baru))
            conn.commit()
            # Kasih pesan sukses hijau
            flash('Sukses: Kuliah berhasil ditambahkan!', 'success')
        
        
        conn.close()
        
        # Refresh halaman
        return redirect(url_for('halaman_absen'))
    
    data_absen_db = conn.execute('SELECT * FROM absen').fetchall()
    conn.close()
    
    # Buat kotak kosong untuk menyimpan data yanda sudah dihitung
    data_absen_lengkap = []
    
    # Loop datanya satu per satu untuk dihitung persentasenya
    for absen in data_absen_db:
        # Rumus: (Hadir / Total) * 100
        persentase = (absen['hadir'] / absen['total_pertemuan']) * 100
        persentase_bulat = round(persentase) # Bulatkan agar tidak ada koma panjang
        
        # Masukkan kembali datanya beserta hasil hitungannya ke dalam kotak
        data_absen_lengkap.append({
            'id': absen['id'],
            'matkul': absen['matkul'],
            'hadir': absen['hadir'],
            'total_pertemuan': absen['total_pertemuan'],
            'persentase': persentase_bulat
        })
    
    # Kirim datanya ke HTML dengan nama 'data_absen'
    return render_template('absen.html', data_absen=data_absen_lengkap)

# Route khusus untuk menghapus data.
@app.route('/hapus/<int:id_tugas>')
def hapus_tugas(id_tugas):
    
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    # Buka brankas
    conn = get_db_connection()
    
    # Perintahkan SQL untuk menghapus baris yang ID-nya cocok dengan yang diklik
    conn.execute('DELETE FROM tugas WHERE id = ?', (id_tugas,))
    
    # Kunci brankas dan tutup
    conn.commit()
    conn.close()
    
    # Refresh kembali ke halaman tugas
    return redirect(url_for('halaman_tugas'))

# Route untuk Edit Tugas. Karena butuh menampilkan form (GET) dan menyimpan form (POST)
@app.route('/edit/<int:id_tugas>', methods=['GET', 'POST'])
def edit_tugas(id_tugas):
    
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    
    # Jika user menekan tombol "Simpan Perubahan" di formulir (POST)
    if request.method == 'POST':
        matkul_edit = request.form['matkul']
        deskripsi_edit = request.form['deskripsi']
        deadline_edit = request.form['deadline']
        status_edit = request.form['status']
        
        # Perinta SQL UPDATE untuk menimpa data lama dengan data baru, khusus untuk ID yang sedang dibuat
        conn.execute('''
            UPDATE tugas
            SET matkul = ?, deskripsi = ?, deadline = ?, status = ?
            WHERE id = ?
        ''', (matkul_edit, deskripsi_edit, deadline_edit, status_edit))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('halaman_tugas'))
    
    # Jika user baru menekan tombol 'edit' warna kuning di tabel(GET)
    tugas_lama = conn.execute('SELECT * FROM tugas WHERE id = ?', (id_tugas,)).fetchone()
    conn.close()
    
    # Buka halaman edit_tugas.html dan kirimkan data lamanya
    return render_template('edit_tugas.html', tugas=tugas_lama)

# Route khusus untuk tombol +1 Hadir
@app.route('/tambah_absen/<int:id_absen>')
def tambah_absen_matkul(id_absen):
    
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Cek dulu data saat ini
    absen_saat_ini = conn.execute('SELECT hadir, total_pertemuan FROM absen WHERE id = ?', (id_absen,)).fetchone()
    
    # Logika pencegahan: Jangan sampai kehadiran melebihi total pertemuan (misal mentok di 14/14)
    if absen_saat_ini['hadir'] < absen_saat_ini['total_pertemuan']:
        # kalau masih masuk akal, tambahkan 1 ke kolom 'hadir' menggunakan SQL UPDATE
        conn.execute('UPDATE absen SET hadir = hadir + 1 WHERE id =  ?', (id_absen,))
        conn.commit()
    
    conn.close()
    
    # Refresh kembali ke halaman absen
    return redirect(url_for('halaman_absen'))

# Route khusus untuk menghapus mata kuliah dari daftar absen
@app.route('/hapus_absen/<int:id_absen>')
def hapus_absen(id_absen):
    
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    
    # buka brankas
    conn = get_db_connection()
    
    # Hapus baris di tabel absen yang ID-nya cocok
    conn.execute('DELETE FROM absen WHERE id = ?', (id_absen,))
    
    # kunci brankas dan tutup
    conn.commit()
    conn.close()
    
    # Refresh halaman absen
    return redirect(url_for('halaman_absen'))
        

# Perintah untuk menjalankan server lokal
if __name__ == "__main__":
    app.run(debug=True)