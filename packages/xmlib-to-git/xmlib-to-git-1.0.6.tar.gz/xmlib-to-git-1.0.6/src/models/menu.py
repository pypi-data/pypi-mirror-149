# meny.py

import os, re
from src.utils import split_tool
from src import settings

def creates_menus(menus):
    # Create a menu folder + menus
    # create a file MENUS.md with tree menu
    path = "{}/menus".format(settings.APP_DIR)
    if not os.path.exists(path.encode("utf-8")):
        os.makedirs(path.encode("utf-8"))
    menu_file = open(
        "{}/MENUS.md".format(settings.APP_DIR), "w+", encoding="utf-8"
    )
    menu_file.write("## Menus\n\n```\n.\n")
    for menu in menus:
        new_menu = Menu(menu, path)
        new_menu.to_file()
        menu_file.write(new_menu.get_menus(menus))
    menu_file.write("```\n")

class Menu(object):
    """
        Défini un menu Rollase
        """
    translations = ""
    sub_menus = ""

    def __init__(self, menu, dir):
        self.id = menu["id"]
        self.orig_id = menu["origId"]
        self.order = menu["orderNo"]
        self.obj_def = menu["objDef"]
        self.parent_id = menu["parentId"]
        self.page_def_id = menu["pageDefId"]
        self.name = menu.DisplayName.cdata
        if hasattr(menu, "Translations"):
            if hasattr(menu.Translations, "Translation"):
                self.translations = menu.Translations.Translation
        if hasattr(menu, "Menus"):
            if hasattr(menu.Menus, "Menu"):
                self.sub_menus = menu.Menus.Menu
        dirname = split_tool.split_name(self.name)
        self.menu_dir = "{}/{}".format(dir, dirname)

    def to_file(self):
        # fichier de propriétés
        if not os.path.exists(self.menu_dir.encode('utf-8')):
            os.makedirs(self.menu_dir.encode('utf-8'))
        file = open("{}/PROPERTIES.md".format(self.menu_dir), 'w+', encoding='utf-8')
        with file:
            # nom de l'objet
            file.write("# {}\n".format(self.name))
            # Informations
            file.write("\n\n## Informations\n")
            file.write("- id : {}\n".format(self.id))
            file.write("- origId : {}\n".format(self.orig_id))
            file.write("- objDef : {}\n".format(self.obj_def))
            file.write("- parentId : {}\n".format(self.parent_id))
            file.write("- orderNo : {}\n".format(self.order))

            if self.translations:
                file.write("\n## Traductions\n")
                file.write("|code|nom|text|\n")
                file.write("|---|---|---|\n")
                for trans in self.translations:
                    file.write("|{}|{}|{}|\n".format(trans["langCode"], trans["fieldName"], trans["text"]))

            if self.sub_menus:
                file.write("\n## Sub menus\n```\n")
                file.write(".\n|-- {}\n".format(self.name))
                for sub_menu in self.sub_menus:
                    new_menu = Menu(sub_menu, self.menu_dir)
                    new_menu.to_file()
                    file.write("|   |-- {}\n".format(new_menu.name))
                file.write("```\n")

    def get_menus(self, menus):
        menu_string = ""
        if self.sub_menus:
            menu_string += "|-- {}\n".format(self.name)
            for sub_menu in self.sub_menus:
                new_menu = Menu(sub_menu, self.menu_dir)
                menu_string += "|   |-- {}\n".format(new_menu.name)
                if hasattr(new_menu, "menus"):
                    if new_menu.sub_menus:
                        menu_string += new_menu.get_menus(new_menu.menus)
        return menu_string
