# permission.py

from src import settings

def creates_permissions(permissions):
    t = open("{}/PERMISSIONS.md".format(settings.APP_DIR), "w+", encoding="utf-8")
    with t:
        t.write("\n## Permissions :\n")
        
        t.write("|resId|prId|actionsSet|\n|---|---|---|\n")
        for x in permissions:
                t.write("|{}|{}|{}|\n".format(x["resId"], x["prId"], x["actionsSet"]))