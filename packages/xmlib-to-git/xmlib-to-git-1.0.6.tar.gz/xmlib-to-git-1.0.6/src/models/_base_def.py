# base_field.py

import base64
import binascii
import os
from src.models.translation import creates_translations
from src.models.object_def.workflow import creates_workflow
from src.utils import split_tool


class AField(object):
    """ "
    Blueprint for field

    Contains dir, id, origId, orderNo, objDefId, name, properties, ConditionB64, ScriptB64, Translation, Workflow
        ValidationB64
    Creates folder if not exists
    """

    name = None
    properties = None
    condition_base64 = None
    script_base64 = None
    validation_base64 = None
    translations = None
    workflow = None
    columns = None

    def __init__(self, data, path) -> None:
        self.id = data["id"]
        self.orig_id = data["origId"]
        self.obj_def_id = data["objDefId"]
        if hasattr(data, "objDef"):
            self.obj_def_id = data["objDef"]
        self.name = data["name"]
        if hasattr(data, "DisplayName"):
            self.name = data.DisplayName.cdata
        elif hasattr(data, "DisplayLabel"):
            self.name = data.DisplayLabel.cdata
        elif hasattr(data, "ViewName"):
            self.name = data.ViewName.cdata
        elif hasattr(data, "ChartName"):
            self.name = data.ChartName.cdata
        elif hasattr(data, "MapColumns"):
            self.name = data["mapName"]
        # if hasattr(data, "name"):

        self.dir = "{}/{}".format(path, split_tool.split_name(self.name))

        if hasattr(data, "Description"):
            self.description = data.Description.cdata

        if hasattr(data, "Props"):
            self.properties = data.Props.__dict__

        if hasattr(data, "ConditionB64"):
            self.condition_base64 = data.ConditionB64.cdata

        if hasattr(data, "ScriptB64"):
            self.scriscript_base64pt = data.ScriptB64.cdata

        if hasattr(data, "Translations"):
            if hasattr(data.Translations, "Translation"):
                self.translations = data.Translations.Translation

        if hasattr(data, "Workflow"):
            if hasattr(data.Workflow, "Node"):
                self.workflow = data.Workflow.Node

        if hasattr(data, "ValidationScriptB64"):
            self.validation_base64 = data.ValidationScriptB64.cdata

        if hasattr(data, "MapColumns"):
            if hasattr(data.MapColumns, "MapColumn"):
                self.columns = data.MapColumns.MapColumn

    def to_file(self) -> None:
        if not os.path.exists(self.dir.encode("utf-8")):
            os.makedirs(self.dir.encode("utf-8"))

        if self.translations:
            creates_translations(self.translations, self.dir)

        if self.workflow:
            creates_workflow(self.workflow, self.dir)

        if self.condition_base64:
            file = open("{}/condition.js".format(self.dir), "w+", encoding="utf-8")
            with file:
                file_content = base64.b64decode(self.condition_base64).decode(
                    "UTF-8", "ignore"
                )
                file.write(file_content)

        if self.script_base64:
            file = open("{}/script.js".format(self.dir), "w+", encoding="utf-8")
            with file:
                file_content = base64.b64decode(self.script_base64).decode(
                    "UTF-8", "ignore"
                )
                file.write(file_content)

        if self.validation_base64:
            file = open(
                "{}/validation_script.js".format(self.dir), "w+", encoding="utf-8"
            )
            with file:
                file_content = base64.b64decode(self.validation_base64).decode(
                    "UTF-8", "ignore"
                )
                file.write(file_content)

    def template(self, text):
        template = open("{}/template.js".format(self.dir), "w+", encoding="utf-8")
        with template:
            try:
                template_content = base64.b64decode(text).decode("UTF-8", "ignore")
                template.write(template_content)
            except binascii.Error:
                template.write(text)
            except ValueError:
                template.write(text)
