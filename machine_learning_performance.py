# ==============================================
# Makine Öğrenimi Model Performans Analizi (Code-Mixing + ER)
# ==============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, LinearSVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, f1_score, average_precision_score
import math

# -------------------------------
# 1. Veri Setini Yükle
# -------------------------------
DATA_PATH = r"C:\Users\cdemi\Desktop\veriseti + analiz\codemix_er_merged_full.v2.xlsx"
df = pd.read_excel(DATA_PATH)

# Gerekli sütunlar (örnek)
cols_needed = ["video_id", "channel_id", "EN_Oran", "CMI", "M_index", "I_index",
               "views", "subscribers", "ER_View_%", "ER_Subscriber_%"]
df = df[[c for c in cols_needed if c in df.columns]]

# -------------------------------
# 2. Özellik Mühendisliği
# -------------------------------
df["log_views"] = np.log1p(df["views"])
df["log_subs"] = np.log1p(df["subscribers"])
df = df.dropna()

# Özellikler ve hedef değişkenler
X = df[["EN_Oran", "CMI", "M_index", "I_index", "log_views", "log_subs"]]
y_view = df["ER_View_%"]
y_sub = df["ER_Subscriber_%"]

# Kanal bazlı grup
groups = df["channel_id"]

# Normalizasyon
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------
# 3. Modelleri Tanımla
# -------------------------------
models_reg = {
    "Linear Regression": LinearRegression(),
    "SVR (RBF)": SVR(kernel='rbf', C=1.0, gamma='scale'),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost": XGBRegressor(
        n_estimators=200, learning_rate=0.1, max_depth=3, subsample=0.9, random_state=42)
}

models_cls = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000),
    "Linear SVM": LinearSVC(class_weight='balanced', max_iter=2000),
    "XGBoost Classifier": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
}

# -------------------------------
# 4. Değerlendirme Fonksiyonları
# -------------------------------
def evaluate_regression(model, X, y, groups):
    gkf = GroupKFold(n_splits=5)
    maes, rmses, r2s = [], [], []
    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        maes.append(mean_absolute_error(y_test, preds))
        rmses.append(math.sqrt(mean_squared_error(y_test, preds)))
        r2s.append(r2_score(y_test, preds))
    return np.mean(maes), np.mean(rmses), np.mean(r2s)

def evaluate_classification(model, X, y, groups):
    gkf = GroupKFold(n_splits=5)
    f1s, auprcs = [], []
    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test)[:,1]
        else:
            probs = preds
        f1s.append(f1_score(y_test, preds))
        auprcs.append(average_precision_score(y_test, probs))
    return np.mean(f1s), np.mean(auprcs)

# -------------------------------
# 5. Regresyon Görevleri
# -------------------------------
results = []
for name, model in models_reg.items():
    mae, rmse, r2 = evaluate_regression(model, X_scaled, y_view, groups)
    results.append([name, mae, rmse, r2, "-", "-", "ER_View"])
    mae, rmse, r2 = evaluate_regression(model, X_scaled, y_sub, groups)
    results.append([name, mae, rmse, r2, "-", "-", "ER_Subscriber"])

# -------------------------------
# 6. Sınıflandırma Görevi (yüksek/düşük etkileşim)
# -------------------------------
median_thr = y_view.median()
y_class = (y_view >= median_thr).astype(int)

for name, model in models_cls.items():
    f1, auprc = evaluate_classification(model, X_scaled, y_class, groups)
    results.append([name, "-", "-", "-", f1, auprc, "High/Low Engagement"])

# -------------------------------
# 7. Sonuçları Kaydet
# -------------------------------
df_results = pd.DataFrame(results, columns=["Model", "MAE", "RMSE", "R²", "F1", "AUPRC", "Görev"])
df_results.to_excel(r"C:\Users\cdemi\Desktop\Model_Performance_Results.xlsx", index=False)
print("✅ Model performans tablosu oluşturuldu: Model_Performance_Results.xlsx")
print(df_results)
