# conversion.py

import os

from src.models._base_def import AField


def creates_conversions(conversions, obj_dir) -> None:
    path = "{}/conversions".format(obj_dir)
    if not os.path.exists(path.encode("utf-8")):
        os.makedirs(path.encode("utf-8"))
    for conversion in conversions:
        ImportMap(conversion, path).to_file()


class ImportMap(AField):
    """ " """

    def __init__(self, data, path) -> None:
        super().__init__(data, path)
        self.dest_def_id = data["destDefId"]
        self.check = data["checkRequiredFields"]

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
            file.write("- destDefId : {}\n".format(self.dest_def_id))
            file.write("- checkRequiredFields : {}\n".format(self.check))

            if self.columns:
                # dest="process" col="-10" uniqueId="-1"
                file.write("\n\n## Columns\n")
                file.write("|dest|col|uniqueId|\n")
                file.write("|---|---|---|\n")
                for c in self.columns:
                    file.write(
                        ("|{}|{}|{}|\n").format(c["dest"], c["col"], c["uniqueId"])
                    )
