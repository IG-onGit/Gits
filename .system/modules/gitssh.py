from imports import *


class GitSSH:
    ####################################################################################// Load
    def __init__(self, cliname="", sources="", storage=""):
        self.config = self.__setupDir()
        self.cliname = cliname
        self.sources = sources
        self.storage = storage
        self.ssh_key = ""
        self.ssh_rsa = ""
        pass

    ####################################################################################// Main
    def newUser(cliname="", sources="", storage=""):
        if not cliname or not os.path.exists(sources) or not os.path.exists(storage):
            return False

        obj = GitSSH(cliname, sources, storage)
        obj.__newUser()

        return obj.ssh_rsa

    def dropUser(cliname="", storage="", user=""):
        if not cliname or not os.path.exists(storage) or not user:
            return False

        obj = GitSSH(cliname, "", storage)

        return obj.__dropUser(user)

    def cloneProject(current="", link=""):
        if not os.path.exists(current) or not link:
            return False

        obj = GitSSH("", "", "")

        return obj.__cloneProject(current, link)

    ####################################################################################// Helpers
    def __setupDir(self):
        username = os.environ.get("USERNAME")
        folder = f"C:/Users/{username}/.ssh"

        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        return f"{folder}/config"

    def __newUser(self):
        sshdir = os.path.dirname(self.config)
        if not os.path.exists(sshdir):
            cli.error("Invalid ssh dir")
            return False

        info = {}
        for item in self.__interface():
            value = ""
            while not value:
                value = input(f"{item}: ")
            info[item] = value

        info["cliname"] = self.cliname
        info["storage"] = self.storage.replace("\\", "/")

        user = info["user"]
        service = info["service"]
        key_file = os.path.join(self.storage, f"{service}_{user}")
        if os.path.exists(key_file):
            cli.error("User already exists")
            return False

        content = ""
        if os.path.exists(self.config):
            content = cli.read(self.config).strip()

        template_file = os.path.join(self.sources, "sshconfig")
        if not os.path.exists(template_file):
            cli.error("Invalid template")
            return False

        ssh = self.__sshKeys(key_file)
        if not ssh:
            cli.error("Invalid ssh keys")
            return False

        self.ssh_key = ssh["key"]
        self.ssh_rsa = ssh["rsa"]

        template = cli.template(cli.read(template_file), info)
        merged = f"{content}\n\n{template}"

        cli.write(self.config, merged.strip())

        return True

    def __dropUser(self, user=""):
        items = os.listdir(self.storage)
        if user not in items or user in ["pycache", "placeholder"]:
            cli.error("User not found")
            return False

        if not os.path.exists(self.config):
            cli.error("Config not found")
            return False

        # Remove from config
        content = cli.read(self.config)
        pattern = rf"# {self.cliname}-start: {user}(.*?)# {self.cliname}-end: {user}"
        matches = re.findall(pattern, content, re.DOTALL)

        if not matches:
            return True
        for match in matches:
            content = content.replace(
                f"\n\n# {self.cliname}-start: {user}{match}# {self.cliname}-end: {user}",
                "",
            )
            content = content.replace(
                f"\n# {self.cliname}-start: {user}{match}# {self.cliname}-end: {user}",
                "",
            )
            content = content.replace(
                f"# {self.cliname}-start: {user}{match}# {self.cliname}-end: {user}",
                "",
            )

        if not cli.write(self.config, content.strip()):
            cli.error("Failed: config")
            return False

        # Remove from storage
        key_file = os.path.join(self.storage, user)
        os.remove(key_file)

        return True

    def __sshKeys(self, key_file=""):
        passphrase = input("Passphrase: ")
        print()

        try:
            command = f'ssh-keygen -o -t rsa -b 4096 -f "{key_file}" -N "{passphrase}" -C "{self.cliname}"'
            subprocess.run(command, shell=True, check=True)

            pub = f"{key_file}.pub"
            if not os.path.exists(key_file) or not os.path.exists(pub):
                return False

            rsa = open(pub, "r").read()
            os.remove(pub)

            return {
                "key": open(key_file, "r").read(),
                "rsa": rsa,
            }
        except subprocess.CalledProcessError as e:
            print(f"ssh-keygen error: {e}")

        return False

    def __cloneProject(self, current="", link=""):
        user = ""
        while not user:
            user = input("User: ")
        mail = ""
        while not mail:
            mail = input("Mail: ")
        print()

        link = link.replace(":", f"-{user}:")
        name = link.split("/").pop().split(".")[0].strip()
        self.__execute(f"git clone {link}", "git clone")

        source_folder = os.path.join(current, name)
        if not os.path.exists(source_folder):
            cli.error("Project not found")
            return False

        for item_name in os.listdir(source_folder):
            source_item = os.path.join(source_folder, item_name)
            destination_item = os.path.join(current, item_name)
            shutil.move(source_item, destination_item)
        os.rmdir(source_folder)

        current = current.replace("\\", "/")
        self.__execute(
            f'git config --global --add safe.directory "{current}"', "git config safe"
        )
        self.__execute(f'git config user.name "{user}"', "git config user")
        self.__execute(f'git config user.email "{mail}"', "git config mail")

        return True

    def __execute(self, line="", message="", background=False):
        if not line:
            cli.error("Invalid CMD line")
            return False

        try:
            if background:
                subprocess.Popen(line, shell=True)
            else:
                subprocess.run(line, check=True)
            cli.done(message)
            return True
        except subprocess.CalledProcessError:
            cli.error(f"CMD Failed: {message}")
            return False

        return False

    def __interface(self):
        return [
            "service",
            "user",
        ]
