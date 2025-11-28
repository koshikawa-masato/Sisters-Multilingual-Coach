"""
Localization module for Sisters-Multilingual-Coach

Structure:
- locales/
  - en/translations.py  (English)
  - ja/translations.py  (日本語)
  - zh/translations.py  (中文)
  - ko/translations.py  (한국어)
  - es/translations.py  (Español)

Each language file contains:
- LANGUAGE_INFO: code, flag, native_name
- GOALS: goal text for each target language
- UI_TEXT: all UI strings
"""

from locales.en import translations as en
from locales.ja import translations as ja
from locales.zh import translations as zh
from locales.ko import translations as ko
from locales.es import translations as es

# Map language name to module
_LANG_MODULES = {
    "English": en,
    "日本語": ja,
    "中文": zh,
    "한국어": ko,
    "Español": es,
}

# Build LANGUAGES dict from individual files
LANGUAGES = {
    name: module.LANGUAGE_INFO
    for name, module in _LANG_MODULES.items()
}

# Build GOALS dict: {target_language: {native_language: goal_text}}
GOALS = {}
for target_lang in LANGUAGES.keys():
    GOALS[target_lang] = {}
    for native_lang, module in _LANG_MODULES.items():
        GOALS[target_lang][native_lang] = module.GOALS.get(target_lang, "")

# Build UI_TEXT dict: {native_language: {key: text}}
UI_TEXT = {
    name: module.UI_TEXT
    for name, module in _LANG_MODULES.items()
}

# Export all
__all__ = ["LANGUAGES", "GOALS", "UI_TEXT"]
