

                                   ----- Personal Menager Task APP -----

    Aplikasi ini dibuat pada 20 April 2026 dengan tujuan untuk menguji pemahaman developer tentang python dan OOP dasar.
    Pembuatan aplikasi ini juga memperhatikan hal" utama seperti UI, validasi input user, logic, dan file handling .
    kedepeannya bisa lebih berkembang lagi untuk developer dan semoga aplikasi ini bisa membantu mereka yang membutuhkan.


-> berikut adalah beberapa penjelasan dan lain halnya

# config
    |- contants.py -> tempat konstanta (scalebel dan mudah di update)
    |- setting.py -> tempat format nama file dan format lainnya

# models
    |- task.py -> model / set atribut data dari task

# services
    |- task_menager.py -> semua logic mulai dari view task - filter&sortw

# storages
    |- json_storage.py -> file_handling untuk json , format dict ke file json

# UI
    |- cli.py -> Bagian yang berhubungan langsung dengan user - menampilkan data dan input user

# Utils
    |- helper.py -> Kumpulan fungsi yang reuseble

# main -> Saat ingin menjalankan aplikasi, start dari main. tidak dapat start dari folder/file lainnya
                                                    
