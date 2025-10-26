Python 3.13.6 (tags/v3.13.6:4e66535, Aug  6 2025, 14:36:00) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> # Author: Cagri Demirci
... # Appendix A.1 – Code-Mixing Ratio Calculation
... # Part of MSc Thesis (2025)
... 
... """
... Code-Mixing Ratio (CMR) Calculator
... 
... This script computes the proportion of English tokens within Turkish (or mixed)
... social media texts. It offers two complementary heuristics:
... 
... 1) ASCII-word heuristic:
...    Counts tokens composed only of [A–Z a–z] as English candidates.
...    (Useful when diacritics or non-Latin scripts are present in the non-English text.)
... 
... 2) Optional English lexicon filter:
...    If you provide a set of known English words (e.g., a frequency list),
...    the script will only count a token as English if it appears in that lexicon.
... 
... These heuristics are lightweight and transparent. They do not claim perfect
... language identification and should be interpreted accordingly.
... 
... Usage examples
... --------------
... # Example 1: quick test on a single string
... python code_mixing_ratio.py
... 
... # Example 2: as a library
... from code_mixing_ratio import code_mixing_ratio, cmr_on_series
... ratio = code_mixing_ratio("Bugün very good bir gün oldu.")
... 
... # Example 3: with a pandas Series
... import pandas as pd
... texts = pd.Series(["Bugün very good bir gün oldu.", "Tamamen Turkish cümle."])
... results = cmr_on_series(texts)
... print(results)
... """

from __future__ import annotations
import re
from typing import Iterable, Optional, Set

import pandas as pd


ASCII_WORD_RE = re.compile(r"^[A-Za-z]+$")


def is_english_token(
    token: str,
    english_lexicon: Optional[Set[str]] = None,
) -> bool:
    """
    Returns True if `token` is considered an English token according to:
    - ASCII-only heuristic (token contains only A–Z or a–z), and
    - If `english_lexicon` is provided, the token must also be in that set.

    The token is normalized to lowercase before lexicon lookup.
    """
    if not token:
        return False

    if not ASCII_WORD_RE.match(token):
        return False

    if english_lexicon is not None:
        return token.lower() in english_lexicon

    return True


def tokenize(text: str) -> Iterable[str]:
    """
    Very simple whitespace and punctuation-based tokenizer.
    Keeps only alphanumeric word chunks.
    """
    # Split on non-letter characters, drop empties
    return [t for t in re.split(r"[^A-Za-zÀ-ÖØ-öø-ÿĞÜŞİğüşiçÇ]+", text) if t]


def code_mixing_ratio(
    text: str,
    english_lexicon: Optional[Set[str]] = None,
) -> float:
    """
    Computes the Code-Mixing Ratio (CMR) for a single text:
        CMR = (# of English tokens) / (# of all tokens)

    If there are zero tokens, returns 0.0.
    """
    tokens = tokenize(text)
    if not tokens:
        return 0.0

    eng_count = sum(
        1 for tok in tokens if is_english_token(tok, english_lexicon=english_lexicon)
    )
    return eng_count / float(len(tokens))


def cmr_on_series(
    texts: pd.Series,
    english_lexicon: Optional[Set[str]] = None,
    text_col_name: Optional[str] = None,
) -> pd.DataFrame:
    """
    Applies CMR to a pandas Series of strings and returns a DataFrame with:
        - 'text' (original text)
        - 'token_count'
        - 'english_token_count'
        - 'cmr' (ratio)

    Parameters
    ----------
    texts : pd.Series
        Series of text entries.
    english_lexicon : Optional[Set[str]]
        Optional set of valid English words to constrain English detection.
    text_col_name : Optional[str]
        Optional column name to use for the text in the output (default: 'text').
    """
    rows = []
    for t in texts.fillna(""):
        toks = tokenize(t)
        token_count = len(toks)
        eng_count = sum(
            1 for tok in toks if is_english_token(tok, english_lexicon=english_lexicon)
        )
        cmr = (eng_count / token_count) if token_count > 0 else 0.0
        rows.append(
            {
                (text_col_name or "text"): t,
                "token_count": token_count,
                "english_token_count": eng_count,
                "cmr": cmr,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Minimal demo (no external files, no dummy datasets):
    example = "Bugün very good bir gün oldu."
    ratio = code_mixing_ratio(example)
    print(f"Text: {example}")
    print(f"Code-mixing ratio: {ratio:.4f}")

    # If you want to use a tiny custom lexicon (optional), uncomment below:
    # english_lex = {"very", "good", "day", "hello", "world"}
    # ratio_lex = code_mixing_ratio(example, english_lexicon=english_lex)
    # print(f"Code-mixing ratio (with lexicon): {ratio_lex:.4f}")
