# processor.py

import shutil
import time
from src import settings
from src.utils import my_json
from src.git_tools.git_repo import GitRepo
import untangle, os, json
from src.models.application import Application


def parse_xml(xml) -> None:
    time_start = time.perf_counter()
    print("processing {}".format(xml))

    app_tree = untangle.parse(xml)
    date_creation_fichier = os.path.getmtime(xml)
    json_path = os.path.join(settings.SRC_DIR, "utils", "id_dict.json")
    file_id = json.load(open(json_path))

    # objets dépendants -> ajout dans la liste de référence
    if hasattr(app_tree.Application.DependentDefs, "DataObjectDef"):
        for DataObjectDef in app_tree.Application.DependentDefs.DataObjectDef:
            obj = my_json.find_id_json(file_id, DataObjectDef["id"])
            if not obj:
                file_id[DataObjectDef["id"]] = DataObjectDef["origId"]

        jsontest = json.dumps(file_id)
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(jsontest)

        del jsontest, f, file_id

    props = ""
    description = ""
    
    if hasattr(app_tree.Application, "Props"):
        props = app_tree.Application.Props

    if hasattr(app_tree.Application, "Description"):
        description = app_tree.Application.Description.cdata
    
    app = Application(
        app_tree.Application["id"],
        app_tree.Application["version"],
        app_tree.Application["packedId"],
        app_tree.Application.DisplayName.cdata,
        description,
        props,
        date_creation_fichier,
    )

    git_object = GitRepo(date_creation_fichier, app.version)
    
    if settings.GIT_REPO:
        git_object.del_files()
        git_object.check_git_exists()
        git_object.git_set_branch(settings.CUSTOMER)
    
    # creates Application basics
    app.to_file()
    
    del app

    # creates application Tokens
    if hasattr(app_tree.Application, "Props"):
        if hasattr(props, "tokenNames"):
            from src.models.token import creates_tokens
            creates_tokens(props.tokenNames.cdata)

    # creates custom logo
    if hasattr(app_tree.Application, "CustomLogo"):
        from src.models.logo import creates_logo
        creates_logo(app_tree.Application.CustomLogo.cdata, app_tree.Application.Props.appLogo.cdata)
        
    # PostInstallScriptB64
    if hasattr(app_tree.Application, "PostInstallScriptB64"):
        from src.models.install_script import creates_install_script
        creates_install_script(app_tree.Application.PostInstallScriptB64.cdata, "post_install_script")
    
    # PostAppInstallScriptB64
    if hasattr(app_tree.Application, "PostAppInstallScriptB64"):
        from src.models.install_script import creates_install_script
        creates_install_script(app_tree.Application.PostAppInstallScriptB64.cdata, "post_app_install_script")
        
    # PostAppUpdateScriptB64
    if hasattr(app_tree.Application, "PostAppUpdateScriptB64"):
        from src.models.install_script import creates_install_script
        creates_install_script(app_tree.Application.PostAppUpdateScriptB64.cdata, "post_update_script")
    
    # creates application Dependent Object
    if hasattr(app_tree.Application, "DependentDefs"):
        if hasattr(app_tree.Application.DependentDefs, "DataObjectDef"):
            from src.models.dependent import creates_dependents
            creates_dependents(app_tree.Application.DependentDefs.DataObjectDef)
    
    # creates menus
    if hasattr(app_tree.Application, "Menus"):
        if hasattr(app_tree.Application.Menus, "Menu"):
            from src.models.menu import creates_menus
            creates_menus(app_tree.Application.Menus.Menu)
    
    # creates hosted files 
    if hasattr(app_tree.Application, "HostedFiles"):
        from src.models.hosted_file import create_hosted_files
        create_hosted_files(app_tree.Application.HostedFiles.HostedFile)
            
    # creates Web pages
    if hasattr(app_tree.Application, "WebPageDefs"):
        from src.models.webpagedef import creates_web_pages
        creates_web_pages(app_tree.Application.WebPageDefs.WebPageDef)

    # creates Portals
    if hasattr(app_tree.Application, "Portals"):
        if hasattr(app_tree.Application.Portals, "WebSite"):
            from src.models.portal import creates_portals
            creates_portals(app_tree.Application.Portals.WebSite)

    # creates Seed Records
    if hasattr(app_tree.Application, "SeedRecords"):
        from src.models.seedrecord import creates_seeds
        creates_seeds(app_tree.Application.SeedRecords.DataObject)

    # creates Batch jobs
    if hasattr(app_tree.Application, "BatchJobs"):
        if hasattr(app_tree.Application.BatchJobs, "Event"):
           from src.models.batch_job import creates_batchs
           creates_batchs(app_tree.Application.BatchJobs.Event)
            
    # creates Custom methods
    if hasattr(app_tree.Application, "CustomMethods"):
        if hasattr(app_tree.Application.CustomMethods, "CustomMethod"):
            from src.models.custom_method import creates_custom_methods
            creates_custom_methods(app_tree.Application.CustomMethods.CustomMethod)
    
    # creates Custom Reports
    if hasattr(app_tree.Application, "CustomReports"):
        if hasattr(app_tree.Application.CustomReports, "CustomReport"):
            pass
            # TODO: creates_custom_reports(Application.CustomReports.CustomReport)
           
    # creates Permissions
    if hasattr(app_tree.Application, "Permissions"):
        if hasattr(app_tree.Application.Permissions, "Permission"):
            from src.models.permission import creates_permissions
            creates_permissions(app_tree.Application.Permissions.Permission)
           
    # creates RolePages
    if hasattr(app_tree.Application, "RolePages"):
        if hasattr(app_tree.Application.RolePages, "RolePage"):
            from src.models.role_page import creates_role_pages
            creates_role_pages(app_tree.Application.RolePages.RolePage)

    # creates Translations
    if hasattr(app_tree.Application, "Translations"):
        if hasattr(app_tree.Application.Translations, "Translation"):
            from src.models.translation import creates_translations
            creates_translations(app_tree.Application.Translations.Translation)

    # creates  Objects in the end
    if hasattr(app_tree.Application, "DataObjectDefs"):
        if hasattr(app_tree.Application.DataObjectDefs, "DataObjectDef"):
            from src.models.object_def.object import creates_object_defs
            creates_object_defs(app_tree.Application.DataObjectDefs.DataObjectDef)
            
    text_file = "{}/app.xml".format(settings.APP_DIR.rstrip("/"))
    shutil.copy(xml, text_file)

    if settings.GIT_REPO:
        git_object.commit_tag_push()
        git_object.git_set_branch()
        git_object.git_push()
        pass

    time_elapsed = time.perf_counter() - time_start

    print(
        "application '{}' generated in {}s".format(
            app_tree.Application.DisplayName.cdata, round(time_elapsed, 2)
        )
    )
