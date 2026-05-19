# Fungsi untuk tugas kecil dan umum

import datetime as dt

def get_today():
    '''Fungsi Helper - tanggal hari ini ke string'''
    return dt.date.today().strftime("%d/%m/%Y")
