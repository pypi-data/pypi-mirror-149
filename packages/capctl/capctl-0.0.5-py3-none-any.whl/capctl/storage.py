import json
from urllib.parse import urlparse, ParseResult
import pprint
import time
import urllib3
import requests
from .log import logger
from .cap_util import (
    CapYamlUtil,
    run_proc
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_session(user_id, password, uri):
    session = requests.Session()
    response = session.get(uri, verify=False)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"login": user_id, "password": password}
    session.post(response.url, headers=headers, data=data, verify=False)
    session_cookie = session.cookies.get_dict()["authservice_session"]
    return session_cookie


def _get_headers(session_cookie):
    headers = {
        "Cookie": f"authservice_session={session_cookie}",
    }
    return headers


def _get_endpoint(uri, namespace):
    endpoint = f"{uri}/api/minio-operator/namespaces/{namespace}/minios/"
    return endpoint


def get_storage_list(uri, session_cookie, namespace):
    endpoint = _get_endpoint(uri, namespace)
    headers = {
        "Cookie": f"authservice_session={session_cookie}",
    }
    # logger.info(headers)
    session = requests.Session()
    response = session.get(endpoint, headers=headers, verify=False)
    assert response.status_code == 200
    json_data = json.loads(response.text)
    # logger.info(json_data)
    # logger.info(response.text)
    # print(response.request.url)
    # print(response.request.body)
    # print(response.request.headers)
    return json_data


def _generate_storage_name(storage_name, provider_name, append_provider):
    if append_provider is False:
        return storage_name
    return storage_name + "-" + provider_name


class StorageCommand(object):
    def _append_port(self, uri, port):
        old = urlparse(uri)
        new = ParseResult(
            scheme=old.scheme,
            netloc="{}:{}".format(old.hostname, port),
            path=old.path,
            params=old.params,
            query=old.query,
            fragment=old.fragment)
        return new.geturl()

    def _create_storage_sessions(self, storage_name, config_path, append_provider):
        sessions = []

        cy = CapYamlUtil(config_path)
        docs = cy.read_cap_yaml()
        assert "storage" in docs
        assert "metadata" in docs
        m = docs["metadata"]
        # s = docs["storage"]
        user_id = m["userId"]
        password = m["password"]
        namespace = m["namespace"]
        endpoints = m["endpoints"]

        for endpoint in endpoints:
            provider_name = endpoint["providerName"]
            uri = endpoint["uri"]
            session_cookie = create_session(user_id, password, uri)
            _ = get_storage_list(uri, session_cookie, namespace)
            cur_storage_name = _generate_storage_name(
                storage_name, provider_name, append_provider)
            sessions.append({
                "provider_name": provider_name,
                "session_cookie": session_cookie,
                "storage_name": cur_storage_name,
                "uri": uri,
                "namespace": namespace,
            })
        return sessions

    def _delete_storage_one(self, uri, namespace, session_cookie, storage_name):
        endpoint = _get_endpoint(uri, namespace)
        endpoint += storage_name
        headers = _get_headers(session_cookie)
        response = requests.delete(
            url=endpoint,
            headers=headers,
            verify=False)
        success = response.status_code < 300
        return success

    def _create_storage_one(self, uri, namespace, session_cookie, storage_name):
        endpoint = _get_endpoint(uri, namespace)
        headers = _get_headers(session_cookie)
        response = requests.post(
            url=endpoint,
            headers=headers,
            json={"minioname": storage_name, "username": storage_name},
            verify=False)

        success = False
        if response.status_code < 300:
            success = True
        else:
            logger.warning(response.text)
        return success

    def _create_storage(self, sessions: list):
        success = True
        success_sessions = []
        for session in sessions:
            session_cookie = session["session_cookie"]
            storage_name = session["storage_name"]
            uri = session["uri"]
            namespace = session["namespace"]
            # print(provider, session_cookie, storage_name)
            if self._create_storage_one(uri, namespace, session_cookie, storage_name):
                success_sessions.append(session)
            else:
                success = False
                break
        return success, success_sessions

    def _save_metadata(self, storage_name, storage_metadata: list):
        name = storage_name
        for item in storage_metadata:
            cluster = item["provider_name"]
            endpoint = item["endpoint"]
            access_key = item["access_key"]
            secret_key = item["secret_key"]
            self.add(name, cluster, endpoint, access_key, secret_key)

    def _delete_storage(self, sessions: list):
        for session in sessions:
            session_cookie = session["session_cookie"]
            storage_name = session["storage_name"]
            uri = session["uri"]
            namespace = session["namespace"]
            self._delete_storage_one(
                uri, namespace, session_cookie, storage_name)

    def __get_storage_info(self, provider_name, uri, namespace, session_cookie, storage_name):
        l = get_storage_list(uri, session_cookie, namespace)
        items = l["services"]["items"]
        for item in items:
            d = item["metadata"]["annotations"]
            name = d["meta.helm.sh/release-name"]
            secret_key = d["secretKey"]
            node_port = item["spec"]["ports"][0]["nodePort"]
            endpoint = self._append_port(uri, node_port)
            if name == storage_name:
                info = {
                    "provider_name": provider_name,
                    "endpoint": endpoint,
                    "access_key": name,
                    "secret_key": secret_key
                }
                logger.debug(info)
                return info
        time.sleep(3)
        logger.warning("Try one more getting storage info")
        return self.__get_storage_info(provider_name, uri, namespace, session_cookie, storage_name)

    def _collect_metadata(self, sessions: list):
        storage_infos = []
        for session in sessions:
            provider_name = session["provider_name"]
            session_cookie = session["session_cookie"]
            storage_name = session["storage_name"]
            uri = session["uri"]
            namespace = session["namespace"]
            storage_info = self.__get_storage_info(
                provider_name, uri, namespace, session_cookie, storage_name)
            storage_infos.append(storage_info)
        return storage_infos

    def _remove_mc_alias(self, name, sessions: list):
        for session in sessions:
            provider_name = session["provider_name"]
            cluster = provider_name
            command = f"mc alias rm {name}-{cluster}"
            success, out, err = run_proc(command, mute_log=True)
            assert success

    def delete(self, name, config_path="cap.yaml", append_provider=True):
        logger.info("Start delete storage")
        storage_name = name
        sessions = self._create_storage_sessions(
            storage_name, config_path, append_provider)
        logger.info("Sessions are created.")
        self._delete_storage(sessions)
        logger.info("After delete storage in clusters")
        self._remove_mc_alias(name, sessions)
        cy = CapYamlUtil(config_path)
        docs = cy.read_cap_yaml()
        s = docs["storage"]
        new_storage_list = [
            item for item in s
            if item["name"] != name]
        docs["storage"] = new_storage_list
        cy.update_cap_yaml(docs)
        logger.info("After update cap.yaml")

    def create(self, name, config_path="cap.yaml", append_provider=True):
        logger.info("Start create storage")
        storage_name = name
        sessions = self._create_storage_sessions(
            storage_name, config_path, append_provider)
        logger.info("Sessions are created.")

        # create storage
        success, success_sessions = self._create_storage(sessions)
        if success:
            logger.info("Storage created.")
            storage_metadata = self._collect_metadata(success_sessions)
            logger.info("After collect metadata.")
            time.sleep(10)
            self._save_metadata(storage_name, storage_metadata)
            logger.info("After saving metadata.")
            logger.info(
                "Finish create storage. plz check cap.yaml and storage in cap-dashboard.")
        else:
            self._delete_storage(success_sessions)
            logger.info("Fail to create storage(rollback)")

    def ls(self,
           config_path="cap.yaml"):
        cy = CapYamlUtil(config_path)
        docs = cy.read_cap_yaml()
        assert "storage" in docs
        s = docs["storage"]
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(s)

    def sync(self,
             name,
             config_path="cap.yaml"):
        cy = CapYamlUtil(config_path)
        docs = cy.read_cap_yaml()
        assert "storage" in docs
        s = docs["storage"]
        target_storage_list = [
            item for item in s
            if item["name"] == name]
        assert len(target_storage_list) == 1
        target_storage = target_storage_list[0]
        cap = [
            item for item in target_storage["kubernetes"]
            if item["cluster"] == "cap"][0]

        others = [
            item for item in target_storage["kubernetes"]
            if item["cluster"] != "cap"]

        home = "%s-%s" % (name, cap["cluster"])

        for other in others:
            away = "%s-%s" % (name, other["cluster"])
            command = f'mc mirror --overwrite {away} {home}'
            success, out, err = run_proc(command)
            assert success

        for other in others:
            away = "%s-%s" % (name, other["cluster"])
            command = f'mc mirror --overwrite {home} {away}'
            success, out, err = run_proc(command)
            assert success
        logger.info("Sync success")

    def add(self,
            name,
            cluster,
            endpoint,
            access_key,
            secret_key,
            config_path="cap.yaml"):
        cy = CapYamlUtil(config_path)
        docs = cy.read_cap_yaml()
        s = docs["storage"]
        target_storage_list = [
            item for item in s
            if item["name"] == name]

        if len(target_storage_list) == 0:
            target_storage = {
                "name": name,
                "kubernetes": []
            }
            s.append(target_storage)
        else:
            target_storage = target_storage_list[0]

        k = target_storage["kubernetes"]

        target_cluster_list = [
            item for item in k
            if item["cluster"] == cluster]

        if len(target_cluster_list) == 0:
            target_cluster = {
                "cluster": cluster,
            }
            target_storage["kubernetes"].append(target_cluster)
        else:
            target_cluster = target_cluster_list[0]

        target_cluster["endpoint"] = endpoint
        target_cluster["accessKey"] = access_key
        target_cluster["secretKey"] = secret_key
        cy.update_cap_yaml(docs)

        command = f"mc alias set {name}-{cluster} {endpoint} {access_key} {secret_key}"
        success, out, err = run_proc(command, mute_log=True)
        if success is False:
            logger.warning(f"Try again '{command}'")
            time.sleep(10)
            return self.add(name, cluster, endpoint, access_key, secret_key, config_path)
        assert success
