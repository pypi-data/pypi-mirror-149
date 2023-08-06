# status.py
import os
from src.models._base_def import AField
from src.models.translation import creates_translations

from src.utils import split_tool


def creates_statuses(statuses, obj_dir) -> None:
    path = "{}/statuses".format(obj_dir)
    if not os.path.exists(path.encode("utf-8")):
        os.makedirs(path.encode("utf-8"))
    for status in statuses:
        Status(status, path).to_file()


class Status(AField):
    """ """

    translations = ""

    def __init__(self, data, path):
        super().__init__(data, path)

        self.order = data["orderNo"]
        self.obj_type_id = data["objTypeId"]

    def to_file(self):
        super().to_file()

        file = open("{}/STATUS.md".format(self.dir), "w+", encoding="utf-8")
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- orderNo : {}\n".format(self.order))
            file.write("- objDefId : {}\n".format(self.obj_def_id))
            file.write("- objTypeId : {}\n".format(self.obj_type_id))
