"""Pembersihan, penggabungan, PCA, dan klaster.
Jalankan dari akar repo:  python clean_and_analyze.py
Output: data/processed/profil_kabkota.csv, data/geo/kabkota.geojson, data/processed/pca_loadings.csv
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

RAW_XLSX = "data/raw/Data_Mentah_UAS.xlsx"
RAW_SHP = "data/raw/shp/SHP_KabKota_Indonesia_Baru514.shp"

RENAME = {
    "Kab/Kota": "nama_data", "UHH": "uhh", "HLS": "hls", "RLS": "rls",
    "Pengeluaran per Kapita Disesuaikan": "pengeluaran",
    "Persentase Penduduk Miskin (P0)": "miskin_p0",
    "Indeks Kedalaman Kemiskinan (P1)": "kedalaman_p1",
    "TPT": "tpt", "Sanitasi Layak": "sanitasi", "Air Minum Layak": "air_minum",
    "IPM": "ipm", "Jumlah Penduduk": "penduduk",
}
PCA_VARS = ["uhh", "hls", "rls", "pengeluaran", "miskin_p0",
            "kedalaman_p1", "tpt", "sanitasi", "air_minum"]

# nama di file data -> nama di shapefile (penulisan berbeda)
NAME_MAP = {
    "Banyu Asin": "Banyuasin", "Batang Hari": "Batanghari", "Fakfak": "Fak Fak",
    "Gunung Kidul": "Gunungkidul", "Kep. Seribu": "Administrasi Kepulauan Seribu",
    "Kota Banjar Baru": "Kota Banjarbaru", "Kota Baubau": "Kota Bau Bau",
    "Kota Jakarta Barat": "Kota Administrasi Jakarta Barat",
    "Kota Jakarta Pusat": "Kota Administrasi Jakarta Pusat",
    "Kota Jakarta Selatan": "Kota Administrasi Jakarta Selatan",
    "Kota Jakarta Timur": "Kota Administrasi Jakarta Timur",
    "Kota Jakarta Utara": "Kota Administrasi Jakarta Utara",
    "Kota Lubuklinggau": "Kota Lubuk Linggau", "Kota Makasar": "Kota Makassar",
    "Kota Padangsidimpuan": "Kota Padang Sidempuan",
    "Kota Palangka Raya": "Kota Palangkaraya", "Kota Parepare": "Kota Pare Pare",
    "Kota Pematang Siantar": "Kota Pematangsiantar", "Kota Sawah Lunto": "Kota Sawahlunto",
    "Labuhan Batu": "Labuhanbatu", "Labuhan Batu Selatan": "Labuhanbatu Selatan",
    "Labuhan Batu Utara": "Labuhanbatu Utara",
    "Maluku Tenggara Barat / Kepulauan Tanimbar": "Kepulauan Tanimbar",
    "Mamuju Utara / Pasangkayu": "Pasangkayu", "Mukomuko": "Muko Muko",
    "Pangkajene dan Kepulauan": "Pangkajene Kepulauan",
    "Siau Tagulandang Biaro": "Kepulauan Siau Tagulandang Biaro",
    "Toba Samosir / Toba": "Toba", "Tojo Una-Una": "Tojo Una Una",
    "Toli-Toli": "Toli Toli", "Tulangbawang": "Tulang Bawang",
}
# Natuna tidak ada di shapefile; kode & provinsi diisi manual (kode BPS/Kemendagri 21.03)
MANUAL = {"Natuna": {"kode_wilayah": "21.03", "provinsi": "Kepulauan Riau"}}

PULAU = {
    "Sumatera": ["Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi", "Sumatera Selatan",
                 "Bengkulu", "Lampung", "Kepulauan Bangka Belitung", "Kepulauan Riau"],
    "Jawa": ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Daerah Istimewa Yogyakarta",
             "Jawa Timur", "Banten"],
    "Bali & Nusa Tenggara": ["Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur"],
    "Kalimantan": ["Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan",
                   "Kalimantan Timur", "Kalimantan Utara"],
    "Sulawesi": ["Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara",
                 "Gorontalo", "Sulawesi Barat"],
    "Maluku": ["Maluku", "Maluku Utara"],
    "Papua": ["Papua", "Papua Barat", "Papua Barat Daya", "Papua Selatan",
              "Papua Tengah", "Papua Pegunungan"],
}
PROV2PULAU = {p: k for k, v in PULAU.items() for p in v}


def main():
    # 1. data BPS
    df = pd.read_excel(RAW_XLSX).rename(columns=RENAME)
    for c in df.columns[1:]:
        df[c] = pd.to_numeric(df[c].astype(str).str.strip().replace({"-": np.nan, "nan": np.nan}).str.replace(",", "."), errors="coerce")
    df["nama_shp"] = df["nama_data"].replace(NAME_MAP)

    # 2. shapefile: buang baris gabungan rusak, simpan kolom perlu saja
    g = gpd.read_file(RAW_SHP)
    g = g[g["KDPKAB"].str.len() == 5].copy()
    g = g.rename(columns={"KDPKAB": "kode_wilayah", "WADMKK": "nama_shp", "WADMPR": "provinsi"})
    g = g[["kode_wilayah", "nama_shp", "provinsi", "geometry"]]

    # 3. gabung lewat nama (sekali), simpan kode_wilayah sebagai kunci tetap
    m = df.merge(g.drop(columns="geometry"), on="nama_shp", how="left", validate="1:1")
    for nama, v in MANUAL.items():
        i = m["nama_data"] == nama
        for k, val in v.items():
            m.loc[i, k] = val
    assert m["kode_wilayah"].notna().all(), m[m["kode_wilayah"].isna()]["nama_data"].tolist()
    assert m["kode_wilayah"].is_unique
    m["pulau"] = m["provinsi"].map(PROV2PULAU)
    assert m["pulau"].notna().all(), m[m["pulau"].isna()]["provinsi"].unique()
    m["nama_wilayah"] = m["nama_data"]
    m["ada_geometri"] = m["kode_wilayah"].isin(g.loc[g.geometry.notna(), "kode_wilayah"])
    m["lengkap_pca"] = m[PCA_VARS].notna().all(axis=1)

    # 4. PCA + klaster (hanya baris lengkap)
    X = m.loc[m.lengkap_pca, PCA_VARS].copy()
    X["kedalaman_p1"] = np.log1p(X["kedalaman_p1"])   # P1 sangat miring ke kanan
    Z = StandardScaler().fit_transform(X)
    pca = PCA().fit(Z)
    sc = pca.transform(Z)
    m.loc[m.lengkap_pca, ["pc1", "pc2", "pc3"]] = sc[:, :3]
    load = pd.DataFrame(pca.components_[:3].T, index=PCA_VARS, columns=["PC1", "PC2", "PC3"])
    load.loc["varian_dijelaskan"] = pca.explained_variance_ratio_[:3]

    sil = {}
    for k in range(2, 8):
        lab = KMeans(k, n_init=20, random_state=42).fit_predict(Z)
        sil[k] = silhouette_score(Z, lab)
    K = 4
    km = KMeans(K, n_init=20, random_state=42).fit(Z)
    # urutkan label klaster berdasar rata-rata PC1 (klaster 1 = PC1 terendah)
    order = pd.Series(sc[:, 0]).groupby(km.labels_).mean().sort_values().index
    remap = {old: new + 1 for new, old in enumerate(order)}
    m.loc[m.lengkap_pca, "klaster"] = [remap[l] for l in km.labels_]

    # 5. simpan
    cols = ["kode_wilayah", "nama_wilayah", "provinsi", "pulau"] + PCA_VARS + \
           ["ipm", "penduduk", "pc1", "pc2", "pc3", "klaster", "ada_geometri", "lengkap_pca"]
    m[cols].sort_values("kode_wilayah").to_csv("data/processed/profil_kabkota.csv", index=False)
    load.to_csv("data/processed/pca_loadings.csv")

    gg = g[g.geometry.notna()].copy()
    gg["geometry"] = gg.geometry.make_valid()
    gg["geometry"] = gg.geometry.simplify(0.003, preserve_topology=True)
    gg = gg[["kode_wilayah", "geometry"]]
    gg.to_file("data/geo/kabkota.geojson", driver="GeoJSON")

    print("baris data:", len(m), "| lengkap utk PCA:", int(m.lengkap_pca.sum()),
          "| punya geometri:", int(m.ada_geometri.sum()))
    print("varian PC1-PC3:", np.round(pca.explained_variance_ratio_[:3], 3),
          "kumulatif 3 PC:", round(pca.explained_variance_ratio_[:3].sum(), 3))
    print("silhouette per k:", {k: round(v, 3) for k, v in sil.items()})
    print(load[["PC1", "PC2", "PC3"]].round(2).to_string())
    print(m.groupby("klaster")[PCA_VARS + ["ipm"]].mean().round(1).to_string())
    print(m.groupby("klaster").size().to_dict())
    print("tanpa geometri:", m.loc[~m.ada_geometri, "nama_wilayah"].tolist())
    print("tidak lengkap PCA:", m.loc[~m.lengkap_pca, "nama_wilayah"].tolist())


if __name__ == "__main__":
    main()
