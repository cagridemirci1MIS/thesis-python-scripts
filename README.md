# Thesis Python Scripts – Cagri Demirci (2025)

This repository contains Python scripts developed for the MSc Thesis project by **Cagri Demirci**, focusing on **code-mixing analysis**, **language interaction**, and **digital communication analytics**.  
Each file represents an independent analytical module that can be executed individually or imported as part of a larger workflow.

## 📘 Project Overview
These scripts were created to support linguistic and computational research on **English lexical borrowings in Turkish social media texts**.  
The analyses focus on code-mixing ratios, English root extraction, engagement measurement, and general exploratory data analysis (EDA).

## 📂 File Descriptions
### `code_mixing_ratio.py`
Calculates the **Code-Mixing Ratio (CMR)** by identifying English tokens within multilingual text data.
- Detects English-origin words in mixed-language texts.  
- Returns a numeric ratio (English words / total words).  
- Compatible with both single-text and pandas Series input.

### `english_root_extraction.py`
Extracts English roots from Turkish-English hybrid words such as `like'lamak` or `save'ledim`.  
Applies optional stemming (via NLTK) for root normalization.
- Regex-based detection of English substrings.  
- Optional stemming for root-level analysis.  
- Returns token lists and frequency counts.

### `youtube_engagement_rate.py`
Computes **YouTube engagement rate** using likes, comments, and views.
```
Engagement Rate = ((Likes + Comments) / Views) * 100
```
- Safe division (avoids division by zero).  
- Vectorized computation for pandas DataFrames.  
- Outputs engagement rate per video.

### `exploratory_data_analysis.py`
Performs basic **exploratory data analysis (EDA)** on text datasets.
- Supports CSV and JSON input.  
- Provides descriptive statistics and optional visualization.  
- Exportable as summary tables.

## ⚙️ How to Run
Clone this repository and navigate into the folder:
```bash
git clone https://github.com/yourusername/thesis_python_scripts.git
cd thesis_python_scripts
```
Run each script individually:
```bash
python code_mixing_ratio.py
python english_root_extraction.py
python youtube_engagement_rate.py
python exploratory_data_analysis.py data.csv
```
Or import functions directly in a Jupyter Notebook or Python environment.

## 🔐 Important Note on API Keys
All sensitive credentials have been **removed**.  
If an API call is needed, replace the placeholder line:
```python
API_KEY = "YOUR_API_KEY"
```
with your own valid key before execution.

## 🧠 Citation
> Demirci, C. (2025). *Code-Mixing in Digital Communication: Data-Driven Analysis of the Use of English in Turkish Social Media Texts*.  
> MSc Thesis, Erciyes University.

## 📄 License
These scripts are provided for **academic and research purposes** under an open educational license.  
You may reuse or adapt them with proper attribution to the author.

**Author:** Cagri Demirci  
**Year:** 2025  
**Email:** cagridemirci1@gmail.com  
**Location:** Kayseri, Türkiye
