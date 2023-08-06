from src import settings
import base64

def creates_install_script(encoded_str, name):
    with open("{}/{}.js".format(settings.APP_DIR, name), "wb") as file:
        file_content = base64.b64decode(encoded_str)
        file.write(file_content)
        