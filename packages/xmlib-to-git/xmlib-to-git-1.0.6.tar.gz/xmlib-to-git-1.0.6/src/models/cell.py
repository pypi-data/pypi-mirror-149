# -*- coding: utf-8 -*-
import base64, os

# TODO: cell js en fonction du type de cell
class Cell(object):
    """

    """

    properties = ""
    script = ""

    def __init__(self, cell, section_directory):
        self.id = cell["id"]
        self.orig_id = cell["origId"]
        self.section_id = cell["sectionId"]
        self.order_no = cell["orderNo"]
        self.alignment = cell["alignment"]
        self.field_id = cell["fieldId"]
        self.cell_class_name = cell["cellClassName"].split('.')[-1]
        self.cell_directory = "{}".format(section_directory)
        if hasattr(cell, "Props"):
            self.properties = cell.Props.__dict__
        if hasattr(cell, "TextB64"):
            self.script = cell.TextB64.cdata

    def to_file(self):
        # fichier de propriétés
        # if not os.path.exists(self.cell_directory):
        #     os.makedirs(self.cell_directory)
        with open("{}/_cell_{}.md".format(self.cell_directory, self.order_no), 'w+', encoding='utf-8') as file:
            # nom de l'objet
            file.write("# {}\n".format(self.cell_class_name))

            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- sectionId : {}\n".format(self.section_id))
            file.write("- orderNo : {}\n".format(self.order_no))
            file.write("- alignment : {}\n".format(self.alignment))
            file.write("- fieldId : {}\n".format(self.field_id))
            file.write("- cellClassName : {}\n".format(self.cell_class_name))

            # Propriétés
            if self.properties:
                for el in self.properties["children"]:
                    file.write("- {} : {}\n".format(el.__dict__["_name"], el.__dict__["cdata"]))
        decoded = base64.b64decode(self.script).decode("utf-8")
        if self.script and self.cell_class_name == "TemplateHTML":
            self.create_code("html", decoded)
        if self.script and self.cell_class_name == "ScriptControl": 
            if "<script" in decoded or "<style" in decoded:
                self.create_code("js", decoded)
            else:
                self.create_code("html", decoded)

    def create_code(self, ext, decoded):
        with open("{}/_cell_{}.{}".format(self.cell_directory, self.order_no, ext), 'w+', encoding='utf-8') as script:
            script.write(decoded)
