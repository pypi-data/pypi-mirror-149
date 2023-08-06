# role_page.py

from src import settings

def creates_role_pages(roles):
    t = open("{}/ROLE_PAGES.md".format(settings.APP_DIR), "w+", encoding="utf-8")
    with t:
        t.write("\n## Role page:\n")
        
        t.write("|pageDefId|pageId|roleId|\n|---|---|---|\n")
        for x in roles:
            #TODO: find pageDef name and Role name
            t.write("|{}|{}|{}|\n".format(x["pageDefId"], x["pageId"], x["roleId"]))