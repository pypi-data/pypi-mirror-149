import subprocess
from .log import logger
from .cap_util import (
    CapYamlUtil,
    login_harbor,
    install,
    download_kubeconfig,
    merge_kubeconfig,
    publish_image,
    apply_helm,
    apply_kube_ns,
    run_telepresence,
)


util = CapYamlUtil()


class DevCommand(object):
    def __init__(self, kubeconfig=False):
        self.kubeconfig = kubeconfig
        self.cap_yaml = util.read_cap_yaml() 

    def init(self):
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
        login_harbor(self.cap_yaml["registry"], **kwargs)
        install("helm", **kwargs)
        install("telepresence", **kwargs)
        if self.kubeconfig == True:
            download_kubeconfig(
                self.cap_yaml["user"], self.cap_yaml["accessIP"], **kwargs
            )
            merge_kubeconfig(self.cap_yaml["accessIP"], **kwargs)
        self.deploy()

    def deploy(self):
        kwargs = {"stderr": subprocess.PIPE}
        image_name = "/".join(
            [
                self.cap_yaml["registry"],
                self.cap_yaml["project"],
                self.cap_yaml["image"],
            ]
        )
        dockerfile = self.cap_yaml["deploy"]["dockerfile"]
        namespace = self.cap_yaml["namespace"]

        publish_image(image_name, dockerfile, **kwargs)
        deploy_dict = self.cap_yaml["deploy"]
        if "kubectl" in deploy_dict:
            manifests = deploy_dict["kubectl"]["manifests"]
            for manifest in manifests:
                apply_kube_ns(manifest, namespace, **kwargs)
        elif "helm" in deploy_dict:
            apply_helm(
                deploy_dict["helm"]["name"],
                deploy_dict["helm"]["chartPath"],
                namespace,
                **kwargs,
            )
        else:
            logger.error("Please check deployment type (only kubectl and helm)")

    def publish(self):
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
        image_name = "/".join(
            [
                self.cap_yaml["registry"],
                self.cap_yaml["project"],
                self.cap_yaml["image"],
            ]
        )
        image_tag = self.cap_yaml["version"]
        dockerfile = self.cap_yaml["deploy"]["dockerfile"]
        image_name = f"{image_name}:{image_tag}"
        publish_image(image_name, dockerfile, **kwargs)

    def debug(self):
        deployment_name = self.cap_yaml["develop"]["name"]
        container_port = self.cap_yaml["develop"]["port"]
        namespace = self.cap_yaml["namespace"]
        run_telepresence(deployment_name, container_port, namespace)
