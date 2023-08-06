import datetime
import os
import subprocess
import platform
from pathlib import Path
import yaml
from .log import logger
from .session import Session
from .script import (
    mac_helm_install,
    mac_telepresence_install,
    ubuntu_helm_install,
    ubuntu_telepresence_install,
)


def run_proc(command, mute_log=False):
    logger.debug('run_proc: %s' % command)
    proc = subprocess.Popen(
        [command],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True)
    (out, err) = proc.communicate()
    success = int(proc.returncode) == 0
    if success or mute_log:
        pass
    else:
        logger.warning('command: %s' % command)
        logger.warning('out: %s' % out)
        logger.warning('err: %s' % err)
    return success, out, err


class CapYamlUtil:
    def __init__(self, config_path="cap.yaml"):
        self.config_path = config_path
        self.docs = {}

    def read_cap_yaml(self):
        config_path = self.config_path
        Path(config_path).touch(exist_ok=True)
        with open(config_path) as f:
            docs = yaml.safe_load(f)
            if docs is None:
                docs = {}
            if "storage" not in docs:
                docs["storage"] = []
        self.docs = docs
        return docs

    def update_cap_yaml(self, docs):
        self.docs = docs
        self.save_cap_yaml()

    def save_cap_yaml(self):
        config_path = self.config_path
        with open(config_path, "w") as f:
            yaml.dump(self.docs, f)


def login_harbor(registry, **kwargs):
    cmd = ["docker", "login", registry]
    _, err, ret = run_command(cmd, **kwargs)
    if ret != 0:
        logger.error(f"Fail to login CAP harbor")
        logger.error(err)


def install(target, **kwargs):
    os_type = check_os()
    if os_type == "Linux":
        # linux
        if target == "helm":
            install_target(target, ubuntu_helm_install, **kwargs)
        elif target == "telepresence":
            install_target(target, ubuntu_telepresence_install, **kwargs)
        else:
            logger.error(f"{target} is not supported")
            return
    elif os_type == "Darwin":
        # macos
        if target == "helm":
            install_target(target, mac_helm_install, **kwargs)
        elif target == "telepresence":
            install_target(target, mac_telepresence_install, **kwargs)
        else:
            logger.error(f"{target} is not supported")
            return
    else:
        logger.error(f"Unknown OS type : {os_type}")
        return


def install_target(target, cmd, **kwargs):
    if check_installed(target, **kwargs):
        print(f"{target} is already installed")
        logger.debug(f"{target} is already installed")
        return
    print(f"Installing {target}...")
    kwargs["shell"] = True
    _, err, ret = run_command(cmd, **kwargs)
    if ret != 0:
        logger.error("Fail to install helm")
        logger.error(err)
        return


def check_os():
    return platform.system()


def check_installed(target, **kwargs):
    cmd = ["which", target]
    _, _, ret = run_command(cmd, **kwargs)
    if ret == 1:
        return False
    else:
        return True


def write(filename, text):
    with open(filename, "w") as f:
        f.write(text)


def download_kubeconfig(user, access_ip, **kwargs):
    cmds = [
        ["scp", f"{user}@{access_ip}:~/.kube/config", f"./config.{access_ip}"],
        [
            "sed",
            "-r",
            "-i.bak",
            f"s/((1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){{3}}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])/{access_ip}/",
            f"config.{access_ip}",
        ],
    ]
    print("Downloading kubeconfig file...")
    for cmd in cmds:
        _, err, ret = run_command(cmd, **kwargs)
        if ret != 0:
            logger.error(err)
            return


def merge_kubeconfig(access_ip, **kwargs):
    home_dir = str(Path.home())
    kube_env = os.environ.copy()
    kube_env["KUBECONFIG"] = f"config.{access_ip}:{home_dir}/.kube/config"
    kwargs["env"] = kube_env
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    cmds = [
        ["sed", "-i", "-e", "s/kubernetes/develop/g", f"config.{access_ip}"],
        [
            "cp",
            f"{home_dir}/.kube/config",
            f"{home_dir}/.kube/config.bak.{now_date}",
        ],
        ["kubectl", "config", "view", "--merge", "--flatten"],
        ["mv", f"{home_dir}/.kube/merged", f"{home_dir}/.kube/config"],
        ["kubectl", "config", "use-context", "develop-admin@cluster.local"],
    ]
    print("Merging kubeconfig...")
    for cmd in cmds:
        output, err, ret = run_command(cmd, **kwargs)
        if ret != 0:
            logger.error(err)
            return
        if cmd[2] == "view":
            write(f"{home_dir}/.kube/merged", output)


def publish_image(image_name, dockerfile, **kwargs):
    cmds = [
        ["docker", "build", "-t", f"{image_name}", "-f", f"{dockerfile}", "."],
        ["docker", "push", f"{image_name}"],
    ]
    print("Publishing image...")
    for cmd in cmds:
        _, err, ret = run_command(cmd, **kwargs)
        if ret != 0:
            logger.error(err)
            return


def apply_kube(filename, expect=[0]):
    cmd = f"kubectl apply -f {filename}"
    logger.debug(cmd)
    ret = subprocess.call(cmd, shell=True)
    logger.debug(f"kubectl apply result: {ret}")
    if ret not in expect:
        logger.error(f"Unexpected kubectl apply cmd:'{cmd}', ret:'{ret}'")


def apply_kube_ns(filename, namespace, **kwargs):
    cmd = ["kubectl", "apply", "-f", f"{filename}", "-n", f"{namespace}"]
    print("Applying deployment...")
    # ret = subprocess.call(cmd, shell=True)
    _, err, ret = run_command(cmd, **kwargs)
    logger.debug(f"kubectl apply result: {ret}")
    if ret != 0:
        logger.error(f"Unexpected kubectl apply cmd:'{cmd}', ret:'{ret}'")
        logger.error(err)


def apply_helm(release_name, char_path, namespace, **kwargs):
    cmd = [
        "helm",
        "install",
        f"{release_name}",
        f"{char_path}",
        "-n",
        f"{namespace}",
    ]
    print("Applying helm chart...")
    _, err, ret = run_command(cmd, **kwargs)
    if ret != 0:
        logger.error(err)
        return


def get_branch_name(**kwargs):
    cmd = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    output, err, ret = run_command(cmd, **kwargs)
    if ret != 0:
        logger.error(err)
    return output.strip()


def run_telepresence(deployment_name, container_port, namespace, **kwargs):
    cmd = [
        "telepresence",
        "--swap-deployment",
        deployment_name,
        "--expose",
        f"{container_port}",
        "--namespace",
        namespace,
    ]
    _, err, ret = run_command(cmd, **kwargs)
    if ret != 0:
        logger.error(err)


def run_command(cmd, **kwargs):
    session = Session(cmd)
    output, err, ret = session.run(**kwargs)
    return (
        output,
        err,
        ret,
    )


def print_console(process):
    stdout = ""
    while True:
        nextline = str(process.stdout.readline(), "utf-8")
        if len(nextline) == 0 and process.poll() is not None:
            break
        if nextline:
            print(nextline.strip())
            stdout += nextline
    return stdout


def get_stdout(cmd, yaml_format=True):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = proc.stdout.read()
    if yaml_format:
        return yaml.safe_load(output)
    return output


def get_email_by_name(username):
    cmd = "kubectl get profiles.kubeflow.org -oyaml"
    data = get_stdout(cmd)
    items = data["items"]
    for item in items:
        email = item["spec"]["owner"]["name"]
        cur_username = item["metadata"]["name"]
        if username == cur_username:
            return email
    return None


def get_name_by_email(email):
    cmd = "kubectl get profiles.kubeflow.org -oyaml"
    data = get_stdout(cmd)
    items = data["items"]
    for item in items:
        cur_email = item["spec"]["owner"]["name"]
        username = item["metadata"]["name"]
        if email == cur_email:
            return username
    return None


def get_sumup():
    # 1. owner info
    cmd = "kubectl get profiles.kubeflow.org -oyaml"
    data = get_stdout(cmd)
    items = data["items"]
    owners = [
        (item["spec"]["owner"]["name"], item["metadata"]["name"], "owner")
        for item in items
    ]

    owners_key = set(x[0] for x in owners)

    # 2. member info
    cmd = "kubectl get rolebindings --all-namespaces -o yaml"
    data = get_stdout(cmd)
    items = data["items"]
    members = [
        (
            item["metadata"]["annotations"]["user"],
            item["metadata"]["namespace"],
            "member",
        )
        for item in items
        if ("annotations" in item["metadata"] and "user" in item["metadata"]["annotations"])
        and ("namespace" in item["metadata"])
    ]
    members_key = set(x[0] for x in members)

    # 3. dex info
    cmd = "kubectl get configmap dex -n auth -o yaml"
    data = get_stdout(cmd)
    data = yaml.safe_load(data["data"]["config.yaml"])
    items = data["staticPasswords"]
    dex_key = set(item["email"] for item in items)

    # 4. All email list
    keys = owners_key.union(members_key).union(dex_key)

    # 5. print table
    sumup = {
        x: {"email": x, "dex": False, "owners": [], "members": []} for x in keys
    }
    for email in dex_key:
        sumup[email]["dex"] = True

    for owner in owners:
        email = owner[0]
        sumup[email]["owners"].append(owner[1])

    for member in members:
        email = member[0]
        sumup[email]["members"].append(member[1])

    return sumup
