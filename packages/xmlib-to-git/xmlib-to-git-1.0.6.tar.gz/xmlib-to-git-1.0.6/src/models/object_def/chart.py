# chart.py

import os
from src.models._base_def import AField


def creates_charts(charts, obj_dir) -> None:
    path = "{}/charts".format(obj_dir)
    if not os.path.exists(path.encode("utf-8")):
        os.makedirs(path.encode("utf-8"))
    for chart in charts:
        Chart(chart, path).to_file()


class Chart(AField):
    """ "
    Chart def
    """

    def __init__(self, data, path) -> None:
        super().__init__(data, path)
        self.order = data["orderNo"]

    def to_file(self) -> None:
        super().to_file()

        file = open("{}/PROPERTIES.md".format(self.dir), "w+", encoding="utf-8")
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- objDefId : {}\n".format(self.obj_def_id))
            file.write("- order : {}\n".format(self.order))
