# view.py

import os
from src.models._base_def import AField
from src.utils import split_tool

def creates_views(views, obj_dir) -> None:
        path = "{}/views".format(obj_dir)
        if not os.path.exists(path.encode('utf-8')):
            os.makedirs(path.encode('utf-8'))
        
        from .view import View
        for view in views:
            new_view = View(view, path)
            new_view.to_file()

class View(AField):
    """

    """

    properties = ""

    def __init__(self, data, path):
        super().__init__(data, path)

        self.order = data["orderNo"]
        self.is_system = data["isSystem"]
        self.columns = data.Columns.cdata.replace("\n","")

    def to_file(self):
        super().to_file()
        
        file = open("{}/PROPERTIES.md".format(self.dir), 'w+', encoding='utf-8')
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- orderNo : {}\n".format(self.orig_id))
            file.write("- isSystem : {}\n".format(self.is_system))

            # Propriétés
            if self.properties:
                file.write("\n\n## Properties\n")
                for el in self.properties["children"]:
                    file.write("- {} : {}\n".format(el.__dict__["_name"], el.__dict__["cdata"]))

            #Colonnes
            file.write("\n\n## Columns\n")
            for col in self.columns.split(","):
                if col and col != " ":
                    file.write("- {}\n".format(col))


