# Satu IPM, Banyak Wajah

Visualisasi interaktif profil pembangunan manusia kabupaten/kota di Indonesia (data BPS tahun 2024). Proyek ini memuat tiga topik visualisasi: **multivariat** (PCA, heatmap, radar chart), **geospasial** (peta koroplet), dan **hierarkis** (treemap, sunburst).

- **Demo:**  https://mercycantik.github.io/UAS-VISDAT-222313205/ 
- **Cakupan data:** 514 kabupaten/kota. Empat kab/kota di Papua Pegunungan tidak diikutkan dalam PCA karena data sanitasi/air minum kosong (510 kab/kota dianalisis), dan delapan kab/kota tidak punya geometri pada shapefile sumber sehingga tidak tampil di peta.
- **Struktur:**
  - `index.html`: halaman visualisasi
  - `plotly.min.js`: pustaka Plotly (disimpan lokal)
  - `clean_and_analyze.py`: pembersihan data, PCA, dan klaster
  - `data/raw`: data mentah (Excel dan shapefile)
  - `data/processed`: data olahan dan bobot PCA
  - `data/geo`: GeoJSON batas kab/kota
- **Reproduksi:** `pip install pandas geopandas scikit-learn openpyxl`, lalu `python clean_and_analyze.py` dari akar repositori.

## Sumber data

Seluruh data utama bersumber dari BPS dan diperoleh melalui fitur Query Builder BPS. Judul tabel ditulis persis seperti di BPS.

| Variabel | Judul tabel | Tahun | URL | Tanggal akses |
|---|---|---|---|---|
| Umur Harapan Hidup | [Metode Baru] Umur Harapan Hidup Saat Lahir (UHH) | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Harapan Lama Sekolah | [Metode Baru] Harapan Lama Sekolah | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Rata-rata Lama Sekolah | [Metode Baru] Rata-rata Lama Sekolah | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Pengeluaran per Kapita Disesuaikan | [Metode Baru] Pengeluaran per Kapita Disesuaikan | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Persentase Penduduk Miskin (P0) | Persentase Penduduk Miskin (P0) Menurut Kabupaten/Kota | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Indeks Kedalaman Kemiskinan (P1) | Indeks Kedalaman Kemiskinan (P1) Menurut Kabupaten/Kota | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| TPT | Tingkat Pengangguran Terbuka menurut Jenis Kelamin dan Kabupaten/Kota (kategori yang dipakai: Jumlah) | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Sanitasi Layak | Persentase rumah tangga yang memiliki akses terhadap sanitasi layak menurut kabupaten/kota | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Air Minum Layak | Persentase Rumah Tangga yang Memiliki Akses terhadap Sumber Air Minum Layak menurut Kabupaten/Kota | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| IPM | [Metode Baru] Indeks Pembangunan Manusia (IPM) | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |
| Jumlah Penduduk | Jumlah Penduduk menurut Kabupaten/Kota dan Kelompok Umur (total seluruh kelompok umur: Total) | 2024 | https://www.bps.go.id/id/query-builder | 30 Sept 2026 |

**Batas wilayah (data pendukung non-BPS):** shapefile kab/kota `SHP_KabKota_Indonesia_Baru514`, disediakan oleh dosen (Dr. Rindang Bangun Prasetyo, S.S.T., M.Si.), diterima pada September 2026. Sumber asli data tidak diketahui secara pasti; atribut file menunjukkan turunan dari data batas desa/kelurahan (TASWIL) yang diagregasi menjadi 514 kab/kota. Geometri disederhanakan agar ringan untuk web.

## Pengolahan singkat

Tabel dari BPS digabung per kabupaten/kota, nama wilayah diseragamkan dengan shapefile, lalu kode wilayah (`KDPKAB`) dipakai sebagai kunci. Sembilan indikator distandarisasi (indikator P1 ditransformasi log1p) untuk PCA dan klaster k-means (k = 4). IPM dan jumlah penduduk tidak dimasukkan ke PCA.

## Deklarasi penggunaan alat bantu AI

Claude (Anthropic) digunakan sebagai alat bantu untuk merancang struktur proyek, menulis kode pengolahan data dan halaman visualisasi, serta memberi saran tampilan. Penulis memeriksa, menjalankan, dan menyesuaikan seluruh keluaran, dan bertanggung jawab penuh atas isi proyek ini.