# Author: Cagri Demirci
# Appendix A.2 – English Root Extraction from Turkish Social Media Text
# Part of MSc Thesis (2025)

"""
English Root Extraction Script

This script extracts and lists all English word roots appearing in a given
set of Turkish social media texts. The main goal is to identify the English-origin
components that appear in code-mixed or hybrid forms (e.g., “like’lamak”, “save’ledim”).

Methodology
-----------
1) Tokenization and normalization of input text.
2) Regular expression matching for possible English substrings.
3) Optional stemming of English tokens for root detection (if NLTK is available).
4) Output of frequency counts for English word roots.

Dependencies
------------
- pandas
- re
- nltk (optional; used only for stemming if installed)

Usage Examples
---------------
# Example 1: Run directly
python english_root_extraction.py

# Example 2: Import as a library
from english_root_extraction import extract_english_roots
roots = extract_english_roots("Bugün like'ladım ve save'ledim.")
print(roots)
"""

from __future__ import annotations
import re
from typing import List, Optional
import pandas as pd

try:
    from nltk.stem import PorterStemmer
except ImportError:
    PorterStemmer = None


ENGLISH_FRAGMENT_RE = re.compile(r"[A-Za-z']+")


def extract_english_roots(
    text: str,
    use_stemming: bool = True,
) -> List[str]:
    """
    Extracts candidate English roots from the provided text.

    Parameters
    ----------
    text : str
        Input text possibly containing code-mixed English elements.
    use_stemming : bool
        Whether to apply English stemming (requires nltk).

    Returns
    -------
    List[str]
        A list of English root tokens found in the text.
    """
    if not text:
        return []

    # Identify all English-like substrings (e.g., "like", "save", "follow")
    tokens = [t.strip("'") for t in ENGLISH_FRAGMENT_RE.findall(text)]
    tokens = [t for t in tokens if t and len(t) > 1]

    if not tokens:
        return []

    if use_stemming and PorterStemmer is not None:
        stemmer = PorterStemmer()
        return [stemmer.stem(tok.lower()) for tok in tokens]
    else:
        return [tok.lower() for tok in tokens]


def extract_roots_from_series(
    texts: pd.Series,
    use_stemming: bool = True,
) -> pd.DataFrame:
    """
    Applies English root extraction across a pandas Series of texts.

    Returns a DataFrame with:
    - 'text' (original text)
    - 'english_roots' (list of English roots)
    - 'root_count' (number of unique roots)
    """
    results = []
    for t in texts.fillna(""):
        roots = extract_english_roots(t, use_stemming=use_stemming)
        results.append(
            {
                "text": t,
                "english_roots": roots,
                "root_count": len(set(roots)),
            }
        )
    return pd.DataFrame(results)


if __name__ == "__main__":
    # Minimal demonstration
    example = "Bugün like'ladım ve save'ledim."
    roots = extract_english_roots(example)
    print(f"Input text: {example}")
    print(f"Extracted English roots: {roots}")
