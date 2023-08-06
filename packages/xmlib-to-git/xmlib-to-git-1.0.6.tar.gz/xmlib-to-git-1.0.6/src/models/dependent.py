import src.settings as settings, os, json
from src.utils import my_json

def creates_dependents(dependents):
    # Dependants objects
    readme = open("{}/DEPENDENTS.md".format(settings.APP_DIR), "w+", encoding="utf-8")
    with readme:
        readme.write("\n## Objets dépendants:\n")
        json_path = os.path.join(settings.SRC_DIR, "utils", "objects_dict.json")
        objects_dict = json.load(open(json_path))
        readme.write(
            "|Id d'origine|Id|Nom|Nom d'intégration|\n" "|---|---|---|---|\n"
        )

        # write in json file
        jsontest = json.dumps(objects_dict)
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(jsontest)

        del jsontest

        for dependent in dependents:
            obj = my_json.find_in_json(objects_dict, dependent["id"])
            readme.write(
                "|{}|{}|{}|{}|\n".format(
                    dependent["origId"],
                    dependent["id"],
                    dependent.SingularName.cdata,
                    dependent["objDefName"],
                )
            )
