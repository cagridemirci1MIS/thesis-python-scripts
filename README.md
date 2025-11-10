Thesis Python Scripts – Cagri Demirci (2025)

This repository contains Python scripts developed for the MSc Thesis project by Cagri Demirci, focusing on code-mixing analysis, language interaction, and digital communication analytics.
Each file represents an independent analytical module that can be executed individually or imported as part of a larger research workflow.

📘 Project Overview

These scripts were created to support linguistic and computational research on English lexical borrowings in Turkish social media texts.
The analyses cover code-mixing ratios, English root extraction, engagement metrics, machine learning performance, and visual insights from exploratory data analysis.

📂 File Descriptions
🔤 Linguistic Analysis

code_mixing_ratio.py

Calculates the Code-Mixing Ratio (CMR) by identifying English tokens within multilingual text data.

Detects English-origin words in mixed-language texts.

Returns a numeric ratio (English words / total words).

Works with text strings or pandas Series.

english_root_extraction.py

Extracts English roots from Turkish-English hybrid words (e.g., like'lamak, save'ledim).

Includes regex-based substring detection and optional NLTK stemming.

Returns token lists and frequency counts.

english_wordcloud.py

Generates visual word clouds of English tokens extracted from code-mixed datasets.

Provides frequency-weighted visualization to highlight dominant English borrowings.

Supports customization of color palettes, shapes, and stopwords.

📊 Data Analysis and Visualization

exploratory_data_analysis.py

Performs initial EDA (Exploratory Data Analysis) on text datasets (CSV/JSON).

Provides descriptive statistics, token distributions, and visualization options.

Generates exportable summary tables.

final_eda_visualisation.py

Produces detailed EDA visualizations including frequency plots and token heatmaps.

Used to complement exploratory_data_analysis.py outputs for presentation-ready visuals.

merge_codemix_data.py

Merges multilingual datasets for cross-platform or multi-source analysis.

Handles deduplication, normalization, and consistent text encoding.

pipeline_diagram.py

Visualizes the full data processing and modeling pipeline.

Generates flowcharts showing interactions between linguistic and ML modules.

🤖 Machine Learning and Performance Analysis

machine_learning_performance.py

Evaluates model performance metrics (accuracy, precision, recall, F1-score).

Supports multiple models for comparative benchmarking.

Outputs structured reports and plots.

Model_Performance_Bulgular.py

Summarizes empirical findings from model performance experiments.

Provides tabular and visual interpretations of classification outcomes.

Intended for inclusion in thesis result sections.

YouTube_CodeMix_Model_Performance.py

Integrates YouTube data (e.g., comments, titles) into code-mixing performance evaluation.

Assesses how English code-mixing influences engagement and model accuracy.

🎥 Social Media Engagement

youtube_engagement_rate.py

Calculates engagement rate from YouTube video metadata:
Engagement Rate = ((Likes + Comments) / Views) * 100

Vectorized for DataFrame-level computation.

Handles missing or zero-view cases safely.

⚙️ How to Run

Clone the repository and navigate into the folder:

git clone https://github.com/yourusername/thesis_python_scripts.git
cd thesis_python_scripts


Run scripts individually:

python code_mixing_ratio.py
python english_root_extraction.py
python youtube_engagement_rate.py
python machine_learning_performance.py


Or import modules directly into a Jupyter Notebook or Python environment.

🔐 API Keys

All sensitive credentials are removed.
If an API call is needed, replace:

API_KEY = "YOUR_API_KEY"


with your valid key.

🧠 Citation

Demirci, C. (2025). Code-Mixing in Digital Communication: Data-Driven Analysis of the Use of English in Turkish Social Media Texts.
MSc Thesis, Erciyes University.

📄 License

These scripts are provided for academic and research purposes under an open educational license.
Reuse or adaptation is permitted with proper attribution to the author.

Author: Cagri Demirci
Year: 2025
Email: cagridemirci1@gmail.com

Location: Kayseri, Türkiye
