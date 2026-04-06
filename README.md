# 🎓 Portal Ihsan - Asisten Manajemen Kuliah

Portal Ihsan adalah aplikasi berbasis web yang dirancang khusus sebagai asisten pribadi untuk memanajemen kehidupan perkuliahan. Aplikasi ini membantu melacak jadwal kuliah, memanajemen tugas, hingga menghitung persentase kehadiran secara otomatis.

## ✨ Fitur Utama
- **🔒 Sistem Keamanan:** Dilengkapi fitur Login/Logout dengan Flask Session untuk menjaga privasi data.
- **📅 Jadwal Kuliah Cerdas:** Menampilkan jadwal dalam format kartu (Grid Card) yang otomatis menyorot (menjadi hijau) mata kuliah pada hari ini secara *real-time*. Dilengkapi fitur penambahan jadwal via *Pop-up Modal*.
- **📝 Manajemen Tugas:** Sistem CRUD untuk mencatat tugas, batas waktu (deadline), dan status pengerjaan yang responsif di perangkat *mobile*.
- **✅ Tracker Kehadiran:** Menghitung dan memvisualisasikan persentase kehadiran (*progress bar*) secara otomatis berdasarkan total pertemuan, lengkap dengan sistem validasi pencegah data ganda.

## 🛠️ Teknologi yang Digunakan
- **Backend:** Python 3, Flask Framework
- **Database:** SQLite
- **Frontend:** HTML5, Bootstrap 5, Jinja2 Templating
- **Deployment:** PythonAnywhere