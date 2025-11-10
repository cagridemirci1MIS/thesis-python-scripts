# ==============================================
# YouTube Code-Mixing + Engagement Data Merge (Final)
# ==============================================

import pandas as pd
import numpy as np

# ✅ Dosya yolları
P_TRANSCRIPT = r"D:\TEZ\veriseti + analiz\31_satir_veriseti__with_detect.xlsx"
P_ENGAGEMENT = r"D:\TEZ\veriseti + analiz\youtube_engagement_rates.xlsx"
OUT_PATH = r"D:\TEZ\veriseti + analiz\codemix_er_merged_full.v2.xlsx"

# 1️⃣ Veri setlerini oku
print("📂 Dosyalar okunuyor...")
trans = pd.read_excel(P_TRANSCRIPT)
eng = pd.read_excel(P_ENGAGEMENT)

print("Transkript shape:", trans.shape)
print("Engagement shape:", eng.shape)

# 2️⃣ Sütun adlarını normalize et
trans.columns = [c.strip().lower() for c in trans.columns]
eng.columns = [c.strip().lower() for c in eng.columns]

# 3️⃣ Video kimliği sütunlarını bul
vcol_trans = [c for c in trans.columns if "video" in c and "id" in c]
vcol_eng = [c for c in eng.columns if "video" in c and "id" in c]

video_col_trans = vcol_trans[0] if vcol_trans else trans.columns[0]
video_col_eng = vcol_eng[0] if vcol_eng else eng.columns[0]

print(f"🎬 Eşleştirme sütunları: {video_col_trans} ↔ {video_col_eng}")

# 4️⃣ Birleştirme
df = pd.merge(trans, eng, left_on=video_col_trans, right_on=video_col_eng, how="inner", suffixes=("_tr","_eng"))
print(f"✅ Birleştirildi: {df.shape[0]} satır, {df.shape[1]} sütun")

# 5️⃣ Gereksiz sütunları sil (boş, duplicate, unnamed)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.loc[:, df.columns.notna()]

# 6️⃣ Sayısal sütunları dönüştür (virgül → nokta)
for c in df.columns:
    if df[c].dtype == object:
        try:
            df[c] = df[c].str.replace(",", ".").astype(float)
        except Exception:
            continue

# 7️⃣ Eksik değer raporu
print("\n📊 Eksik değer sayıları (ilk 10):")
print(df.isna().sum().sort_values(ascending=False).head(10))

# 8️⃣ Boşlukları temizle
df.columns = df.columns.str.strip()

# 9️⃣ Sayısal özet
print("\n📈 Sayısal kolon istatistikleri:")
print(df.describe().round(2))

# 🔟 Çıkışı kaydet
df.to_excel(OUT_PATH, index=False)
print(f"\n🎉 Dosya kaydedildi: {OUT_PATH}")
