# Satu IPM, Banyak Wajah
Visualisasi interaktif multivariat (PCA, parallel coordinates, heatmap), geospasial (koroplet + simbol proporsional), dan hierarkis (treemap, sunburst) profil pembangunan manusia 514 kab/kota.

- **Demo:** (isi URL GitHub Pages)
- **Sumber data:** BPS (UHH, HLS, RLS, pengeluaran per kapita disesuaikan, P0, P1, TPT, sanitasi layak, air minum layak, IPM, jumlah penduduk). Isi judul tabel, tahun, URL, dan tanggal akses di bawah. Batas wilayah: shapefile kab/kota (non-BPS), isi sumbernya.
- **Struktur:** `index.html` (halaman), `clean_and_analyze.py` (pembersihan, PCA, klaster), `data/raw` (data mentah), `data/processed` (hasil olahan), `data/geo` (GeoJSON).
- **Reproduksi:** `pip install pandas geopandas scikit-learn openpyxl` lalu `python clean_and_analyze.py`.
- **Deklarasi alat bantu AI:** isi (AI dipakai sebagai alat bantu pengolahan dan penulisan kode; penulis bertanggung jawab atas isi).

## Tabel sumber data
| Variabel | Judul tabel (isi persis seperti di BPS) | Tahun | URL | Tanggal akses |
|---|---|---|---|---|
| Umur Harapan Hidup | | 2024 | | |
| Harapan Lama Sekolah | | 2024 | | |
| Rata-rata Lama Sekolah | | 2024 | | |
| Pengeluaran per Kapita Disesuaikan | | 2024 | | |
| Persentase Penduduk Miskin (P0) | | 2024 | | |
| Indeks Kedalaman Kemiskinan (P1) | | 2024 | | |
| TPT | | 2024 | | |
| Sanitasi Layak | | 2024 | | |
| Air Minum Layak | | 2024 | | |
| IPM | | 2024 | | |
| Jumlah Penduduk | | 2024 | | |

**Batas wilayah (data pendukung non-BPS):** shapefile kab/kota `SHP_KabKota_Indonesia_Baru514`, disediakan oleh dosen (Dr. Rindang Bangun Prasetyo, S.S.T., M.Si.), diterima pada tahun 2024. Sumber asli data tidak diketahui secara pasti; atribut file menunjukkan turunan dari data batas desa/kelurahan (TASWIL), yang diagregasi menjadi 514 kab/kota.
