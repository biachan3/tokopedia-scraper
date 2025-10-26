# 🛒 Tokopedia Scraper

Script Python untuk **mengambil data produk Tokopedia** berdasarkan kata kunci pencarian.  
Menggunakan **Playwright (Chromium)** untuk menampilkan halaman dinamis dan **BeautifulSoup** untuk mengekstrak data seperti nama produk, harga, toko, lokasi, dan link produk.

> ⚠️ Gunakan hanya untuk keperluan edukasi, riset, atau eksperimen pribadi.  
> Harap patuhi [Terms of Service Tokopedia](https://www.tokopedia.com/terms) dan `robots.txt`.

---

## ✨ Fitur
- ✅ Render halaman dinamis menggunakan **Playwright**
- ✅ Auto-scroll agar semua produk termuat
- ✅ Parsing aman dengan **regex** (tidak bergantung pada class CSS acak Tokopedia)
- ✅ Retry otomatis jika gagal memuat halaman
- ✅ Menyimpan hasil ke **CSV** dan **JSON**
- ✅ Logging rapi + struktur kode modular

---

## 📁 Struktur Project
```
tokopedia-scraper/
├─ scrape_tokopedia.py      # script utama
├─ utils.py                 # helper (logging, save, delay, retry)
├─ requirements.txt         # daftar library
├─ README.md                # dokumentasi (file ini)
└─ output/                  # hasil scraping tersimpan di sini
```

---

## ⚙️ Instalasi

### 1️⃣ Clone repository
```bash
git clone https://github.com/biachan3/tokopedia-scraper.git
cd tokopedia-scraper
```

### 2️⃣ Buat virtual environment & install dependency
```bash
python -m venv venv
source venv/bin/activate   # mac / linux
venv\Scripts\activate      # windows

pip install -r requirements.txt
```

### 3️⃣ Install browser Playwright
```bash
python -m playwright install chromium
```

---

## 🚀 Cara Menjalankan

Contoh: scraping produk dengan kata kunci *laptop gaming* di 2 halaman hasil pencarian.
```bash
python scrape_tokopedia.py --query "laptop gaming" --pages 2 --headless
```

**Parameter:**

| Argumen | Keterangan | Default |
|----------|-------------|----------|
| `--query` / `-q` | Kata kunci pencarian | (wajib) |
| `--pages` / `-p` | Jumlah halaman pencarian yang ingin diambil | 1 |
| `--headless` | Jalankan browser tanpa tampilan GUI | opsional |

---

## 📄 Hasil Output

Setelah scraping selesai, file hasil akan tersimpan di folder `output/`:
```
output/
 ├─ tokopedia_laptop+gaming_1732778392.csv
 └─ tokopedia_laptop+gaming_1732778392.json
```

Contoh isi file CSV:
```csv
name,price,shop,location,link
ASUS ROG Zephyrus G14 2025, Rp2.000.000, ALL STORE GZ, Jakarta Pusat, https://www.tokopedia.com/all-store-gz/...
Lenovo LOQ 15IAX9E, Rp11.489.000, Lenovo Legion Official, Jakarta Pusat, https://www.tokopedia.com/lenovolegion/...
HP Victus 15 RTX4050, Rp7.419.470, Toko TeknoKreasi, Jakarta Barat, https://www.tokopedia.com/toko-teknokreasi/...
```

---

## 🧠 Cara Kerja
1. Playwright membuka hasil pencarian Tokopedia berdasarkan kata kunci.
2. Script melakukan **scroll otomatis** agar seluruh produk muncul di DOM.
3. BeautifulSoup membaca HTML hasil render.
4. Produk diambil dari elemen `<div class="css-5wh65g">` dan diproses:
   - Nama produk dari tag `<span>`
   - Harga dari teks `Rp...`
   - Nama toko dan lokasi dari bagian bawah kartu produk
5. Data disimpan dalam format `.csv` dan `.json`.

---

## 🧰 Tips Penggunaan
- Gunakan kata kunci spesifik agar hasil lebih relevan.  
  Contoh:
  ```bash
  python scrape_tokopedia.py -q "mouse logitech wireless"
  ```
- Jalankan headless jika ingin scraping tanpa tampilan browser.
- Hindari scraping terus-menerus tanpa delay (agar tidak dianggap bot).
- Cek file HTML hasil render (`debug.html`) jika parsing kosong — biasanya karena struktur DOM berubah.
- Untuk jumlah halaman besar, gunakan `--pages` dan tambahkan jeda di kode (delay range).

---

## 🧾 Troubleshooting

| Masalah | Penyebab | Solusi |
|----------|-----------|--------|
| `Executable doesn’t exist` | Browser Playwright belum di-install | Jalankan `python -m playwright install chromium` |
| `Jumlah item ditemukan: 0` | Halaman belum termuat penuh | Pastikan auto-scroll aktif |
| `Malformed class selector` | Class CSS Tokopedia berisi `+` atau `=` | Sudah diperbaiki di versi regex-safe |
| Hasil tidak lengkap | Struktur DOM berubah | Perbarui fungsi `fallback_parse_cards` |

---

## 🔒 Etika & Batasan
- Jangan mengirim request terlalu sering.
- Jangan mendistribusikan data hasil scraping.
- Gunakan **API resmi Tokopedia** jika membutuhkan data dalam jumlah besar atau real-time.

---

## 📜 Lisensi
MIT License © 2025 — dibuat untuk pembelajaran pribadi.  
Semua merek dagang dan data adalah milik Tokopedia.

---

## 💡 Pengembangan Selanjutnya
- [ ] Export hasil ke Google Sheets
- [ ] Integrasi database SQLite / PostgreSQL
- [ ] Dashboard analisis harga dengan Streamlit
- [ ] Penjadwalan otomatis (cronjob)

---

> Ditulis oleh **Biachan (biachan3)**  
> ✉️ GitHub: [https://github.com/biachan3](https://github.com/biachan3)
