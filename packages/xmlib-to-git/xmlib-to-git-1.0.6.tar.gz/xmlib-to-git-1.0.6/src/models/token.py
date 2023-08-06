# token.py

from src import settings

def creates_tokens(token_names):
    t = open("{}/TOKENS.md".format(settings.APP_DIR), "w+", encoding="utf-8")
    with t:
        t.write("\n## Champs de fusion :\n")
        for x in token_names.split("|"):
            if len(x) > 0:
                t.write("- {}\n".format(x))