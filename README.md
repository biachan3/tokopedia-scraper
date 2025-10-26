🛒 Tokopedia Scraper (Updated 2025)

Proyek ini memungkinkan kamu mengambil data produk Tokopedia berdasarkan kata kunci pencarian — lengkap dengan nama produk, harga, toko, lokasi, dan tautan produk.
Menggunakan Playwright untuk merender halaman (karena Tokopedia memuat data dengan JavaScript) dan BeautifulSoup untuk parsing hasil.

⚠️ Catatan penting: Gunakan untuk kebutuhan pribadi, riset, atau edukasi. Jangan scraping secara masif tanpa izin resmi dari Tokopedia. Baca dan patuhi Terms of Service & robots.txt mereka.

✨ Fitur Utama

✅ Menggunakan Playwright (Chromium headless) untuk menampilkan halaman dinamis
✅ Mendukung scroll otomatis agar semua produk termuat
✅ Parsing cerdas dengan regex (tanpa tergantung class dinamis Tokopedia)
✅ Menyimpan hasil ke CSV & JSON
✅ Logging dan retry otomatis
✅ Modular — fungsi pembantu disimpan di utils.py

📁 Struktur Folder
tokopedia-scraper/
├─ scrape_tokopedia.py     # script utama
├─ utils.py                # helper umum (logging, delay, save, parsing)
├─ requirements.txt        # dependency
├─ README.md               # dokumentasi (file ini)
└─ output/                 # hasil scraping tersimpan di sini

⚙️ Instalasi
1️⃣ Clone proyek
git clone https://github.com/<username>/tokopedia-scraper.git
cd tokopedia-scraper

2️⃣ Buat virtual environment & install dependency
python -m venv venv
source venv/bin/activate     # mac/linux
venv\Scripts\activate        # windows

pip install -r requirements.txt

3️⃣ Install browser Playwright
python -m playwright install chromium

🚀 Cara Menjalankan

Contoh pencarian produk “laptop gaming” di 2 halaman pertama:

python scrape_tokopedia.py --query "laptop gaming" --pages 2 --headless


Parameter:

Argumen	Deskripsi	Default
--query atau -q	Kata kunci pencarian	(wajib diisi)
--pages atau -p	Jumlah halaman hasil pencarian	1
--headless	Menjalankan browser tanpa tampilan GUI	opsional
📄 Hasil Output

Setelah scraping selesai, file hasil akan otomatis tersimpan di folder output/:

output/
 ├─ tokopedia_laptop+gaming_1732784829.csv
 └─ tokopedia_laptop+gaming_1732784829.json


Contoh isi CSV:

name,price,shop,location,link
ASUS ROG Zephyrus G14 2025, Rp2.000.000, ALL STORE GZ, Jakarta Pusat, https://www.tokopedia.com/all-store-gz/...
Lenovo LOQ 15IAX9E, Rp11.489.000, Lenovo Legion Official, Jakarta Pusat, https://www.tokopedia.com/lenovolegion/...
HP Victus 15 RTX4050, Rp7.419.470, Toko TeknoKreasi, Jakarta Barat, https://www.tokopedia.com/toko-teknokreasi/...

🧠 Cara Kerja (Ringkas)

Playwright membuka hasil pencarian Tokopedia.

Script otomatis scroll ke bawah agar semua produk termuat.

BeautifulSoup mengambil data dari elemen <div class="css-5wh65g">.

Data produk diekstrak berdasarkan pola teks (Rp, nama toko, lokasi, dsb).

Semua data disimpan ke file .csv dan .json.

🧩 Fungsi-fungsi Utama
File	Fungsi	Penjelasan
scrape_tokopedia.py	scrape_query()	Mengatur alur scraping (Playwright + parsing + save)
	fallback_parse_cards()	Parsing elemen produk dengan regex aman
	save_results()	Menyimpan hasil ke file
utils.py	logger, retry, random_delay, save_csv, dll.	Fungsi pendukung reusable
🧰 Tips Penggunaan

Gunakan kata kunci spesifik, contoh:

python scrape_tokopedia.py -q "mouse wireless logitech"


Tambahkan jeda scraping agar tidak cepat terdeteksi bot (delay_range bisa diatur di kode).

Jika hasil kosong, buka file debug.html (bisa diaktifkan sementara di kode) untuk memeriksa struktur DOM terbaru.

Jika scraping dalam jumlah besar, gunakan proxy atau ganti user-agent secara berkala (sudah disiapkan di utils.py).

🧾 Troubleshooting
Masalah	Penyebab	Solusi
❌ “Executable doesn’t exist…”	Browser Playwright belum terinstal	Jalankan python -m playwright install chromium
⚠️ “Jumlah item ditemukan: 0”	Struktur DOM berubah / belum scroll	Pastikan auto-scroll aktif & update selector
🧱 “Malformed class selector”	Class mengandung karakter + / =	Sudah diperbaiki di versi terbaru (regex-safe)
🔒 Etika & Batasan Penggunaan

Jangan jalankan scraper terlalu sering (beri delay antar halaman).

Jangan distribusikan atau jual ulang data yang diambil.

Gunakan API resmi Tokopedia jika kamu butuh akses data besar atau realtime.

📜 Lisensi

Proyek ini bersifat open-source untuk keperluan belajar dan eksperimen pribadi.
Semua data dan merek dagang adalah milik Tokopedia.

💡 Contoh Pengembangan Lanjutan

Kamu bisa menambahkan fitur:

Export ke Google Sheets

Integrasi dengan SQLite / PostgreSQL

Scraping otomatis terjadwal (pakai cronjob)

Analisis harga dengan pandas