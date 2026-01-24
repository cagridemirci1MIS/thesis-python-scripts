# Code-Mixing Analysis in Turkish Social Media Content

## Project Overview

This repository contains the data collection, preprocessing, and analytical pipeline developed as part of a Master’s thesis in the field of **Management Information Systems**. The study focuses on the **use of English-origin words and code-mixing (Turkish–English)** in Turkish social media texts and examines this phenomenon from a **socio-technical systems perspective**.

Using YouTube gaming content produced by Turkish creators, the project applies **Natural Language Processing (NLP)**, **machine learning**, and **BERT-based deep learning models** to analyze multilingual user-generated data and to evaluate how code-mixing relates to **digital engagement indicators** and **model performance**.

---

## Research Questions

The empirical analyses conducted in this repository address the following research questions:

- **RQ1:** Is there a statistically significant relationship between the level of code-mixing in Turkish social media content and digital engagement indicators (e.g., views, likes, comments)?
- **RQ2:** Does the degree of code-mixing affect the performance of machine learning and BERT-based deep learning models in classification and prediction tasks?
- **RQ3:** Can linguistic features related to code-mixing be used as meaningful input variables for predicting engagement levels?

---

## Data Collection and Selection Criteria

The data collection process follows a multi-stage pipeline implemented in Python:

### Video and Channel Selection
- Platform: YouTube  
- Region: Turkey (`TR`)  
- Language context: Turkish  
- Content domain: Gaming-related videos  
- Sources:
  - Predefined Turkish gaming content creators
  - Keyword-based YouTube search queries

### Filtering and Selection
- Inclusion based on gaming-related keywords in video titles and descriptions
- Exclusion of non-relevant content (e.g., news, politics, children’s content)
- Long-form video duration constraints
- Deduplication based on video identifiers
- Ranking and selection of videos using engagement-based criteria and channel-level limits

### Transcript Retrieval
- Video transcripts were retrieved via the YouTube Data API.
- API credentials are not included in the repository and must be provided by the user.

### Feature Construction
- Detection of English-origin lexical items in Turkish transcripts
- Computation of code-mixing indicators and frequency-based features

All selection thresholds, keyword lists, and constraints are explicitly defined in the codebase to ensure transparency and reproducibility.

---

## Data Availability

Due to platform terms of service and ethical considerations related to user-generated content, **raw YouTube transcripts and full datasets are not publicly shared**.

To support transparency and reproducibility, this repository provides:
- All scripts used for data collection, filtering, and preprocessing,
- A derived and anonymized **sample dataset** (`data/sample/sample_codemixing_dataset.xlsx`),
- All feature extraction and modeling code used in the analyses.

The shared sample dataset includes the following variables:
- `Video_ID`: anonymized video identifier  
- `Transkript`: processed transcript text  
- `english_detect`: detected English-origin lexical items  
- `english_counts`: frequency of detected English-origin items  

Researchers may reproduce the full dataset by re-running the provided scripts with their own API credentials, subject to YouTube’s terms of service.

---

## Repository Structure
thesis-python-scripts/
│
├─ config/ # Selection criteria and thresholds
├─ data/
│ └─ sample/ # Anonymized sample dataset
├─ scripts/ # Data collection and preprocessing pipeline
├─ src/ # Core feature extraction and modeling modules
├─ notebooks/ # Exploratory analysis and modeling notebooks
├─ requirements.txt
├─ .env.example
├─ CITATION.cff
└─ README.md

---

## How to Run

pip install -r requirements.txt

YOUTUBE_API_KEY=your_api_key_here

python scripts/select_top50.py

## Ethical Considerations

This study adheres to ethical research principles concerning digital trace data and user-generated content. No personally identifiable information is disclosed. Data sharing is limited to derived and anonymized samples, and all data collection complies with YouTube’s terms of service.

## Citation

If you use this repository or build upon this work, please cite:

Demirci, C. (2026). Data-Driven Analysis of the Use of English in Turkish Social Media Texts.
MSc Thesis, Erciyes University.
---


Türkçe Açıklama
Proje Özeti

Bu depo, Yönetim Bilişim Sistemleri alanında hazırlanmış bir yüksek lisans tezi kapsamında geliştirilen veri toplama, ön işleme ve analiz süreçlerini içermektedir. Çalışma, Türkçe sosyal medya metinlerinde İngilizce kökenli sözcüklerin kullanımı ve kod karışımı (Türkçe–İngilizce) olgusunu sosyo-teknik sistemler perspektifi çerçevesinde incelemektedir.

YouTube platformunda Türk içerik üreticileri tarafından üretilen oyun videoları temel alınarak; Doğal Dil İşleme (NLP), makine öğrenimi ve BERT tabanlı derin öğrenme modelleri kullanılmış, kod karışımının dijital etkileşim göstergeleri ve model performansı ile ilişkisi analiz edilmiştir.

Araştırma Soruları

Bu depoda gerçekleştirilen ampirik analizler aşağıdaki araştırma sorularını ele almaktadır:

AR1: Türkçe sosyal medya içeriklerinde kod karışımı düzeyi ile dijital etkileşim göstergeleri (izlenme, beğeni, yorum sayısı vb.) arasında anlamlı bir ilişki var mıdır?

AR2: Kod karışımı düzeyi, makine öğrenimi ve BERT tabanlı derin öğrenme modellerinin sınıflandırma ve tahmin performansını etkilemekte midir?

AR3: Kod karışımına ilişkin dilsel özellikler, etkileşim düzeylerinin tahmininde anlamlı girdi değişkenleri olarak kullanılabilir mi?

Veri Toplama ve Seçim Kriterleri

Veri toplama süreci Python ile geliştirilen çok aşamalı bir iş akışına dayanmaktadır:

Video ve Kanal Seçimi

Platform: YouTube

Bölge: Türkiye (TR)

Dil bağlamı: Türkçe

İçerik alanı: Oyun içerikleri

Kaynaklar:

Önceden belirlenmiş Türk oyun içerik üreticileri

Anahtar kelime tabanlı YouTube aramaları

Filtreleme ve Seçim

Video başlığı ve açıklamasında oyunla ilişkili anahtar kelimelerin bulunması

Haber, politika, çocuk içeriği gibi alakasız içeriklerin hariç tutulması

Uzun format video süre kısıtları

Video kimliği üzerinden tekilleştirme

Etkileşim temelli sıralama ve kanal bazlı üst sınırlar

Transkript Toplama

Video transkriptleri YouTube Data API aracılığıyla elde edilmiştir.

API anahtarları depoda yer almamakta, kullanıcı tarafından sağlanmaktadır.

Özellik Türetme

Türkçe metinlerde İngilizce kökenli sözcüklerin tespiti

Kod karışımı göstergeleri ve frekans tabanlı metriklerin hesaplanması

Tüm eşikler, anahtar kelime listeleri ve kısıtlar, şeffaflık ve tekrar üretilebilirlik amacıyla kod tabanında açıkça tanımlanmıştır.

Veri Erişilebilirliği

Platform kullanım koşulları ve kullanıcı tarafından üretilmiş içeriklere ilişkin etik gerekçeler nedeniyle ham YouTube transkriptleri ve tam veri seti paylaşılmamaktadır.

Şeffaflık ve tekrar üretilebilirliği desteklemek amacıyla bu depo:

Veri toplama, filtreleme ve ön işleme için kullanılan tüm betikleri,

Türetilmiş ve anonimleştirilmiş bir örnek veri setini (data/sample/sample_codemixing_dataset.xlsx),

Analizlerde kullanılan tüm özellik çıkarımı ve modelleme kodlarını içermektedir.

Paylaşılan örnek veri setinde yer alan değişkenler:

Video_ID: anonimleştirilmiş video kimliği

Transkript: işlenmiş transkript metni

english_detect: tespit edilen İngilizce kökenli sözcükler

english_counts: tespit edilen İngilizce kökenli sözcüklerin frekansı

Araştırmacılar, kendi API anahtarlarını kullanarak ilgili betikleri yeniden çalıştırmak suretiyle veri setini yeniden üretebilirler.

Depo Yapısı
thesis-python-scripts/
│
├─ config/          # Seçim kriterleri ve eşikler
├─ data/
│   └─ sample/      # Anonimleştirilmiş örnek veri seti
├─ scripts/         # Veri toplama ve ön işleme adımları
├─ src/             # Özellik çıkarımı ve modelleme modülleri
├─ notebooks/       # Keşifsel analiz ve modelleme defterleri
├─ requirements.txt
├─ .env.example
├─ CITATION.cff
└─ README.md

Çalıştırma Adımları

Bağımlılıkların kurulması

pip install -r requirements.txt


API anahtarının ayarlanması
.env.example dosyasına göre bir .env dosyası oluşturun ve YouTube Data API anahtarınızı ekleyin:

YOUTUBE_API_KEY=your_api_key_here


Seçim ve ön işleme sürecinin çalıştırılması

python scripts/select_top50.py


Özellik çıkarımı ve modelleme
scripts/ klasöründeki betikler veya notebooks/ klasöründeki defterler kullanılarak analizler tekrarlanabilir.

Etik Hususlar

Bu çalışma, dijital iz verilerinin kullanımına ilişkin etik araştırma ilkelerine uygun olarak yürütülmüştür. Kişisel olarak tanımlanabilir herhangi bir bilgi paylaşılmamaktadır. Veri paylaşımı yalnızca türetilmiş ve anonimleştirilmiş örnekler ile sınırlıdır ve tüm veri toplama süreçleri YouTube’un kullanım koşullarıyla uyumludur.

Atıf

Bu depoyu kullanan veya bu çalışmadan yararlanan araştırmacıların aşağıdaki kaynağa atıf vermesi rica olunur:

Demirci, C. (2026). Türkçe Sosyal Medya Metinlerinde İngilizce Kökenli Kelime
Kullanımının Veri Odaklı Analizi.
Yüksek Lisans Tezi, Erciyes Üniversitesi.
