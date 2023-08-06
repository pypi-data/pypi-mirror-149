import kubernetes as k
from .log import logger
import subprocess
from .cap_util import write, apply_kube, get_name_by_email


rb_template = """
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  annotations:
    role: edit
    user: {email}
  name: user-{kebab_email}-clusterrole-edit
  namespace: {namespace} 
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubeflow-edit
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: {email}
"""

ap_template = """
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  annotations:
    role: edit
    user: {email}
  name: user-{kebab_email}-clusterrole-edit
  namespace: {namespace}
spec:
  rules:
  - when:
    - key: request.headers[kubeflow-userid]
      values:
      - {email}
"""

srb_template = """
apiVersion: rbac.istio.io/v1alpha1
kind: ServiceRoleBinding
metadata:
  annotations:
    role: edit
    user: {email}
  generation: 1
  name: user-{kebab_email}-clusterrole-edit
  namespace: {namespace}
spec:
  roleRef:
    kind: ServiceRole
    name: ns-access-istio
  subjects:
  - properties:
      request.headers[kubeflow-userid]: {email}
"""


class ProjectCommand(object):
    def join(self, email, namespace):
        logger.debug("join")
        name = get_name_by_email(email)
        if not name:
            logger.error(f"Fail! email:'{email}' not exist.")
            return

        kebab_email = email.replace("@", "-").replace(".", "-")
        rb = rb_template.format(
            email=email, namespace=namespace, kebab_email=kebab_email
        )
        rb_file = f"{kebab_email}-rb.yaml"
        write(rb_file, rb)

        srb = ap_template.format(
            email=email, namespace=namespace, kebab_email=kebab_email
        )
        srb_file = f"{kebab_email}-ap.yaml"
        write(srb_file, srb)

        apply_kube(rb_file)
        apply_kube(srb_file)

    def leave(self, email, namespace):
        logger.debug("leave")
        name = get_name_by_email(email)
        if not name:
            logger.error(f"Fail! email:'{email}' not exist.")
            return

        kebab_email = email.replace("@", "-").replace(".", "-")
        name = f"user-{kebab_email}-clusterrole-edit"
        cmd = f"kubectl delete rolebinding {name} -n {namespace}"
        logger.debug(cmd)
        ret = subprocess.call(cmd, shell=True)
        logger.debug(f"kubectl result: {ret}")
        cmd = f"kubectl delete authorizationpolicy {name} -n {namespace}"
        logger.debug(cmd)
        ret = subprocess.call(cmd, shell=True)
        logger.debug(f"kubectl result: {ret}")
