import json
import os
import warnings
from http import HTTPStatus
from queue import Queue

import numpy as np
import requests

from .__consumer import Consumer
from .utils import AGGREGATED_OUTPUT_DIR

FILE_METADATA = "{'key1':'value1', 'key2':'value2'}"


class Client:
    def __init__(self,
                 credentials: dict = None,
                 host: str = "https://api.branchkey.com"):

        if credentials is None:
            credentials = dict(leaf_name="guest", leaf_password="guest", tree_id="guest", branch_id="guest",
                               queue_password="guest", host="response.branchkey.com", port=5672)
        if 'response_host' in credentials:
            credentials['host'] = credentials['response_host']
        self.__leaf_name = credentials["leaf_name"]
        self.__leaf_password = credentials["leaf_password"]
        self.__tree_id = credentials["tree_id"]
        self.__branch_id = credentials["branch_id"]

        self.__status = False
        self.__access_token = None
        self.__leaf_id = None

        self.__api_host = host
        # Verify SSL certs
        self.__verify = True

        self.queue = Queue()

        self.rabbit_credentials = credentials
        self.consumer = None
        return

    def disable_ssl_verification(self, enabled=False):
        warnings.warn("[BranchKey] We highly recommend enabling ssl verification. Use this at your own risk.")
        self.__verify = enabled
        return self.__verify

    def convert_pytorch_numpy(self, model, weighting=1):
        """
        Usage:
        update = convert_pytorch_numpy(model.get_params(), client_samples=5*5)
        :param model: Pytorch model parameters
        :param weighting: Weight given to this update. Usually the number of client samples used to construct the model
        :return: type(np.ndarray) of parameters
        """
        params = []
        for param in model:
            params.append(param[1].data.cpu().detach().numpy())
        numpy = (weighting, params)
        return np.asarray(numpy, dtype=object)

    def validate_weight_shape(self, file):
        """
        Validates that the weights are in the correct shape before being sent to the API
        :param file: file bytes or file path
        :return: True on success, otherwise returns an exception
        """
        array = np.load(file, allow_pickle=True)
        if array.shape[0] != 2:
            raise Exception("[validate_weight_shape] Incorrect shape != 2")
        elif type(array[0]) is not int:
            raise Exception("[validate_weight_shape] Dim 0 not integer")
        elif type(array[1]) is not list:
            raise Exception("[validate_weight_shape] Dim 1 not list")
        elif type(array[1][0]) is not np.ndarray:
            raise Exception("[validate_weight_shape] Dim 1:0 not ndarray")
        else:
            file.seek(0)
            return True

    def login(self):
        try:
            url = self.__api_host + "/v1/leaf/login"
            headers = {"accept": "application/json"}
            data = json.dumps({
                      "tree_id": self.__tree_id,
                      "branch_id": self.__branch_id
                    })

            resp = requests.put(url, data=data, headers=headers,
                                auth=(self.__leaf_name, self.__leaf_password), verify=self.__verify)

            if resp.status_code != HTTPStatus.CREATED:
                raise Exception(resp.json()["message"])

            login_data = resp.json()["data"]
            try:
                self.__leaf_id = login_data["id"]
                self.__access_token = login_data["access_token"]
                self.__status = login_data["status"]
                self.rabbit_credentials["queue_password"] = self.__access_token
                self.rabbit_credentials["leaf_id"] = self.__leaf_id
                consumer = Consumer(self.rabbit_credentials, self.queue)
                self.consumer = consumer.spawn_consumer_thread()
                return self.__status == "logged_in"
            except Exception as e:
                msg = "Failed to parse response from login"
                raise Exception(msg)

        except Exception as e:
            msg = "Login failed for {}: {}".format(self.__leaf_name, e)
            raise Exception(msg)

    def logout(self):
        if not self.__status == "logged_in" or not self.__access_token:
            msg = "Logout failed for {}: not logged in or no access_token present".format(self.__leaf_name)
            raise Exception(msg)
        try:
            url = self.__api_host + "/v1/leaf/logout"

            resp = requests.put(url, auth=(self.__leaf_name, self.__leaf_password), verify=self.__verify)

            if resp.status_code != HTTPStatus.OK:
                raise Exception(f"{resp.json()['message']}")

            self.__access_token = None
            self.__status = "logged_out"
            return True

        except Exception as e:
            msg = "Logout failed for {}: {}".format(self.__leaf_name, e)
            raise Exception(msg)

    def file_upload(self, file_path):
        if self.__status == "logged_in":
            try:
                with open(file_path, mode="rb") as f:
                    self.validate_weight_shape(f)

                    url = self.__api_host + "/v1/file/upload"
                    headers = {"accept": "application/json"}
                    data = {"data": json.dumps({"leaf_name": self.__leaf_name,
                                                "metadata": FILE_METADATA})}
                    file = {"file": f}

                    resp = requests.post(
                        url, files=file, data=data, headers=headers,
                        auth=(self.__leaf_id, self.__access_token), verify=self.__verify)
                    f.close()

                    if resp.status_code != HTTPStatus.CREATED:
                        raise Exception(resp.json()["error"])
                    else:
                        return resp.json()["data"]["file_id"]

            except Exception as e:
                msg = "File Upload failed for {} for file {}: {}".format(self.__leaf_name, file_path, e)
                raise Exception(msg)
        else:
            msg = "File Upload failed for leaf {} : {}".format(self.__leaf_name, "leaf not logged in")
            raise Exception(msg)

    def file_download(self, file_id):
        if self.__status == "logged_in":
            try:
                if not os.path.exists(AGGREGATED_OUTPUT_DIR):
                    os.makedirs(AGGREGATED_OUTPUT_DIR)

                url = self.__api_host + "/v1/file/download/" + file_id
                headers = {"accept": "*/*S"}
                resp = requests.get(url, headers=headers,
                                    auth=(self.__leaf_id, self.__access_token), verify=self.__verify)

                if resp.status_code != HTTPStatus.OK:
                    raise Exception(resp.json()["error"])

                if len(resp.content) == 0:
                    raise Exception("file not received")

                f = open(AGGREGATED_OUTPUT_DIR + '/' + file_id, 'wb')
                f.write(resp.content)
                f.close()

                return True
            except Exception as e:
                msg = "File Download failed for {} for file {}: {}".format(self.__leaf_name, file_id, e)
                raise Exception(msg)
        else:
            msg = "File Download failed for leaf {} : {}".format(self.__leaf_name, "leaf not logged in")
            raise Exception(msg)

    @property
    def leaf_id(self):
        return self.__leaf_id

    @property
    def access_token(self):
        return self.__access_token

    @property
    def is_logged_in(self):
        return self.__status == "logged_in"
