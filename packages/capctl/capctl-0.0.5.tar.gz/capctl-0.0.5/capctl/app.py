import shutil
import os


def _get_curl_sh_str(name):
    curl_t = """
if [ $# -eq 0 ]; then HOST="localhost"; PORT="8080"; else HOST="$1"; PORT="$2";fi
STATE=$(curl -s -k https://${HOST}:${PORT} | grep -oP '(?<=state=)[^ ]*"' | cut -d \\" -f1)
REQ=$(curl -s -k "https://${HOST}:${PORT}/dex/auth?client_id=kubeflow-oidc-authservice&redirect_uri=%2Flogin%2Foidc&response_type=code&scope=profile+email+groups+openid&amp;state=$STATE" | grep -oP '(?<=req=)\w+')
curl -s -k "https://${HOST}:${PORT}/dex/auth/local?req=$REQ" -H 'Content-Type: application/x-www-form-urlencoded' --data 'login=cap-dev%40dudaji.com&password=12341234'
CODE=$(curl -s -k "https://${HOST}:${PORT}/dex/approval?req=$REQ" | grep -oP '(?<=code=)\w+')
curl -s -k --cookie-jar - "https://${HOST}:${PORT}/login/oidc?code=$CODE&amp;state=$STATE" > .dex_session
DEX_SESSION=$(cat .dex_session | grep 'authservice_session' | awk '{print $NF}')"""
    curl_t2 = """

curl -k "https://${HOST}:${PORT}/api/%s/user" -H "Cookie: authservice_session=${DEX_SESSION}"
    """ % name
    return curl_t + curl_t2


def _get_docker_build_str(docker_image_name):
    t = f"""
docker build -t {docker_image_name} .
docker push {docker_image_name}
"""
    return t


def _get_bash_str(name, namespace):
    t = f"""kubectl run curl-{name} --namespace={namespace} --image=radial/busyboxplus:curl -i --tty --rm
# container> curl {name}.{namespace}.svc.cluster.local
"""
    return t


def _create_scripts(name, namespace, project_home, docker_image_name):
    scripts_home = os.path.join(project_home, 'scripts')

    def __create(filename, content):
        f = os.path.join(scripts_home, filename)
        with open(f, 'w') as fd:
            fd.write(content)
        os.chmod(f, 0o755)

    __create(
        'curl-to-get-user.sh',
        _get_curl_sh_str(name))
    __create(
        'docker-build-and-push.sh',
        _get_docker_build_str(docker_image_name))
    __create(
        'get-bash-inside-kubernetes.sh',
        _get_bash_str(name, namespace))
    __create('kubectl-apply.sh', """
kubectl apply -f yaml/deployment.yaml
kubectl apply -f yaml/service.yaml
kubectl apply -f yaml/virtual-service.yaml""")
    __create(
        'debug.sh',
        f"telepresence --swap-deployment {name} --expose 5000 --namespace {namespace}")


def _get_vs_str(name, namespace):
    return f"""
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  labels:
    app: {name}
  name: {name}
  namespace: {namespace}
spec:
  gateways:
  - kubeflow/kubeflow-gateway
  hosts:
  - '*'
  http:
  - match:
    - uri:
        prefix: /api/{name}
    rewrite:
      uri: /
    route:
    - destination:
        host: {name}.cap.svc.cluster.local
        port:
          number: 80
    """


def _get_dp_str(name, namespace, docker_image_name):
    return f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
  namespace: {namespace}
  labels:
    app: {name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
        - image: {docker_image_name}
          imagePullPolicy: Always
          name: {name}
          ports:
            - containerPort: 5000
              protocol: TCP
    """


def _get_svc_str(name, namespace):
    return f"""
apiVersion: v1
kind: Service
metadata:
  name: {name}
  namespace: {namespace}
  labels:
    app: {name}
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 5000
  selector:
    app: {name}
  type: ClusterIP
"""


def _create_yaml(name, namespace, project_home, docker_image_name):
    yaml_home = os.path.join(project_home, 'yaml')

    def __create(filename, content):
        f = os.path.join(yaml_home, filename)
        with open(f, 'w') as fd:
            fd.write(content)
    __create('virtual-service.yaml', _get_vs_str(name, namespace))
    __create('deployment.yaml', _get_dp_str(
        name, namespace, docker_image_name))
    __create('service.yaml', _get_svc_str(name, namespace))


def _create_cap_yaml(name, namespace, project_home, docker_image_name):
    f = os.path.join(project_home, 'cap.yaml')
    with open(f, 'w') as fd:
        fd.write(f"""
veresion: "0.0.1"
user: root
accessIP: localhost
namespace: {namespace}
registry: cap.dudaji.com:31480
project: cap
image: {docker_image_name}
deploy:
  dockerfile: Dockerfile
  kubectl:
    manifests:
    - yaml/deployment.yaml
    - yaml/service.yaml
    - yaml/virtual-service.yaml
develop:
  name: {name}
  port: 5000""")


class AppCommand(object):
    def __init__(self):
        pass

    def create(
            self,
            name,
            lang='python'):
        namespace = 'cap'
        cwd = os.getcwd()
        project_home = os.path.join(cwd, name)
        os.makedirs(project_home)
        os.makedirs(os.path.join(project_home, 'yaml'))
        os.makedirs(os.path.join(project_home, 'scripts'))

        template_home = os.path.join(
            os.path.dirname(__file__),
            'template',
            lang
        )
        copy_files = [
            'main.py',
            'Dockerfile',
            'requirements.txt'
        ]
        for copy_file in copy_files:
            shutil.copy2(
                os.path.join(template_home, copy_file),
                project_home
            )

        docker_image_name = f"cap.dudaji.com:31480/cap/{name}:0.0.1"

        _create_scripts(name, namespace, project_home, docker_image_name)
        _create_yaml(name, namespace, project_home, docker_image_name)
        _create_cap_yaml(name, namespace, project_home, docker_image_name)
