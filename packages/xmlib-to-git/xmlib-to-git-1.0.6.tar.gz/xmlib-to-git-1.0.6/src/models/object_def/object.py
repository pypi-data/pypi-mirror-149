# object.py
import json
import os
from src import settings
from src.models.batch_job import creates_batchs
from src.models.object_def.action import creates_actions
from src.models.object_def.button import creates_buttons
from src.models.object_def.chart import creates_charts
from src.models.object_def.conversion import creates_conversions
from src.models.object_def.event import creates_events
from src.models.object_def.field import creates_fields
from src.models.object_def.process import creates_processes
from src.models.object_def.status import creates_statuses
from src.models.object_def.template import creates_templates
from src.models.object_def.view import creates_views
from src.models.translation import creates_translations
from src.utils import my_json, split_tool
from .relationship import creates_relationships


def creates_object_defs(objects):
    # objets de l'application
    for appObject in objects:
        new_object = Object(appObject)
        new_object.create()


class Object(object):

    """
    définition d'un object
    comporte liste de 'fields'
    """

    description = ""
    is_managed = ""
    def_process = ""
    audit_view = ""
    audit_create = ""
    audit_delete = ""
    audit_edit = ""
    enable_reports = ""
    show_tags = ""
    goog_synch = ""
    translations = ""
    relations = ""
    views = ""
    events = ""
    menus = ""
    processes = ""
    statuses = ""
    actions = ""
    conversions = ""
    buttons = ""
    templates = ""
    charts = ""
    is_localized = ""

    def __init__(self, data):
        self.id = data["id"]
        self.orig_id = data["origId"]
        self.name = split_tool.split_name(data.SingularName.cdata)
        self.def_name = data["objDefName"]
        self.is_system = data["isSystem"]
        self.is_auditable = data["isAuditable"]
        self.is_viewable = data["isViewable"]
        self.is_flagdable = data["isFlaggable"]
        self.is_dependent = data["isDependent"]
        self.is_deployed = data["isDeployed"]
        self.obj_directory = "{}/objects/{}".format(settings.APP_DIR, self.def_name)
        self.data = data

        # id -> origin id
        json_path = os.path.join(settings.SRC_DIR, "utils", "id_dict.json")
        file_id = json.load(open(json_path))
        obj = my_json.find_id_json(file_id, self.id)
        if not obj:
            file_id[self.id] = self.orig_id

        jsontest = json.dumps(file_id)
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(jsontest)

        # obj_dict
        json_dict = os.path.join(settings.SRC_DIR, "utils", "objects_dict.json")
        file_dict = json.load(open(json_dict))
        obj = my_json.find_id_json(file_dict, self.id)
        if not obj:
            inner_data = {
                "origId": self.orig_id,
                "name": self.name,
                "defName": self.def_name,
            }
            file_dict[self.id] = inner_data
            file_dict[self.orig_id] = inner_data

        jsontest = json.dumps(file_dict)
        with open(json_dict, "w", encoding="utf-8") as f:
            f.write(jsontest)

    def create(self):
        """
        Ecrit dans des fichiers les paramètres de l'obejt
        - PROPERTIES.md avec les infos techniques
        - RELATIONSHIP.md avec les relations
        - VIEWS.md avec les définitions des view
        - TRANSLATIONS.yml pour les traductions de l'objet
        - un dossier par champ dans le dossier fields
        - un dossier par déclencheur dans le dossier triggers
        :return:

        """
        if not os.path.exists(self.obj_directory.encode("utf-8")):
            os.makedirs(self.obj_directory.encode("utf-8"))

        data = self.data
        dir = self.obj_directory

        if hasattr(data, "Description"):
            self.description = data.Description.cdata
        if hasattr(data, "Props"):
            if hasattr(data.Props, "isManaged"):
                self.is_managed = data.Props.isManaged.cdata
            if hasattr(data.Props, "defProcess"):
                self.def_process = data.Props.defProcess.cdata
            if hasattr(data.Props, "auditView"):
                self.audit_view = data.Props.auditView.cdata
            if hasattr(data.Props, "auditCreate"):
                self.audit_create = data.Props.auditCreate.cdata
            if hasattr(data.Props, "auditDelete"):
                self.audit_delete = data.Props.auditDelete.cdata
            if hasattr(data.Props, "auditEdit"):
                self.audit_edit = data.Props.auditEdit.cdata
            if hasattr(data.Props, "enableReports"):
                self.enable_reports = data.Props.enableReports.cdata
            if hasattr(data.Props, "showTags"):
                self.show_tags = data.Props.showTags.cdata
            if hasattr(data.Props, "googSynch"):
                self.goog_synch = data.Props.googSynch.cdata
            if hasattr(data.Props, "deleteFormulaBase64"):
                self.delete_formula = data.Props.deleteFormulaBase64.cdata
            if hasattr(data.Props, "isLocalized"):
                self.is_localized = data.Props.isLocalized.cdata

        if hasattr(data, "Translations"):
            if hasattr(data.Translations, "Translation"):
                creates_translations(data.Translations.Translation, dir)

        if hasattr(data, "RelationshipDefs"):
            if hasattr(data.RelationshipDefs, "RelationshipDef"):
                creates_relationships(data.RelationshipDefs.RelationshipDef, dir)

        if hasattr(data, "ListViews"):
            creates_views(data.ListViews.ListView, dir)

        if hasattr(data, "Events"):
            creates_events(data.Events.Event, dir)

        if hasattr(data, "Actions"):
            creates_actions(data.Actions.Action, dir)

        if hasattr(data, "Statuses"):
            creates_statuses(data.Statuses.Status, dir)

        if hasattr(data, "Processes"):
            creates_processes(data.Processes.Process, dir)

        if hasattr(data, "Buttons"):
            creates_buttons(data.Buttons.Button, dir)

        if hasattr(data, "ConversionMaps"):
            if hasattr(data.ConversionMaps, "ImportMap"):
                creates_conversions(data.ConversionMaps.ImportMap, dir)

        if hasattr(data, "Charts"):
            creates_charts(data.Charts.Chart, dir)

        if hasattr(data, "Templates"):
            creates_templates(data.Templates.Template, dir)

        creates_fields(data.DataFieldDefs.DataFieldDef, dir)

    def creates_properties(self):
        # fichier de propriétés
        with open(
            "{}/PROPERTIES.md".format(self.obj_directory), "w+", encoding="utf-8"
        ) as file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Description
            if self.description:
                file.write("## Description\n")
                file.write(self.description)
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- objDef : {}\n".format(self.def_name))
            # Déploiement
            file.write("\nInfos déploiement :\n")
            file.write(
                "- [{}] isSystem \n".format("X" if self.is_system == "true" else " ")
            )
            file.write(
                "- [{}] isAuditable\n".format(
                    "X" if self.is_auditable == "true" else " "
                )
            )
            file.write(
                "- [{}] isViewable\n".format("X" if self.is_viewable == "true" else " ")
            )
            file.write(
                "- [{}] isFlaggable\n".format(
                    "X" if self.is_flagdable == "true" else " "
                )
            )
            file.write(
                "- [{}] isDependent\n".format(
                    "X" if self.is_dependent == "true" else " "
                )
            )
            file.write(
                "- [{}] isDeployed\n".format("X" if self.is_deployed == "true" else " ")
            )
            # Propriétés
            file.write("\nPropriétés :\n")
            if self.is_managed:
                file.write(
                    "- [{}] isManaged \n".format(
                        "X" if self.is_managed == "true" else " "
                    )
                )
            if self.def_process:
                file.write(
                    "- [{}] defProcess\n".format(
                        "X" if self.def_process == "1" else " "
                    )
                )
            if self.audit_view:
                file.write(
                    "- [{}] auditView\n".format(
                        "X" if self.audit_view == "true" else " "
                    )
                )
            if self.audit_create:
                file.write(
                    "- [{}] auditCreate\n".format(
                        "X" if self.audit_create == "true" else " "
                    )
                )
            if self.audit_delete:
                file.write(
                    "- [{}] auditDelete\n".format(
                        "X" if self.audit_delete == "true" else " "
                    )
                )
            if self.audit_edit:
                file.write(
                    "- [{}] auditEdit\n".format(
                        "X" if self.audit_edit == "true" else " "
                    )
                )
            if self.enable_reports:
                file.write(
                    "- [{}] enableReports\n".format(
                        "X" if self.enable_reports == "true" else " "
                    )
                )
            if self.show_tags:
                file.write(
                    "- [{}] showTags\n".format("X" if self.show_tags == "true" else " ")
                )
            if self.goog_synch:
                file.write(
                    "- [{}] googSync\n".format(
                        "X" if self.goog_synch == "true" else " "
                    )
                )
            if self.is_localized:
                file.write(
                    "- [{}] isLocalized\n".format(
                        "X" if self.is_localized == "true" else " "
                    )
                )
