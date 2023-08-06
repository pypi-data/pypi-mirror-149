# event.py
import os
from src.models._base_def import AField


def creates_events(events, obj_dir) -> None:
    # créer un dossier events + nouveaux events
    path = "{}/events".format(obj_dir)
    if not os.path.exists(path.encode("utf-8")):
        os.makedirs(path.encode("utf-8"))
    from .event import Event

    for event in events:
        new_event = Event(event, path)
        new_event.to_file()


class Event(AField):
    """
    Define an event
    """

    script = ""

    def __init__(self, data, path) -> None:
        super().__init__(data, path)
        self.order = data["orderNo"]
        self.config_id = data["configId"]
        self.name = data["name"]
        self.on_what = data["onWhat"]  # sur quel origId d'un objet
        self.relative_to_id = data["relativeToId"]
        self.delay = data["delay"]
        self.template_id = data["templateId"]
        self.change_field_id = data["changeFieldId"]
        self.id_deployed = data["isDeployed"]

    def to_file(self) -> None:
        super().to_file()
        # properties file
        if not os.path.exists(self.dir.encode("utf-8")):
            os.makedirs(self.dir.encode("utf-8"))
        file = open("{}/PROPERTIES.md".format(self.dir), "w+", encoding="utf-8")
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- objDef : {}\n".format(self.obj_def_id))
            file.write("- configId : {}\n".format(self.id))
            file.write(
                "- onWhat : {}\n".format(self.orig_id)
            )  # TODO : trouver le nom dans un dict
            file.write("- relativeTo : {}\n".format(self.relative_to_id))  # TODO: idem
            file.write("- delay : {}\n".format(self.delay))
            file.write("- templateId : {}\n".format(self.template_id))  # TODO: idem
            file.write(
                "- changeField : {}\n".format(self.change_field_id)
            )  # TODO: idem

            # Properties
            file.write("\n\n## Properties\n")
            for el in self.properties["children"]:
                if (el.__dict__["_name"] != "ConditionB64") and (
                    el.__dict__["_name"] != "Props"
                ):
                    file.write(
                        "- {} : {}\n".format(el.__dict__["_name"], el.__dict__["cdata"])
                    )

            if self.properties:
                for el in self.properties["children"]:
                    if el.__dict__["_name"] == "template":
                        if el.__dict__["cdata"] != self.script:
                            self.template(el.__dict__["cdata"])
                    else:
                        file.write(
                            "- {} : {}\n".format(
                                el.__dict__["_name"], el.__dict__["cdata"]
                            )
                        )
