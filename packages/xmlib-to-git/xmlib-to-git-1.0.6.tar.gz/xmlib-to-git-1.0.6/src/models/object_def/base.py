# base.py
import base64
from PIL import Image
from io import BytesIO

from src.models._base_def import AField


class BaseField(AField):
    """Classe générique pour définir un champ d'un objet
    - Infos
    - DisplayLabel
    - Description
    - traductions
    - propriétés (liste d'éléments Props)
    """

    list_items = ""
    validation_script = ""
    formula_script = ""
    group_name = ""
    shared_image_name = ""
    shared_image_data = ""

    def __init__(self, data, path) -> None:
        super().__init__(data, path)

        self.column_name = data["columnName"]
        self.field_name = data["fieldName"]
        self.data_class_name = data["dataClassName"]
        self.ui_class_name = data["uiClassName"].split(".")[-1]
        self.is_required = data["isRequired"]
        self.is_read_only = data["isReadOnly"]
        self.is_text_indexable = data["isTextIndexable"]
        self.is_system = data["isSystem"]
        self.is_auditable = data["isAuditable"]
        self.has_permissions = data["hasPermissions"]
        self.max_length = data["maxLength"]
        self.dir = "{}/{}/{}".format(path, self.ui_class_name, self.field_name)

        if hasattr(data, "groupeName"):
            self.group_name = data["groupName"]

        if hasattr(data, "ListItems"):
            self.list_items = data.ListItems.ListItem

        if hasattr(data, "ImageData"):
            self.shared_image_data = data.ImageData.cdata

    def to_file(self) -> None:
        super().to_file()
        with open("{}/PROPERTIES.md".format(self.dir), "w+", encoding="utf-8") as file:
            file.write("## {}\n".format(self.name))
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- objDef : {}\n".format(self.obj_def_id))
            file.write("- columnName : {}\n".format(self.column_name))
            file.write("- fieldName : {}\n".format(self.field_name))
            if self.group_name:
                file.write("- groupName : {}\n".format(self.group_name))
            file.write("- dataClassName : {}\n".format(self.data_class_name))
            file.write("- uidClassName : {}\n".format(self.ui_class_name))
            file.write("- isRequired : {}\n".format(self.is_required))
            file.write("- isReadOnly : {}\n".format(self.is_read_only))
            file.write("- isTextIndexable : {}\n".format(self.is_text_indexable))
            file.write("- isSystem : {}\n".format(self.is_system))
            file.write("- isAuditable : {}\n".format(self.is_auditable))
            file.write("- hasPermissions : {}\n".format(self.has_permissions))
            file.write("- maxLength : {}\n".format(self.max_length))

            # Translations
            if self.translations:
                file.write("## Traductions\n")
                file.write("|code|nom|texte|\n")
                file.write("|---|---|---|\n")
                for trans in self.translations:
                    file.write(
                        "|{}|{}|{}|\n".format(
                            trans["langCode"], trans["fieldName"], trans["text"]
                        )
                    )

    def set_properties(self):
        if self.properties:
            with open(
                "{}/PROPERTIES.md".format(self.dir), "a+", encoding="utf-8"
            ) as file:
                file.write("## Propriétés\n")
                for el in self.properties["children"]:
                    if el.__dict__["_name"] == "templateB64":
                        with open(
                            "{}/template.html".format(self.dir), "w+", encoding="utf-8"
                        ) as template:
                            template.write(
                                base64.b64decode(el.__dict__["cdata"]).decode("utf-8")
                            )
                    elif el.__dict__["_name"] == "formulaB64":
                        with open(
                            "{}/formula.js".format(self.dir), "w+", encoding="utf-8"
                        ) as formula:
                            formula.write(
                                base64.b64decode(el.__dict__["cdata"]).decode("utf-8")
                            )
                    elif el.__dict__["_name"] == "linkTemplB64":
                        with open(
                            "{}/link.html".format(self.dir), "w+", encoding="utf-8"
                        ) as link:
                            link.write(
                                base64.b64decode(el.__dict__["cdata"]).decode("utf-8")
                            )
                    elif el.__dict__["_name"] == "sharedImage":
                        self.shared_image_name = "{}.{}".format(
                            self.name, el.__dict__["cdata"].split(".")[-1]
                        )
                        im = Image.open(
                            BytesIO(base64.b64decode(self.shared_image_data))
                        )
                        im.save(
                            "{}/{}".format(self.dir, self.shared_image_name),
                            el.__dict__["cdata"].split(".")[-1],
                        )
                    else:
                        file.write(
                            "- {} : {}\n".format(
                                el.__dict__["_name"], el.__dict__["cdata"]
                            )
                        )
