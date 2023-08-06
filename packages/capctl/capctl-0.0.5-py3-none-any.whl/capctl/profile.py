import subprocess
from .log import logger
from .cap_util import write, apply_kube


profile_template = """
apiVersion: kubeflow.org/v1beta1
kind: Profile
metadata:
  name: {username}
spec:
  owner:
    kind: User
    name: {email}
"""


class ProfileCommand(object):
    def add(self, email, username):
        profile = profile_template.format(username=username, email=email)
        filename = f"{username}-profile.yaml"

        write(filename, profile)
        apply_kube(filename)

    def delete(self, username):
        cmd = f"kubectl delete profiles.kubeflow.org {username}"
        logger.debug(cmd)
        ret = subprocess.call(cmd, shell=True)
        logger.debug(f"kubectl result: {ret}")
