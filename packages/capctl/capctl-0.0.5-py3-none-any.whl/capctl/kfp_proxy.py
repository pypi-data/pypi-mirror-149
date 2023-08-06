"kubectl get envoyfilter pipeline-add-header -n cap-dev -o yaml > pipeline-add-header.yaml"
"kubectl get authorizationpolicy bind-kfp-proxyb-cap-dev -n cap-dev -o yaml > bind-kfp-proxyb.yaml"
"kubectl get authorizationpolicy bind-ml-pipeline-nb-cap-dev -n kubeflow -o yaml > bind-ml-pipeline-nb.yaml"
"kubectl get deployment kfp-deploy -n cap-dev -o yaml > kfp-deploy.yaml"
"kubectl get svc kfp-proxy -n cap-dev -o yaml > kfp-proxy-svc.yaml"

from abc import abstractmethod
import os
import yaml
import subprocess
from .log import logger
from .cap_util import get_name_by_email, write_yaml

PIPELINE_ADD_HEADER = "pipeline-add-header.yaml"
BIND_KFP_PROXYB = "bind-kfp-proxyb.yaml"
BIND_ML_PIPELINE_NB = "bind-ml-pipeline-nb.yaml"
KFP_DEPLOY = "kfp-deploy.yaml"
KFP_PROXY_SVC = "kfp-proxy-svc.yaml"


class KfpProxyCommand(object):
    def add(self, email, username):
        logger.debug("add kfp-proxy for new user")
        success = self.update_pipeline_add_header(email, username)
        if success:
            self.apply(PIPELINE_ADD_HEADER)
        else:
            logger.error("Failed to add pipeline_add_header envoyfilter")

        success = self.update_bind_kfp_proxyb(email, username)
        if success:
            self.apply(BIND_KFP_PROXYB)
        else:
            logger.error("Failed to add bind_kfp_proxyb")

        success = self.update_bind_ml_pipeline_nb(email, username)
        if success:
            self.apply(BIND_ML_PIPELINE_NB)
        else:
            logger.error("Failed to add bind_ml_pipeline_nb")

        success = self.update_kfp_deploy(email, username)
        if success:
            self.apply(KFP_DEPLOY)
        else:
            logger.error("Failed to add kfp_deploy")

        success = self.update_kfp_proxy(email, username)
        if success:
            self.apply(KFP_PROXY_SVC)
        else:
            logger.error("Failed to add kfp_proxy_svc")

        self.delete_all_yaml()

    def delete(self, username):
        cmd = f"kubectl delete authorizationpolicy bind-ml-pipeline-nb-{username} -n kubeflow"
        self.run_command(cmd)

    ## pipeline_add_header
    def update_pipeline_add_header(self, email, username):
        self.save_pipeline_add_header()
        contents = self.get_pipeline_add_header(email, username)
        if contents:
            write_yaml(contents, PIPELINE_ADD_HEADER)
            return True
        return False

    def save_pipeline_add_header(self):
        cmd = (
            "kubectl get envoyfilter pipeline-add-header -n cap-dev -o yaml > %s"
            % PIPELINE_ADD_HEADER
        )
        self.run_command(cmd)

    def get_pipeline_add_header(self, email, username):
        with open(PIPELINE_ADD_HEADER) as f:
            body = yaml.safe_load(f)
            body["metadata"]["namespace"] = username
            body["spec"]["configPatches"][0]["patch"]["value"][
                "request_headers_to_add"
            ][0]["header"]["value"] = email
            return body

    ## bind_kfp_proxyb
    def update_bind_kfp_proxyb(self, email, username):
        self.save_bind_kfp_proxyb()
        contents = self.get_bind_kfp_proxyb(email, username)
        if contents:
            write_yaml(contents, BIND_KFP_PROXYB)
            return True
        return False

    def save_bind_kfp_proxyb(self):
        cmd = (
            "kubectl get authorizationpolicy bind-kfp-proxyb -n cap-dev -o yaml > %s"
            % BIND_KFP_PROXYB
        )
        self.run_command(cmd)

    def get_bind_kfp_proxyb(self, email, username):
        with open(BIND_KFP_PROXYB) as f:
            body = yaml.safe_load(f)
            body["metadata"]["namespace"] = username
            return body

    ## bind_ml_pipeline_nb
    def update_bind_ml_pipeline_nb(self, email, username):
        self.save_bind_ml_pipeline_nb()
        contents = self.get_bind_ml_pipeline_nb(email, username)
        if contents:
            write_yaml(contents, BIND_ML_PIPELINE_NB)
            return True
        return False

    def save_bind_ml_pipeline_nb(self):
        cmd = (
            "kubectl get authorizationpolicy bind-ml-pipeline-nb-cap-dev -n kubeflow -o yaml > %s"
            % BIND_ML_PIPELINE_NB
        )
        self.run_command(cmd)

    def get_bind_ml_pipeline_nb(self, email, username):
        with open(BIND_ML_PIPELINE_NB) as f:
            body = yaml.safe_load(f)
            body["metadata"]["name"] = f"bind-ml-pipeline-nb-{username}"
            body["spec"]["rules"][0]["from"][0]["source"]["principals"][
                0
            ] = f"cluster.local/ns/{username}/sa/default-editor"
            return body

    ## kfp_deploy
    def update_kfp_deploy(self, email, username):
        self.save_kfp_deploy()
        contents = self.get_kfp_deploy(email, username)
        if contents:
            write_yaml(contents, KFP_DEPLOY)
            return True
        return False

    def save_kfp_deploy(self):
        cmd = "kubectl get deployment kfp-deploy -n cap-dev -o yaml > %s" % KFP_DEPLOY
        self.run_command(cmd)

    def get_kfp_deploy(self, email, username):
        with open(KFP_DEPLOY) as f:
            body = yaml.safe_load(f)
            body["metadata"]["namespace"] = username
            return body

    ## kfp_proxy
    def update_kfp_proxy(self, email, username):
        self.save_kfp_proxy()
        contents = self.get_kfp_proxy(email, username)
        if contents:
            write_yaml(contents, KFP_PROXY_SVC)
            return True
        return False

    def save_kfp_proxy(self):
        cmd = "kubectl get svc kfp-proxy -n cap-dev -o yaml > %s" % KFP_PROXY_SVC
        self.run_command(cmd)

    def get_kfp_proxy(self, email, username):
        with open(KFP_PROXY_SVC) as f:
            body = yaml.safe_load(f)
            body["metadata"]["namespace"] = username
            body["spec"].pop("clusterIPs", None)
            body["spec"].pop("clusterIP", None)
            return body

    ##
    def run_command(self, cmd):
        logger.debug(cmd)
        ret = subprocess.call(cmd, shell=True)

    def apply(self, yaml_file):
        cmd = "kubectl apply -f %s" % yaml_file
        ret = subprocess.call(cmd, shell=True)
        logger.debug(f"kubectl apply result: {ret}")

    def delete_all_yaml(self):
        os.remove(PIPELINE_ADD_HEADER)
        os.remove(BIND_KFP_PROXYB)
        os.remove(BIND_ML_PIPELINE_NB)
        os.remove(KFP_DEPLOY)
        os.remove(KFP_PROXY_SVC)
