# 🛒 Tokopedia Scraper

Script Python untuk **mengambil data produk Tokopedia** berdasarkan kata kunci pencarian.  
Menggunakan **Playwright (Chromium)** untuk menampilkan halaman dinamis dan **BeautifulSoup** untuk mengekstrak data seperti nama produk, harga, toko, lokasi, rating, dan jumlah terjual.

> ⚠️ Gunakan hanya untuk keperluan edukasi, riset, atau eksperimen pribadi.  
> Harap patuhi [Terms of Service Tokopedia](https://www.tokopedia.com/terms) dan `robots.txt`.

---

## ✨ Fitur

- ✅ Render halaman dinamis menggunakan **Playwright**
- ✅ Auto-scroll & auto-click tombol **“Muat Lebih Banyak”**
- ✅ Parsing aman dengan **BeautifulSoup**
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

Contoh: scraping produk dengan kata kunci *laptop gaming* dan klik tombol “Muat Lebih Banyak” hingga 10 kali.

```bash
python scrape_tokopedia.py --query "laptop gaming" --clicks 10 --headless
```

### Parameter

| Argumen | Keterangan | Default |
|----------|-------------|----------|
| `--query` / `-q` | Kata kunci pencarian | (wajib) |
| `--clicks` / `-c` | Jumlah klik tombol **“Muat Lebih Banyak”** | 25 |
| `--headless` | Jalankan browser tanpa tampilan GUI | opsional |

---

## 📄 Hasil Output

Setelah scraping selesai, file hasil akan tersimpan di folder `output/`:
```
output/
 ├─ tokopedia_laptop+gaming_1761500000.csv
 └─ tokopedia_laptop+gaming_1761500000.json
```

Contoh isi file CSV:
```csv
name,price,shop,location,rating,sold,link
ASUS ROG Zephyrus G14, Rp24.999.000, ASUS Official Store, Jakarta Pusat, 4.9, 27 terjual, https://www.tokopedia.com/asus-official/...
Lenovo LOQ 15IRH8, Rp15.499.000, Lenovo Legion, Jakarta Barat, 4.8, 15 terjual, https://www.tokopedia.com/lenovo-legion/...
```

---

## 🧠 Cara Kerja

1. Playwright membuka hasil pencarian Tokopedia berdasarkan kata kunci.
2. Script melakukan **scroll otomatis** ke bagian bawah halaman.
3. Jika tombol **“Muat Lebih Banyak”** muncul, script akan menekannya berulang kali.
4. Setelah semua produk dimuat, **BeautifulSoup** membaca HTML hasil render.
5. Produk diambil dari elemen `<div class="css-5wh65g">` dan diproses:
   - Nama produk dari tag `<span>`
   - Harga dari teks `Rp...`
   - Nama toko dan lokasi dari elemen bawah
   - Rating dan jumlah terjual (jika tersedia)
6. Data disimpan dalam format `.csv` dan `.json`.

---

## 🧰 Tips Penggunaan

- Gunakan kata kunci spesifik agar hasil lebih relevan.  
  Contoh:
  ```bash
  python scrape_tokopedia.py -q "mouse logitech wireless"
  ```
- Jalankan dengan `--headless` jika tidak perlu melihat tampilan browser.
- Hindari scraping terus-menerus tanpa delay (agar tidak dianggap bot).
- Jika hasil kosong, periksa apakah class `css-5wh65g` berubah di DOM terbaru Tokopedia.
- Gunakan opsi `--clicks` untuk menyesuaikan jumlah produk yang dimuat.

---

## 🧾 Troubleshooting

| Masalah | Penyebab | Solusi |
|----------|-----------|--------|
| `Executable doesn’t exist` | Browser Playwright belum di-install | Jalankan `python -m playwright install chromium` |
| `Jumlah item ditemukan: 0` | Halaman belum termuat penuh / tombol belum diklik | Coba tanpa `--headless` untuk lihat progres |
| `Malformed class selector` | Struktur DOM berubah | Update fungsi `fallback_parse_cards` |
| `Gagal klik tombol` | Tombol “Muat Lebih Banyak” belum muncul di viewport | Tambah delay atau scroll otomatis |

---

## 🔒 Etika & Batasan

- Gunakan secara wajar (tidak spam request).
- Jangan mendistribusikan data hasil scraping.
- Gunakan **API resmi Tokopedia** jika memerlukan data massal atau real-time.

---

## 📜 Lisensi

MIT License © 2025 — dibuat untuk pembelajaran pribadi.  
Semua merek dagang dan data adalah milik Tokopedia.

---

## 💡 Pengembangan Selanjutnya

- [ ] Export hasil ke Google Sheets
- [ ] Integrasi database SQLite / PostgreSQL
- [ ] Dashboard analisis harga (Streamlit / Dash)
- [ ] Penjadwalan otomatis (cronjob)
- [ ] Support kategori spesifik (elektronik, fashion, dsb.)

---

> Ditulis oleh **Biachan (biachan3)**  
> ✉️ GitHub: [https://github.com/biachan3](https://github.com/biachan3)
