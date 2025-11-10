# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrow

plt.figure(figsize=(11, 8))
ax = plt.gca()
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.axis("off")

def box(x, y, text, color="#EAF0F6", w=3.3, h=1.1, fontsize=10.5):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.4", ec="#0D47A1", fc=color, lw=1.4))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color="#0D1117", wrap=True)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrow(x1, y1, x2-x1, y2-y1,
                            width=0.02, head_width=0.25,
                            head_length=0.3, color="#0D47A1"))

# --- Katman 1 ---
box(4.3, 10.0, "Veri Kaynağı\n(YouTube API + Transkript)")
arrow(6, 10.0, 6, 9.1)

# --- Katman 2 ---
box(4.3, 8.4, "Veri Ön İşleme\n(Temizlik, Birleştirme, Eksik Doldurma)")
arrow(6, 8.4, 6, 7.4)

# --- Katman 3 ---
box(4.3, 6.8, "Dil Analizi (NLP)\n(Code-Mixing Tespiti)")
arrow(6, 6.8, 3.5, 5.9)
arrow(6, 6.8, 8.5, 5.9)

# --- Paralel Katmanlar ---
box(2.2, 5.2, "Code-Mixing Metrikleri\n(CMI, M-Index, I-Index, EN_Oran)")
box(7.5, 5.2, "Etkileşim Metrikleri\n(ER_View, ER_Subscriber)")
arrow(3.8, 5.2, 5.3, 4.3)
arrow(8.9, 5.2, 6.7, 4.3)

# --- Katman 4 ---
box(4.4, 3.7, "Modelleme\n(LR, SVM, XGBoost, mBERT)")
arrow(6, 3.7, 6, 2.8)

# --- Katman 5 ---
box(4.4, 2.1, "Performans Değerlendirme\n(MAE, RMSE, R², F1, AUPRC)")

# --- Başlık ---
plt.text(6, 11.2,
         "Şekil 5.0. Geliştirilmiş Veri İşleme Hattı (Pipeline) Diyagramı",
         ha="center", va="center", fontsize=12.5,
         fontweight="bold", color="#0D1117")

plt.tight_layout()
plt.savefig(r"D:\TEZ\veriseti + analiz\Pipeline_Diagram_Final.png",
            dpi=300, bbox_inches="tight")
plt.show()
