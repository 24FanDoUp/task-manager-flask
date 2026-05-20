                                   ----- Task Manager Web App -----

Fitur:
- Register/Login
    jika belum punya akun web app ini sudah memiliki sistem auth register dan login, user baru hanya di minta memasukkan username, passwword dan confirm
    passsowrd.setelah mengisi akun akan otomatis terdaftar dan di arahkan ke halaman login. data user baru akan di simpan di database sqllite dengan tabel
    bernama users. Note: model data yang disimpan ke database dapat di lihat di database/models.py
- CRUD task
    Create - Tambah task. saat user login untuk pertama kalinya user akan diarahkan untuk membuat task pertama. untuk fitur tambah task juga ada di bagian
      nav bar "Add Task". user akan diminta mengisi form yang terdiri dari judul,deskripsi,kategori,prioritas dan deadline/due_date. setiap form dilengkapi
      dengan required jadi membuatnya wajib di isi. setelah semua di isi dan berhasil menbah task baru, data akan di simpan di database sqlite dengan nama
      tabel "tasks"
    Read - Lihat task. setelah user beerhasil menambahkan task pertama, user akan di arahkan ke halaman "My Task". halaman ini berisi semua task milik
      user, karena sudah dilengkapi dengan login_required dan owner_required user hanya bisa melihat dan mengedit task miliknya sendiri.
    Update - Edit task. fitur ini ada di setiap task yang dimiliki user. user akan diarahkan ke halaman edit yang berisikan form pengeditan yang sudah
      terisi sesuai dengan task sebelumnya. jika user ingin membatalkan pengeditan task, terdapat tombol untuk batalkan. begitu juga tombol simpan
      perubahan.

- Search, filter, sort, pagination
    fitur ini agar mempermudah user dalam mengklasifikasikan tugas:
    Search : mencari task berdasarkan judul atau deskripsi.
    Filter : web app ini menyediakan filter berdasarkan kategory dan status tugas
    Sort : digunakan untuk mengurutkan task , sort yang disediakan adalah terbaru,terlama,deadline terdekat, dan prioritas tertinggi

- Role admin/user
    Web app ini juga dilengkapi dengan role admin dan user. untuk role dibedakan dengan menggunakan role_required, ini digunakan untuk memberikan batasan
    akses halaman yang bisa dibuka oleh user atau memerlukan role admin. contoh saja ada halaman admin dashboardl yang membutuhkan role admin untuk
    terlihat /masuk ke halaman. dalam halaman admin dashboard menampilkan total user & task, jumlah task panding/done secara keseluruhan dan menampilkan
    nama usernama serta berapa jumlah task yang mereka miliki. serta terdapat fitur untuk mengganti role user lain dan menghapus user.
- CSRF protection
    Pengamanan sederhana untuk request sejenis POST,PUT,DELETE yang meminta untuk mengubah data dalam database. mencegah supaya tidak ada pengiriman req
    POST diluar web app sendiri/ bisa dibilang sebagai validasi request POST milik web sendiri.
- Alembic migration
    digunakan ketika ingin menambahkan schema baru atau menambah kolom dalam suatu tabel yang tersimpan di database sqlite, selain menambah digunakann juga
    ketika mengubah jenis type dari schema yang sudah ada
- Responsive UI
    Web app task manager sudah menggunakan responsive UI yang dimana UI akan menyesuikan dnegan ukuran dan device yang dipakai oleh user.
    contoh: d desktop tambipilan card akan sejajar 3 dan di mobile card akan membetuk kolom panjang kebawah (sesuai jumlah task)

Tech stack:
- Python
- Flask
- SQLAlchemy
- Alembic
- HTML/CSS
- SQLite
