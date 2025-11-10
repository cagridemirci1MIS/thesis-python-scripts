# Gerekli kütüphaneler
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Excel dosyanın yolunu belirt
file_path = "31_satir_veriseti_.xlsx"  # aynı klasördeyse sadece dosya adı yeterli

# Veri setini oku
df = pd.read_excel(file_path)

# Tüm İngilizce kelimeleri birleştir
english_words_text = " ".join(df["İngilizce Kelimeler"].astype(str).tolist())

# Word Cloud oluştur
wordcloud = WordCloud(
    width=1200,
    height=700,
    background_color="white",
    colormap="viridis",
    font_path="C:/Windows/Fonts/arial.ttf"  # Windows kullanıcıları için
    # Mac için: "/Library/Fonts/Arial.ttf"
    # Linux için: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
).generate(english_words_text)

# Görselleştir
plt.figure(figsize=(14, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Verisetindeki İngilizce Kelimeler Word Cloud", fontsize=16)
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Excel dosyanın yolu
file_path = "31_satir_veriseti_.xlsx"

# Veri setini oku
df = pd.read_excel(file_path)

# İngilizce kelimeleri temizleyip birleştir
all_words = []
for cell in df["İngilizce Kelimeler"]:
    if isinstance(cell, str):
        words = [w.strip().lower() for w in cell.replace(",", " ").split() if w.strip()]
        all_words.extend(words)

# En sık geçen 31 kelimeyi bul
word_counts = Counter(all_words)
top_words = word_counts.most_common(31)

# DataFrame'e çevir
freq_df = pd.DataFrame(top_words, columns=["Kelime", "Frekans"])

# Grafik
plt.figure(figsize=(12, 6))
plt.barh(freq_df["Kelime"], freq_df["Frekans"], color="skyblue")
plt.gca().invert_yaxis()  # En sık kelimeler yukarıda gözüksün
plt.title("En Sık Geçen 31 İngilizce Kelime", fontsize=16)
plt.xlabel("Frekans")
plt.ylabel("Kelime")
plt.tight_layout()
plt.show()
