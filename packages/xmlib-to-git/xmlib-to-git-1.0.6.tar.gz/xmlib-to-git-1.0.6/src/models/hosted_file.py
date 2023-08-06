# hosted_file.py

from src import settings
import os, base64

def create_hosted_files(files):
    ### HOSTED FILES
    hosted_files_dir = "{}/hosted_files".format(settings.APP_DIR)
    for file in files:
        if not os.path.exists(hosted_files_dir.encode("utf-8")):
            os.mkdir(hosted_files_dir.encode("utf-8"))
            os.mkdir("{}/css".format(hosted_files_dir).encode("utf-8"))
            os.mkdir("{}/js".format(hosted_files_dir).encode("utf-8"))
            os.mkdir("{}/images".format(hosted_files_dir).encode("utf-8"))

        folder = ""
        ext = ""
        is_image = False

        if file["contentType"] == "text/css":
            folder = ext = "css"
        elif file["contentType"] == "application/javascript":
            folder = ext = "js"
        elif file["contentType"] == "application/x-javascript":
            folder = "js"
            ext = "min.js"
        elif file["contentType"] == "image/png":
            folder = "images"
            ext = "png"
            is_image = True
        elif file["contentType"] == "image/jpeg":
            folder = "images"
            ext = "jpg"
            is_image = True

        if folder and not is_image:
            with open(
                "{}/{}/#HOSTED_FILE.{}-{}.{}".format(
                    hosted_files_dir,
                    folder,
                    file["origId"],
                    file.DisplayName.cdata.replace("/", "-")
                    .replace(" ", "_")
                    .replace("\\", "-")
                    .replace("&", "")
                    .replace("!", ""),
                    ext,
                ),
                "w+",
                encoding="utf-8",
            ) as readme:
                file_content = base64.b64decode(file.RawData.cdata).decode(
                    "iso8859_15", "ignore"
                )
                readme.write(file_content)
        elif folder and is_image:
            with open(
                "{}/{}/#HOSTED_FILE.{}-{}.{}".format(
                    hosted_files_dir,
                    folder,
                    file["origId"],
                    file.DisplayName.cdata.replace("/", "-")
                    .replace(" ", "_")
                    .replace("\\", "-")
                    .replace("&", "")
                    .replace("!", ""),
                    ext,
                ),
                "wb",
            ) as readme:
                if hasattr(file, "RawData"):
                    file_content = base64.b64decode(file.RawData.cdata)
                    readme.write(file_content)