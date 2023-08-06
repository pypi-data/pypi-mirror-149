from terminaltables import AsciiTable
from .cap_util import run_proc, get_stdout
from .log import logger


def get_quota_list():
    cmd = "kubectl get profiles.kubeflow.org -oyaml"
    data = get_stdout(cmd)
    items = data["items"]
    quota_list = []
    for item in items:
        name = item["metadata"]["name"]
        quota = {
            "name": name,
            "cpu": "None",
            "memory": "None",
            "persistentvolumeclaims": "None",
            "requests.nvidia.com/gpu": "None",
            "requests.storage": "None"
        }
        if "hard" in item["spec"]["resourceQuotaSpec"]:
            n = item["spec"]["resourceQuotaSpec"]["hard"]
            # print(n)
            quota.update(n)
        quota_list.append((
            quota["name"],
            quota["cpu"],
            quota["memory"],
            quota["requests.nvidia.com/gpu"],
            quota["requests.storage"]
        ))
    return quota_list


t = """kubectl patch profile %s --type='json' -p='[{"op": "add", "path": "/spec/resourceQuotaSpec",
"value": {"hard": {"cpu": "%s", "memory": "%s", "requests.nvidia.com/gpu": "%s",
"persistentvolumeclaims": "9999", "requests.storage": "%s"}} }]'"""


class QuotaCommand(object):
    def set(self, project, cpu_count=10, gpu_count=0, mem='20Gi', storage='200Gi'):
        """
        Set quota of project

        ex) capctl quota set --project=shhong --cpu_count=10 --gpu_count=0 --mem='20Gi' --storage='200Gi'
        """
        command = t % (project, cpu_count, mem, gpu_count, storage)
        logger.info(command)
        success, out, err = run_proc(command, mute_log=False)
        assert success

    def status(self, project):
        cmd = """kubectl get resourcequotas -n %s -o yaml""" % project
        data = get_stdout(cmd)
        hard = data["items"][0]["status"]["hard"]
        used = data["items"][0]["status"]["used"]
        targets = ["cpu", "memory",
                   "requests.nvidia.com/gpu", "requests.storage"]
        rows = [
            (k, used[k], hard[k])
            for k in targets
        ]
        header = [["resource", "used", "limit"]]
        table = AsciiTable(header + rows)
        print(table.table)

    def ls(self):
        rows = get_quota_list()
        header = [["project", "cpu", "memory", "gpu", "storage"]]
        table = AsciiTable(header + rows)
        print(table.table)
