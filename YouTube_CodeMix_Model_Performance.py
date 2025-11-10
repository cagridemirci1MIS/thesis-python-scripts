# ==============================================
# CodeMix + ER Model Performans Analizi (Final)
#  - Regresyon: ER_View_% , ER_Subscriber_%
#  - Sınıflandırma: High/Low (ER_View_% medyan eşiği)
#  - 5-fold GroupKFold (kanal bazında)
#  - Çıktılar: Model_Performance_Results.xlsx, Confusion_Matrix.png, ROC_Curve.png
# ==============================================

import os, re, json, ast, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, LinearSVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor, XGBClassifier

from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    average_precision_score, precision_recall_curve, roc_curve, auc,
    confusion_matrix
)

# -------------------------------
# 0) Yol ayarları
# -------------------------------
BASE = r"D:\TEZ\veriseti + analiz"
DATA_PATH = os.path.join(BASE, "codemix_er_merged_full.v2.xlsx")
OUT_XLSX  = os.path.join(BASE, "Model_Performance_Results.xlsx")
FIG_CM    = os.path.join(BASE, "Confusion_Matrix.png")
FIG_ROC   = os.path.join(BASE, "ROC_Curve.png")

# -------------------------------
# 1) Veri setini yükle
# -------------------------------
df = pd.read_excel(DATA_PATH)
df.columns = [c.strip().lower() for c in df.columns]

# Zorunlu kolon isimlerini (olası ad varyasyonlarıyla) çöz
def pick(cols, candidates):
    cols_map = {c.lower(): c for c in cols}
    for cand in candidates:
        c = cand.lower()
        # birebir veya 'içerir' eşleşmesi
        if c in cols_map: return cols_map[c]
        for col in cols:
            if c in col.lower():
                return col
    return None

col_video   = pick(df.columns, ["video_id","id","video"])
col_channel = pick(df.columns, ["channel_id","channel","channel_title"])
col_text    = pick(df.columns, ["transcript","transkript","text"])
col_views   = pick(df.columns, ["views","izlenme"])
col_likes   = pick(df.columns, ["likes","begeni","beğeni"])
col_comments= pick(df.columns, ["comments","yorum"])
col_subs    = pick(df.columns, ["subscribers","aboneler","abone"])
col_er_view = pick(df.columns, ["er_view_%","er view %","er_view"])
col_er_sub  = pick(df.columns, ["er_subscriber_%","er subscriber %","er_subscriber"])

missing_crit = [col_video, col_text, col_views, col_likes, col_comments, col_subs, col_er_view, col_er_sub]
if any(c is None for c in missing_crit):
    raise RuntimeError("Gerekli kolonlardan bazıları bulunamadı. Lütfen dosyayı kontrol edin.")

# -------------------------------
# 2) Metinden code-mixing özellikleri (suffix-aware basit sezgisel)
# -------------------------------
TOKEN_RE = re.compile(r"[A-Za-zçğıöşüÇĞİÖŞÜ’']+", re.UNICODE)
TR_SUFFIX_CHARS = re.compile(r"^[a-zçğıöşü]+$", re.IGNORECASE)

EN_SLANG = {
    "afk","gg","fps","rpg","mmo","mmorpg","dlc","ui","ux","hud","npc","op","xp","hp","mp",
    "ban","banned","unban","spam","stream","streamer","like","comment","subscribe","discord",
    "server","mod","admin","premium","season","battlepass","update","patch","bug","crash","lag",
    "ping","rank","ranked","game","games","gameplay","quest","boss","inventory","loot","craft",
    "grind","speedrun","shader","asset","hitbox","cooldown","multiplayer","singleplayer",
    "keyboard","dialog","cutscene","publisher","developer","graphics","story","level","feature",
    "noob","pro","strat","clickbait","follow","raid","valorant","csgo","lol","pubg","gta","minecraft"
}
SHORT_OK = {"afk","gg","ui","ux","op","xp","hp","mp","dlc","rpg","fps"}
VOWELS = set("aeiou")
SUFFIXES = ("ing","ed","er","est","ly","tion","sion","ment","ness","less","able","ible","al","ous","ize","ise","ity","ial","ic","ive","ful")
BIGRAMS = ("th","ch","sh","qu","ph","wh","ck")

TR_SUFFIX_STARTS = (
    "la","le","yor","yorum","yorsun","yoruz","yorsunuz","yorlar",
    "ladım","ledi","ladık","ledik","ladınız","lediniz","ladılar","lediler",
    "layacak","leyecek","layacağım","leyeceğim",
    "lar","ler","lık","lik","luk","lük","cı","ci","cu","cü",
    "sız","siz","suz","süz","da","de","ta","te","dan","den","tan","ten",
    "yı","yi","yu","yü","yla","yle",
    "ım","im","um","üm","ın","in","un","ün","ımız","imiz","umuz","ümüz",
    "sın","sin","sun","sün","ız","iz","uz","üz","sınız","siniz","sunuz","sünüz",
)

def english_shape_or_slang(t: str) -> bool:
    tl = t.lower()
    if tl in EN_SLANG or tl in SHORT_OK: return True
    if len(tl) >= 3 and (set(tl) & VOWELS) and (
        any(tl.endswith(s) for s in SUFFIXES) or any(b in tl for b in BIGRAMS)
    ):
        return True
    return False

def detect_english_root_with_tr_suffix(token: str):
    t = token.strip()
    if len(t) < 3: return None
    m = re.match(r"^([A-Za-z]{3,})([A-Za-zçğıöşüÇĞİÖŞÜ’']*)$", t)
    if not m: return None
    root, rest = m.groups()
    if not rest: return None
    rest_l = rest.lower().replace("’","").replace("'","")
    if not rest_l: return None
    if not TR_SUFFIX_CHARS.fullmatch(rest_l): return None
    if not any(rest_l.startswith(p) for p in TR_SUFFIX_STARTS): return None
    root_l = root.lower()
    return root_l if english_shape_or_slang(root_l) else None

def english_flag(token: str) -> int:
    # TR ekli İngilizce kök?
    r = detect_english_root_with_tr_suffix(token)
    if r: return 1
    # Tamamen ASCII İngilizce?
    if re.fullmatch(r"[A-Za-z]+", token or ""):
        tl = token.lower()
        if len(tl) < 3 and tl not in SHORT_OK: return 0
        return 1 if english_shape_or_slang(tl) else 0
    return 0

def tokens_of(text: str):
    return TOKEN_RE.findall(text.lower()) if isinstance(text, str) else []

def compute_cm_metrics(text: str):
    toks = tokens_of(text)
    if not toks: 
        return 0, 0, 0.0, 0.0, 0.0
    flags = [english_flag(t) for t in toks]
    en = int(sum(flags))
    tr = len(toks) - en
    tot = len(toks)
    en_ratio = en / tot
    # CMI: TR (matris dil) dışı oran ~ en/tot
    cmi = en / tot
    # M-index: 1 - (p_en^2 + p_tr^2)
    p_en, p_tr = (en/tot), (tr/tot)
    m_index = 1.0 - (p_en**2 + p_tr**2)
    # I-index: dil geçiş oranı
    switches = sum(1 for i in range(1, tot) if flags[i] != flags[i-1])
    i_index = switches / (tot - 1) if tot > 1 else 0.0
    return tot, en, en_ratio, m_index, i_index

# Code-mixing özniteliklerini hesapla
cm_feats = df[col_text].apply(lambda x: compute_cm_metrics(x))
df["tokens"], df["en_tokens"], df["en_oran"], df["m_index"], df["i_index"] = zip(*cm_feats)
df["cmi"] = df["en_oran"]  # basitleştirilmiş CMI

# -------------------------------
# 3) Yapısal öznitelikler
# -------------------------------
# Sayısal dönüştürme (olasılık için)
for c in [col_views, col_subs]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["log_views"] = np.log1p(df[col_views].fillna(0))
df["log_subs"]  = np.log1p(df[col_subs].fillna(0))
df["text_len"]  = df["tokens"].astype(float)

# Hedefler (yüzde)
df[col_er_view] = pd.to_numeric(df[col_er_view], errors="coerce")
df[col_er_sub]  = pd.to_numeric(df[col_er_sub],  errors="coerce")

# Gruplama: kanal kimliği (yoksa hepsi ayrı grup)
groups = df[col_channel] if col_channel in df.columns else pd.Series(range(len(df)))

# -------------------------------
# 4) Özellik matrisi ve hedefler
# -------------------------------
feat_cols = ["en_oran","cmi","m_index","i_index","log_views","log_subs","text_len"]
X = df[feat_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0).values
y_view = df[col_er_view].values
y_sub  = df[col_er_sub].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------
# 5) Modeller
# -------------------------------
models_reg = {
    "Linear Regression": LinearRegression(),
    "SVR (RBF)": SVR(kernel='rbf', C=1.0, gamma='scale'),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=300, random_state=42),
    "XGBoost": XGBRegressor(
        n_estimators=400, learning_rate=0.05, max_depth=3, subsample=0.9, colsample_bytree=0.9,
        random_state=42, reg_lambda=1.0
    )
}

models_cls = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=2000),
    "Linear SVM": LinearSVC(class_weight='balanced', max_iter=5000),
    "XGBoost Classifier": XGBClassifier(
        n_estimators=400, learning_rate=0.05, max_depth=3, subsample=0.9, colsample_bytree=0.9,
        random_state=42, use_label_encoder=False, eval_metric='logloss'
    ),
}

# -------------------------------
# 6) Değerlendirme yardımcıları
# -------------------------------
def eval_reg(model, X, y, groups):
    gkf = GroupKFold(n_splits=5)
    maes, rmses, r2s = [], [], []
    for tr, te in gkf.split(X, y, groups):
        model.fit(X[tr], y[tr])
        p = model.predict(X[te])
        maes.append(mean_absolute_error(y[te], p))
        rmses.append(math.sqrt(mean_squared_error(y[te], p)))
        r2s.append(r2_score(y[te], p))
    return float(np.mean(maes)), float(np.mean(rmses)), float(np.mean(r2s))

def eval_cls(model, X, y, groups):
    gkf = GroupKFold(n_splits=5)
    y_pred_all, y_prob_all = [], []
    y_true_all = []
    for tr, te in gkf.split(X, y, groups):
        model.fit(X[tr], y[tr])
        y_pred = model.predict(X[te])
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X[te])[:,1]
        elif hasattr(model, "decision_function"):
            # skaler skor → sigmoid benzeri normalize (sadece AUPRC için yeterli sıralama)
            s = model.decision_function(X[te])
            y_prob = (s - s.min()) / (s.max() - s.min() + 1e-9)
        else:
            y_prob = y_pred.astype(float)
        y_true_all.extend(list(y[te]))
        y_pred_all.extend(list(y_pred))
        y_prob_all.extend(list(y_prob))
    y_true_all = np.array(y_true_all)
    y_pred_all = np.array(y_pred_all)
    y_prob_all = np.array(y_prob_all)
    acc = accuracy_score(y_true_all, y_pred_all)
    prec = precision_score(y_true_all, y_pred_all, zero_division=0)
    rec = recall_score(y_true_all, y_pred_all, zero_division=0)
    f1 = f1_score(y_true_all, y_pred_all, zero_division=0)
    auprc = average_precision_score(y_true_all, y_prob_all)
    return acc, prec, rec, f1, auprc, (y_true_all, y_pred_all, y_prob_all)

# -------------------------------
# 7) Regresyon: ER_View ve ER_Subscriber
# -------------------------------
rows = []
for name, model in models_reg.items():
    mae, rmse, r2 = eval_reg(model, X_scaled, y_view, groups)
    rows.append([name, "ER_View_%", mae, rmse, r2, "-", "-", "-", "-", "-"])
for name, model in models_reg.items():
    mae, rmse, r2 = eval_reg(model, X_scaled, y_sub, groups)
    rows.append([name, "ER_Subscriber_%", mae, rmse, r2, "-", "-", "-", "-", "-"])

# -------------------------------
# 8) Sınıflandırma: High/Low (ER_View medyan)
# -------------------------------
thr = np.nanmedian(y_view)
y_cls = (y_view >= thr).astype(int)

best_cm_payload = None
best_f1 = -1.0
for name, model in models_cls.items():
    acc, prec, rec, f1, auprc, payload = eval_cls(model, X_scaled, y_cls, groups)
    rows.append([name, "High/Low (ER_View)", "-", "-", "-", f1, auprc, acc, prec, rec])
    if f1 > best_f1:
        best_f1 = f1
        best_cm_payload = (name, payload)

# -------------------------------
# 9) Sonuçları tabloya yaz
# -------------------------------
res = pd.DataFrame(rows, columns=[
    "Model","Görev","MAE","RMSE","R²","F1","AUPRC","Accuracy","Precision","Recall"
])
with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as wr:
    res.to_excel(wr, sheet_name="Results", index=False)
print(f"✅ Kaydedildi: {OUT_XLSX}")
print(res)

# -------------------------------
# 10) Confusion Matrix + ROC (en iyi sınıflandırıcı)
# -------------------------------
if best_cm_payload is not None:
    best_name, (y_true, y_pred, y_prob) = best_cm_payload

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4.5,4))
    im = ax.imshow(cm, cmap="Blues")
    for (i,j), v in np.ndenumerate(cm):
        ax.text(j, i, str(v), ha='center', va='center')
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(f"Confusion Matrix – {best_name}")
    plt.tight_layout()
    plt.savefig(FIG_CM, dpi=200)
    plt.close(fig)

    # ROC (sadece olasılık/score varsa)
    if y_prob is not None and len(np.unique(y_true)) == 2:
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        fig2, ax2 = plt.subplots(figsize=(5,4))
        ax2.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
        ax2.plot([0,1],[0,1],'--')
        ax2.set_xlabel("False Positive Rate")
        ax2.set_ylabel("True Positive Rate")
        ax2.set_title(f"ROC Curve – {best_name}")
        ax2.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(FIG_ROC, dpi=200)
        plt.close(fig2)

    print(f"🖼️ Confusion Matrix kaydedildi: {FIG_CM}")
    print(f"🖼️ ROC Curve kaydedildi: {FIG_ROC}")
else:
    print("Not: En iyi sınıflandırıcı görseli üretilemedi.")
