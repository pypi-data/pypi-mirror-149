import datetime, os, json, unidecode, git
import shutil
from git import Repo, Actor, Commit
from src import settings

class GitRepo(object):
    
    repo = None
    origin = None
    
    def __init__(self, creation_time, version) -> None:
        print("version is {}".format(version))
        self.creation_time = creation_time
        self.version = version
        
    def del_files(self) -> None:
        if not os.path.exists(settings.APP_DIR.encode("utf-8")):
            os.makedirs(settings.APP_DIR.encode("utf-8"))
            
        # delete all files and folder to make git tracking easyest
        else:
            for f in os.listdir(settings.APP_DIR):
                # if not f.startswith('.'):
                if os.path.isfile("{}/{}".format(settings.APP_DIR, f)):
                    os.remove("{}/{}".format(settings.APP_DIR, f))
                else:
                    shutil.rmtree("{}/{}".format(settings.APP_DIR, f).encode("utf-8"))


    def check_git_exists(self) -> None:
        if not os.path.exists(settings.APP_DIR + "/.git"):
            # os.makedirs(self.app_directory)
            self.repo = Repo.init(settings.APP_DIR)
            self.origin = self.repo.create_remote(
                "origin", url=settings.GIT_REPO
            )
            # self.git_repo_obj\
            #     .create_head('master', self.git_origin.refs.master)\
            #     .set_tracking_branch(self.git_origin.refs.master)\
            #     .checkout()
        else:
            self.repo = Repo(settings.APP_DIR)
            self.origin = self.repo.remote("origin")
            self.origin
        self.origin.fetch()
        self.repo.remotes.origin.push("--all")

    def git_set_branch(self, customer_id=None) -> None:
        customer_name = "master"
        if customer_id:
            file_id = json.load(open("./src/utils/customer.json"))

            for i in file_id:
                if i["id"] == int(customer_id):
                    customer_name = (
                        i["name"].lower().replace(" ", "_").replace("-", "_")
                    )
                    break
            customer_name = unidecode.unidecode(customer_name)
        try:
            self.repo.git.checkout(customer_name)
        except git.exc.GitCommandError:
            self.repo.git.checkout("-b", customer_name)
        self.git_branch = customer_name

    def git_push(self) -> None:
        try:
            print("push")
            self.origin.push()
        except Exception as e:
            print('Some error occured while pushing the code : ' + str(e)) 

    def commit_tag_push(self) -> None:
        repo = self.repo
        # add all changes
        repo.git.add(A=True)
        # tree = repo.index.write_tree()

        # create commit with xml file's date

        # Committer and Author
        cr = repo.config_reader()
        committer = Actor.committer(cr)
        author = Actor.author(cr)

        date_creation = datetime.datetime.fromtimestamp(self.creation_time)
        date_creation_git = date_creation.replace(microsecond=0).isoformat()

        # offset = altzone
        # author_time, author_offset = date_creation, offset
        # committer_time, committer_offset = date_creation, offset

        message = "Commit automatique du " + date_creation.strftime("%d/%m/%Y")

        os.environ["GIT_AUTHOR_DATE"] = str(date_creation)
        os.environ["GIT_COMMITTER_DATE"] = str(date_creation)

        # Do the commit thing.
        commit = repo.index.commit(
            message,
            author=author,
            committer=committer,
            commit_date=date_creation_git,
            author_date=date_creation_git,
        )

        # Create TAG if version changed
        repo.remotes.origin.push(self.git_branch)
        tags = repo.tags
        if self.version not in tags:
            repo.create_tag(
                self.version, message='Automatic tag "{0}"'.format(self.version)
            )
            repo.remotes.origin.push(self.version)

        # Do the push
        repo.remotes.origin.push(self.git_branch)