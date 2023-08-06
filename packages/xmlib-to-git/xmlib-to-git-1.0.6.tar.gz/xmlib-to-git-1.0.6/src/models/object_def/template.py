# template.py
import os
import base64
from src.models._base_def import AField
from src.utils import split_tool

def creates_templates(templates, obj_dir) -> None:
    path = "{}/templates".format(obj_dir)
    if not os.path.exists(path.encode('utf-8')):
        os.makedirs(path.encode('utf-8'))
    for template_data in templates:
        template = Template(template_data, path)
        template.to_file()

class Template(AField):
    """
    Define a template
    """
    raw_data = ""
    body = ""
    props = ""

    def __init__(self, data, path):
        super().__init__(data, path)
        self.type = data["type"]
        self.name = data["name"]
        self.content_type = data["contentType"]
        self.obj_type_id = data["objTypeId"]
        if self.type == "mail":
            self.subject = data.Subject.cdata
            self.body = data.Body.cdata
        if self.type == "doc":
            self.raw_data = data.RawData.cdata
            

    def to_file(self):
        super().to_file()
        # properties file

        file = open("{}/PROPERTIES.md".format(self.dir), 'w+', encoding='utf-8')
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- objDef : {}\n".format(self.obj_def_id))
            file.write("- type : {}\n".format(self.type))
            file.write("- contentType : {}\n".format(self.content_type))
            file.write("- objTypeId : {}\n".format(self.obj_type_id))

            if self.properties:
            # Properties
                file.write("\n\n## Properties\n")
                for el in self.properties["children"]:
                    if((el.__dict__["_name"] != "Body" or el.__dict__["_name"] != "RawData") ) and (el.__dict__["_name"] != "Props"):
                        file.write("- {} : {}\n".format(el.__dict__["_name"], el.__dict__["cdata"]))


        if self.body:
            file = open("{}/body.html".format(self.dir), 'w+', encoding='utf-8')
            with file:
                file_content = base64.b64decode(self.body).decode("UTF-8", "ignore")
                file.write(file_content)
        
        if self.raw_data:
            name = "doc"
            if "text/plain" in self.content_type:
                name = name + ".txt"
            elif "application/vnd.ms-excel" in self.content_type:
                name = name + ".xlsx"
            elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in self.content_type:
                name = name + ".docx"
            elif "application/msword" in self.content_type:
                name = name + ".doc"
            elif "application/msexcel" in self.content_type:
                name = name + ".xls"
            elif "text/xml" in self.content_type:
                name = name + ".xml"
            elif "application/pdf" in self.content_type:
                name = name + ".pdf"
            elif "text/html" in self.content_type:
                name = name + ".html"
            file = open("{}/{}".format(self.dir, name), 'w+', encoding='utf-8')
            # TODO: le fichier est mal créer et est illisible
            with file:
                file_content = base64.b64decode(self.raw_data).decode("UTF-8", "ignore")
                file.write(file_content)