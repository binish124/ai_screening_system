import pytest
from parsers.resume_parser import clean_text

def test_clean_text_removes_noise():
    raw = "Here is some text \x00 with weird \x08 symbols."
    cleaned = clean_text(raw)
    assert "\x00" not in cleaned
    assert "\x08" not in cleaned

def test_clean_text_normalizes_bullets():
    raw = "• Python\n* Java\n> C++"
    cleaned = clean_text(raw)
    assert "•" not in cleaned
    assert "*" not in cleaned

def test_clean_text_normalizes_headings():
    raw = "Work Experience\nBuilt some apps."
    cleaned = clean_text(raw)
    assert "EXPERIENCE" in cleaned.upper()