import subprocess
from terminaltables import AsciiTable
from .log import logger
from .cap_util import (
    get_sumup,
    get_name_by_email,
)
from .profile import ProfileCommand
from .dex import DexCommand


class UserCommand(object):
    def ls(self):
        sumup = get_sumup()
        rows = [
            [
                x["email"],
                x["dex"],
                ",".join(x["owners"]),
                ",".join(x["members"]),
            ]
            for k, x in sumup.items()
        ]
        header = [["email", "dex", "owners", "members"]]
        table = AsciiTable(header + rows)
        print(table.table)

    def add(self, email, password, username):
        DexCommand().add(email, password, username)
        ProfileCommand().add(email, username)

    def password(self, email, password):
        DexCommand().change_password(email, password)

    def delete(self, email, username=None):
        if not username:
            username = get_name_by_email(email)
        if not username:
            logger.error(f"Fail! email:'{email}' not exist.")
            return
        DexCommand().delete(email, username)
        ProfileCommand().delete(username)
        if email:
            kebab_email = email.replace("@", "-").replace(".", "-")
            name = f"user-{kebab_email}-clusterrole-edit"
            cmd = f"kubectl delete rolebinding --all-namespaces --field-selector metadata.name={name}"
            logger.debug(cmd)
            ret = subprocess.call(cmd, shell=True)
            logger.debug(f"kubectl result: {ret}")
            cmd = f"kubectl delete servicerolebinding --all-namespaces --field-selector metadata.name={name}"
            logger.debug(cmd)
            ret = subprocess.call(cmd, shell=True)
            cmd = f"kubectl delete servicerolebinding --all-namespaces --field-selector metadata.name={name}"
            logger.debug(f"kubectl result: {ret}")
