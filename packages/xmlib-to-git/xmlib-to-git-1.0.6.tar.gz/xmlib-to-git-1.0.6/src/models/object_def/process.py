# process.py

import os
from src.models._base_def import AField

def creates_processes(processes, obj_dir) -> None:
    path = "{}/processes".format(obj_dir)
    if not os.path.exists(path.encode("utf-8")):
        os.makedirs(path.encode("utf-8"))
    for process in processes:
        Process(process, path).to_file()


class Process(AField):
    """ """

    translations = ""
    workflow = ""

    def __init__(self, data, path):
        super().__init__(data, path)

        self.order = data["orderNo"]
        self.obj_type_id = data["objTypeId"]
        self.def_status_id = data["defStatusId"]

    def to_file(self):
        super().to_file()

        file = open("{}/PROPETIES.md".format(self.dir), "w+", encoding="utf-8")
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
            file.write("- defStatusId : {}\n".format(self.def_status_id))
