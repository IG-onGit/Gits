from imports import *


class index:
    ####################################################################################// Load
    def __init__(self, app="", cwd="", args=[]):
        self.app, self.cwd, self.args = app, cwd, args

        if platform.system() != "Windows":
            cli.error("XAMPHP is currently available only for Windows users")
            sys.exit()

        self.sources = f"{self.app}/.system/sources"
        self.storage = self.__catalog()
        pass

    def __exit__(self):
        # ...
        pass

    ####################################################################################// Main
    def connect(self):  # Setup new ssh connection
        key = GitSSH.newUser("gits", self.sources, self.storage)
        if not key:
            return "SSH key generation failed!"

        print()
        cli.hint("Add this SSH key to your service:\n" + attr("reset") + key)

        return "Connection added successfully"

    def clone(self, url=""):  # (ssh-url) - Clone project from GitHub / GitLab
        if not url.strip() or url[-4:] != ".git":
            return "Invalid ssh-url!"

        if cli.isFolder(f"{self.cwd}/.git"):
            return "Folder is already taken!"

        if not GitSSH.cloneProject(self.cwd, url):
            return "Cloning failed!"

        return "Project clonned successfully"

    def show(self):  # List existing connections
        exists = False
        for item in os.listdir(self.storage):
            if not item or item in ["__pycache__"]:
                continue
            cli.hint(item)
            exists = True

        if not exists:
            return "No connections!"
        pass

    def drop(self, username=""):  # (user-name) - Drop connection
        if not username.strip():
            return "Invalid user-name!"

        if not GitSSH.dropUser("gits", self.storage, username):
            return "Dropping connection failed!"

        return "Connection dropped successfully"

    ####################################################################################// Helpers
    def __catalog(self):
        osuser = os.environ.get("USERNAME")
        if not osuser.strip():
            cli.error("Could not read OS username")
            sys.exit()

        folder = f"C:/Users/{osuser}/.gits"
        os.makedirs(folder, exist_ok=True)

        return folder
