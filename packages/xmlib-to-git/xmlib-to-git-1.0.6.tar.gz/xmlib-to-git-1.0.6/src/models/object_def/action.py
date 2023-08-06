# action.py

import os
from src.models._base_def import AField

def creates_actions(actions, obj_dir) -> None:
        path = "{}/actions".format(obj_dir)
        if not os.path.exists(path.encode('utf-8')):
            os.makedirs(path.encode('utf-8'))
        for action_data in actions:
            action = Action(action_data, path)
            action.to_file()

class Action(AField):
    """

    """

    def __init__(self, action, path) -> None:
        super().__init__(action, path)
        self.order = action["orderNo"]
        self.action_type = action["actionType"]
        self.order = action["orderNo"]
        self.page_id = action["pageId"]
        self.next_stauts_id = action ["nextStatusId"]
        self.is_group = action["isGroup"]
        self.obj_type_id = action["objTypeId"]
        

    def to_file(self) -> None:
        super().to_file()
        # fichier de propriétés
        if not os.path.exists(self.dir.encode('utf-8')):
            os.makedirs(self.dir.encode('utf-8'))
        file = open("{}/PROPERTIES.md".format(self.dir), 'w+', encoding='utf-8')
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- orderNo : {}\n".format(self.order))
            file.write("- objDefId : {}\n".format(self.obj_type_id))
            file.write("- pageId : {}\n".format(self.page_id))
            file.write("- nextStatusId : {}\n".format(self.next_stauts_id))
            file.write("- isGroup : {}\n".format(self.is_group))
            file.write("- objTypeId : {}\n".format(self.obj_type_id))

            # Propriétés
            if self.properties:
                file.write("\n\n## Properties\n")
                for el in self.properties["children"]:
                    file.write("- {} : {}\n".format(el.__dict__["_name"], el.__dict__["cdata"]))
            
