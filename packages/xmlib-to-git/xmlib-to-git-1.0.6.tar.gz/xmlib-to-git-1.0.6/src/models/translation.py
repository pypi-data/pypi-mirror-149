# permission.py

from src import settings

def creates_translations(translations, dir = ""):
    if dir:
        final_dir = "{}/TRANSLATIONS.md".format(dir)
    else :
        final_dir = "{}/TRANSLATIONS.md".format(settings.APP_DIR)
    t = open(final_dir, "w+", encoding="utf-8")
    with t:
        t.write("\n## Translations :\n")
        
        t.write("|fieldName|langCode|text|\n|---|---|---|\n")
        for x in translations:
                t.write("|{}|{}|{}|\n".format(x["fieldName"], x["langCode"], x["text"]))