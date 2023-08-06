# logo.py

from src import settings
import base64

def creates_logo(encoded_str, name):
    ext = name.split('.')[1]
    with open("{}/logo.{}".format(settings.APP_DIR, ext), "wb") as file:
        file_content = base64.b64decode(encoded_str)
        file.write(file_content)