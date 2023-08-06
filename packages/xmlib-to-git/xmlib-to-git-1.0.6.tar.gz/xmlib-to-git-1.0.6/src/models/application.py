# -*- coding: utf-8 -*-

import base64, os, shutil, json, datetime, unidecode, git
from src.utils import my_json
from src import settings

class Application(object):
    """
    Top node application
    """

    header = ""
    footer = ""
    token_names = ""
    git_repo_obj = ""
    git_origin = ""
    git_branch = ""
    show_menus = ""
    use_legacy_header_footer = ""
    is_hidden = ""
    help_field = ""
    is_deployed = ""
    is_managed = ""
    pub_managed = ""
    is_logo_hidden = ""

    def __init__(
        self,
        id,
        version,
        packed_id,
        displayname,
        description,
        properties,
        creation_date,
    ) -> None:
        self.id = id
        self.version = version
        self.packed_id = packed_id
        self.displayname = displayname
        self.description = description
        if hasattr(properties, "showMenus"):
            self.show_menus = properties.showMenus.cdata
        if hasattr(properties, "useLegacyHeaderFooter"):
            self.use_legacy_header_footer = properties.useLegacyHeaderFooter.cdata
        if hasattr(properties, "isHidden"):
            self.is_hidden = properties.isHidden.cdata
        if hasattr(properties, "helpField"):
            self.help_field = properties.helpField.cdata
        if hasattr(properties, "isDeployed"):
            self.is_deployed = properties.isDeployed.cdata
        if hasattr(properties, "isManaged"):
            self.is_managed = properties.isManaged.cdata
        if hasattr(properties, "header"):
            self.header = base64.b64decode(properties.header.cdata)
        if hasattr(properties, "pubManaged"):
            self.pub_managed = properties.pubManaged.cdata
        if hasattr(properties, "isLogoHidden"):
            self.is_logo_hidden = properties.isLogoHidden.cdata
        if hasattr(properties, "dependentDefs"):
            self.dependent_defs = properties.dependentDefs.cdata
        if hasattr(properties, "footer"):
            self.footer = base64.b64decode(properties.footer.cdata)
        self.creation_date = creation_date
        
    def version(self) -> str:
        return self.version
        

    def to_file(self) -> None:
        """
        Write in files application's parameters
        - README.md -> technical informations
        - header.js -> header
        - footer.js -> footer
        :return:
        """
        readme = open("{}/README.md".format(settings.APP_DIR), "w+", encoding="utf-8")
        with readme:
            # nom de l'src
            readme.write("# {}\n".format(self.displayname))
            readme.write("version {}\n\n".format(self.version))
            # Description
            readme.write("## Description\n")
            readme.write(self.description)
            # Informations
            readme.write("\n\n## Informations\n")
            readme.write("- id : {}\n".format(self.id))
            readme.write("- packedId : {}\n".format(self.packed_id))
            readme.write("\nInfos déploiement :\n")
            readme.write(
                "- [{}] showMenu \n".format("X" if self.show_menus == "true" else " ")
            )
            readme.write(
                "- [{}] useLegacyHeaderFooter\n".format(
                    "X" if self.use_legacy_header_footer == "true" else " "
                )
            )
            readme.write(
                "- [{}] isHidden\n".format("X" if self.is_hidden == "true" else " ")
            )
            readme.write(
                "- [{}] helpField\n".format("X" if self.help_field == "true" else " ")
            )
            readme.write(
                "- [{}] isDeployed\n".format("X" if self.packed_id == "true" else " ")
            )

        if self.header:
            header = open(
                "{}/header.html".format(settings.APP_DIR), "w+", encoding="utf-8"
            )
            with header:
                header.write(self.header.decode("utf-8"))

        if self.footer:
            footer = open(
                "{}/footer.html".format(settings.APP_DIR), "w+", encoding="utf-8"
            )
            with footer:
                footer.write(self.footer.decode("utf-8"))
                