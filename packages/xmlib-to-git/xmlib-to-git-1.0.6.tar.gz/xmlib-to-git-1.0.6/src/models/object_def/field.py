# field.py

import os
from .long import LongField
from .longarr import LongArrField
from .base import BaseField

def creates_fields(fields, obj_dir):
    # créer un dossier fields + nouveaux fields
    path = "{}/fields".format(obj_dir)
    if not os.path.exists(path.encode('utf-8')):
        os.makedirs(path.encode('utf-8'))
    for field_data in fields:
        # FieldLong
        if "FieldLong" in field_data["dataClassName"]:
            field = LongField(field_data, path)
        # FieldLongArr
        elif "FieldLongArr" in field_data["dataClassName"]:
            field = LongArrField(field_data, path)
        else:
            field = BaseField(field_data, path)
        if field != "":
            field.to_file()
            field.set_properties()
