import os
import sys
import jwt
import json
import time
import logging
import requests
import pandas as pd
from halo import Halo
from urllib.request import urlopen
from colorlog import ColoredFormatter
from datetime import datetime, timedelta
from requests.exceptions import ConnectionError

class InnocuousAPI:
    def __init__(self, token=None, **kwargs):
        self.version = "1.0.10"
        self.debug = True if 'debug' in kwargs and kwargs['debug'] else False
        self._init_logger()
        
        if 'host' in kwargs:
             self.host = kwargs['host']
        else:
            self.host = os.getenv("INNOCUOUSBOOK_HOST", "https://dashboard.innocuous.ai")

        if token:
            self.token = token
        else:
            self.token = os.getenv("INNOCUOUSBOOK_TOKEN", "")

        self.session = requests.Session()
        self.headers = None
        self.jwt_token = None
        self.error_flag = False
        self.username = None
        self.userid = None
        
        
    def _init_logger(self):
        """Initialize Logger
        """
        if self.debug:
            LOG_LEVEL = logging.DEBUG
        else:
            LOG_LEVEL = logging.INFO
        datefmt = '%Y-%m-%d %H:%M:%S'
        LOGFORMAT = "%(log_color)s[%(asctime)s][%(levelname)-8s]%(reset)s %(log_color)s%(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT, datefmt)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        self.log = logging.getLogger('innocuousboolAPI')
        self.log.setLevel(LOG_LEVEL)
        self.log.addHandler(stream)

    def _get_jwt_token(self):
        """Get JWT token
        Returns:
            Is success
        """
        try:
            if self.error_flag:
                self.log.error("token error or empty")
                return False

            if self.jwt_token:
                decode_token = jwt.decode(self.jwt_token['access'], options={"verify_signature": False})
                dt = int(datetime.now().timestamp())
                if dt < decode_token['exp']:
                    self.log.debug("unnecessary refresh token")
                    return True

                url = self.host + "/api/user/token/refresh/"
                r = self.session.post(url, data={"refresh": self.jwt_token["refresh"]})
                if r.status_code == 200:
                    self.jwt_token = json.loads(r.text)
                    self.headers = {"Authorization": f"Bearer {self.jwt_token['access']}"}
                    self._set_userinfo()
                    self.log.debug("refresh token")
                else:
                    self.jwt_token = None
                    self._get_jwt_token()
            else:
                url = self.host + "/api/user/token/"
                self.headers = {"Authorization": f"Bearer {self.token}"}
                r = self.session.post(url, data={"username": "x", "password": "x"}, headers=self.headers)
                if r.status_code == 200:
                    self.jwt_token = json.loads(r.text)
                    self.headers = {"Authorization": f"Bearer {self.jwt_token['access']}"}
                    self._set_userinfo()
                    self.log.debug("get token")
                else:
                    self.error_flag = True
                    return False
        except ConnectionError:
            self.log.error("Cannot connect to server")
            sys.exit(1)

    
    def _set_userinfo(self):
        """Get user information from JWT
        """
        decode_token = jwt.decode(self.jwt_token['access'], options={"verify_signature": False})
        self.username = decode_token['user_name']
        self.userid = decode_token['user_id']

    def check_login(self):
        """Check is login
        Returns:
            Is login
        """
        self._get_jwt_token()
        url = self.host + "/api/user/is-login"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)["message"] == "ok":
            return True
        return False

    def get_server_version(self):
        """Get server version
        Returns:
            Server api version
        """
        self.check_login()
        url = self.host + "/version"
        r = self.session.get(url)
        if r.status_code == 200:
            return json.loads(r.text)['version']
        return False
    
    def get_api_version(self):
        """Get api version
        Returns:
            Api version
        """
        return self.version

    def create_experiment(self, recipe):
        """Create experiment
        Args: 
            recipe: Recipe of Experiment

        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # return data
            }
        """
        self._get_jwt_token()
        url = self.host + "/api/experiment"
        r = self.session.post(url, headers=self.headers, json=recipe)
        if r.status_code == 200:
            return json.loads(r.text)
        error = {
            "code": -100,
            "data": r.text
        }
        return error

    def get_experiment(self, id):
        """Get information of experiment 
        Args: 
            id: Id of Experiment

        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # information of experiment 
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/{id}"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return json.loads(r.text)['data'][0]
        return None

    def list_experiments(self):
        """List all experiment 
        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # all experiment 
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return json.loads(r.text)['data']
        return None   
    
    def wait_experiment_finish(self, id, quiet_mode=False, timeout=None):
        """Wait for experiment finish
        Args:
            id: Id of experiment
            quiet_mode: Whether to display log
            timeout: The longest waiting time
        Returns:
            Is finish or timeout
        """
        if timeout:
            end_time = datetime.now() + timedelta(minutes=timeout)
        else:
            end_time = datetime.now() + timedelta(days=3650)

        while datetime.now() < end_time:
            if not quiet_mode:
                self.log.info("Waiting for experiment finish")
            status = self.get_experiment(id)["status"]
            if status == "End":
                return True
            time.sleep(10)
        if not quiet_mode:
            self.log.error("Timeout")
        return False
    
    def wait_experiment_status(self, id, status):
        """Wait for the experiment to reach a certain state
        Args:
            id: Id of experiment
            status: Name of status
        Returns:
            Reached
        """
        while True:
            s = self.get_experiment(id)["status"]
            if s == status:
                return True
            time.sleep(10)

    def get_best_experiment_config(self, id):
        """Get experiment result
        Args:
            id: Id of experiment
        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # experiment result
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/result/{id}"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            result_url = json.loads(r.text)['data']['bestconfig']['path']
            f = urlopen(result_url)
            result_json = f.read()
            return json.loads(result_json)
        else:
            self.log.info('request error, returning None')
            return None

    def get_experiment_dataframe(self, id):
        """Get experiment result
        Args:
            id: Id of experiment
        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # experiment result
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/result/{id}"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            result_url = json.loads(r.text)['data']['dataframe']['path']
            f = urlopen(result_url)
            result_json = pd.read_pickle(f)
            return json.loads(result_json)
        else:
            self.log.info('request error, returning None')
            return None

    def kill_experiment(self, id):
        """Kill experiment
        Args:
            id: Id of experiment
        Returns:
            Is success
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/{id}"
        r = self.session.delete(url, headers=self.headers, data={"action": "kill"})
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return True
        return False

    def delete_experiment(self, id):
        """Delete experiment
        Args:
            id: Id of experiment
        Returns:
            Is success
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/{id}"
        r = self.session.put(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return True
        return False

    def create_endpoint(self, recipe):
        """Create endpoint
        Args: 
            recipe: Recipe of endpoint

        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # return data
            }
        """
        self._get_jwt_token()
        url = self.host + "/api/endpoint"
        r = self.session.post(url, headers=self.headers, json=recipe)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return json.loads(r.text)
        return False

    def get_endpoint(self, id):
        """Get information of endpoint 
        Args: 
            id: Id of endpoint

        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # information of endpoint 
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/endpoint/{id}"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return json.loads(r.text)['data'][0]
        return None
    
    def list_endpoints(self):
        """List all endpoint 
        Returns:
            {
                "code": 0,      # if success is 0
                "data": data    # all endpoint 
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/endpoint"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return json.loads(r.text)['data']
        return None

    def delete_endpoint(self, id):
        """Delete endpoint
        Args:
            id: Id of endpoint
        Returns:
            Is success
        """
        self._get_jwt_token()
        url = self.host + f"/api/endpoint/{id}"
        r = self.session.delete(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)['code'] == 0:
            return True
        return False

    def call_endpoint_predict(self, id, data):
        """Call endpoint api of predict
        Args:
            id: Id of endpoint
            data: data
        Returns:
            Result
        """
        endpoint = self.get_endpoint(id)
        url = endpoint["url"] + "/predict"
        headers = {"USERNAME": self.username, "TOKEN": self.token }
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()
        return False

    def call_endpoint_predict_file(self, id, files):
        """Call endpoint api of predict_file
        Args:
            id: Id of endpoint
            files: path of file
        Returns:
            Result
        """
        endpoint = self.get_endpoint(id)
        url = endpoint["url"] + "/predict_file"
        send_files = []
        for file in files:
            send_files.append(('files', open(file, 'rb')))
        headers = {"USERNAME": self.username, "TOKEN": self.token }
        r = requests.post(url, headers=headers, files=send_files)
        if r.status_code == 200:
            return r.json()
        return False

    def call_endpoint_continuous_learning(self, id, dataset):
        """Call endpoint api of continous_learnin
        Args:
            id: Id of endpoint
            dataset: dataset
        Returns:
            Result
        """
        self._get_jwt_token()
        upload = Halo(text=f'Upload {dataset}...', spinner='dots')
        upload.start()
        endpoint = self.get_endpoint(id)
        url = endpoint["url"] + "/get_storage_upload_url"
        file_name = os.path.basename(dataset)
        headers = {"USERNAME": self.username, "TOKEN": self.token }
        r = requests.post(url, headers=headers, json={'filename': file_name})
        if r.status_code == 200 and r.json()['code'] == 0:
            r_json = r.json()
            s3_data = r_json['data']
            s3_path = r_json['path']
            with open(dataset, 'rb') as f:
                r2 = requests.post(s3_data['url'], data={
                        "key": s3_data["fields"]["key"],
                        "policy": s3_data["fields"]["policy"],
                        "x-amz-algorithm": s3_data["fields"]["x-amz-algorithm"],
                        "x-amz-credential": s3_data["fields"]["x-amz-credential"],
                        "x-amz-date": s3_data["fields"]["x-amz-date"],
                        "x-amz-signature": s3_data["fields"]["x-amz-signature"]},
                        files={"file": f})
            
            if r2.status_code == 204:
                url = endpoint["url"] + '/dateset_upload'
                data = {
                    'dataset': {
                        "name": file_name, 
                        "path": s3_path
                    }
                }
                r3 = requests.post(url, json=data, headers=headers)
                if r3.status_code == 200:
                    upload.succeed("Upload success")
                    return True
        upload.fail("Upload failed")
        return False

    def list_model(self):
        """List all model
        Returns:
            {
                "code": 0,     
                "data": data
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/model"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)["code"] == 0:
            return json.loads(r.text)["data"]
        return None

    def list_function(self):
        """List all function
        Returns:
            {
                "code": 0,     
                "data": data
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/function"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)["code"] == 0:
            return json.loads(r.text)["data"]
        return None

    def list_dataset(self):
        """List all dataset
        Returns:
            {
                "code": 0,     
                "data": data
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/dataset"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)["code"] == 0:
            return json.loads(r.text)["data"]
        return None

    def list_requirementst(self):
        """List all requirementst
        Returns:
            {
                "code": 0,     
                "data": data
            }
        """
        self._get_jwt_token()
        url = self.host + f"/api/experiment/requirements"
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and json.loads(r.text)["code"] == 0:
            return json.loads(r.text)["data"]
        return None

    def upload_model(self, name, file_path):
        """Upload model
        Args:
            name: name of model
            file_path: folder of model
        Returns:
            Is success
        """
        self.create_folder(f"model/{name}/")
        self._get_jwt_token()
        upload = Halo(text=f"Upload {name}...", spinner="dots")
        upload.start()
        file_list = []
        for root, _, files in os.walk(file_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = abs_path.replace(file_path, "")
                file_list.append({
                    "name": os.path.join(name, rel_path),
                    "path": os.path.join(root, file)
                })
                
        for index, item in enumerate(file_list):
            upload.text = f"Uploading {index+1}/{len(file_list)}"
            url = self.host + "/api/files/upload_fmd"
            r = requests.post(url, headers=self.headers, json={"file_name": item["name"], "file_type": "model"})
            if r.status_code == 200 and r.json()['code'] == 0:
                r_json = r.json()
                s3_data = r_json['data']
                with open(item["path"], 'rb') as f:
                    r2 = requests.post(s3_data['url'], data={
                            "key": s3_data["fields"]["key"],
                            "policy": s3_data["fields"]["policy"],
                            "x-amz-algorithm": s3_data["fields"]["x-amz-algorithm"],
                            "x-amz-credential": s3_data["fields"]["x-amz-credential"],
                            "x-amz-date": s3_data["fields"]["x-amz-date"],
                            "x-amz-signature": s3_data["fields"]["x-amz-signature"]},
                            files={"file": f})
                if r2.status_code == 204:
                    continue
            upload.fail("Upload failed")
            return False
        upload.succeed("Upload success")
        return True

    def upload_function(self, name, file_path):
        """Upload function
        Args:
            name: name of function
            file_path: folder of function
        Returns:
            Is success
        """
        self.create_folder(f"function/{name}/")
        self._get_jwt_token()
        upload = Halo(text=f"Upload {name}...", spinner="dots")
        upload.start()
        file_list = []
        for root, _, files in os.walk(file_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = abs_path.replace(file_path, "")
                file_list.append({
                    "name": os.path.join(name, rel_path),
                    "path": os.path.join(root, file)
                })
                
        for index, item in enumerate(file_list):
            upload.text = f"Uploading {index+1}/{len(file_list)}"
            url = self.host + "/api/files/upload_fmd"
            r = requests.post(url, headers=self.headers, json={"file_name": item["name"], "file_type": "function"})
            if r.status_code == 200 and r.json()['code'] == 0:
                r_json = r.json()
                s3_data = r_json['data']
                with open(item["path"], 'rb') as f:
                    r2 = requests.post(s3_data['url'], data={
                            "key": s3_data["fields"]["key"],
                            "policy": s3_data["fields"]["policy"],
                            "x-amz-algorithm": s3_data["fields"]["x-amz-algorithm"],
                            "x-amz-credential": s3_data["fields"]["x-amz-credential"],
                            "x-amz-date": s3_data["fields"]["x-amz-date"],
                            "x-amz-signature": s3_data["fields"]["x-amz-signature"]},
                            files={"file": f})
                if r2.status_code == 204:
                    continue
            upload.fail("Upload failed")
            self.log.error()
            return False
        upload.succeed("Upload success")
        return True

    def upload_dataset(self, file_path):
        """Upload dataset
        Args:
            name: name of dataset
            file_path: path of dataset
        Returns:
            Is success
        """
        self._get_jwt_token()
        name = os.path.basename(file_path)
        upload = Halo(text=f"Upload {name}...", spinner="dots")
        upload.start()
        url = self.host + "/api/files/upload_fmd"
        r = requests.post(url, headers=self.headers, json={"file_name": name, "file_type": "dataset"})
        if r.status_code == 200 and r.json()['code'] == 0:
            r_json = r.json()
            s3_data = r_json['data']
            with open(file_path, 'rb') as f:
                r2 = requests.post(s3_data['url'], data={
                        "key": s3_data["fields"]["key"],
                        "policy": s3_data["fields"]["policy"],
                        "x-amz-algorithm": s3_data["fields"]["x-amz-algorithm"],
                        "x-amz-credential": s3_data["fields"]["x-amz-credential"],
                        "x-amz-date": s3_data["fields"]["x-amz-date"],
                        "x-amz-signature": s3_data["fields"]["x-amz-signature"]},
                        files={"file": f})
            if r2.status_code == 204:
                upload.succeed("Upload success")
                return True
        upload.fail("Upload failed")
        return False

    def upload_requirementst(self, name, requirementst):
        """Upload requirementst
        Args:
            name: name of requirementst
            file_path: path of requirementst
        Returns:
            Is success
        """
        self._get_jwt_token()
        upload = Halo(text=f"Upload {name}...", spinner="dots")
        upload.start()
        url = self.host + "/api/experiment/requirementst"
        r = requests.post(url, headers=self.headers, json={"name": name, "value": requirementst, "remarks": name})
        if r.status_code == 200 and r.json()['code'] == 0:        
            upload.succeed("Upload success")
            return True
        upload.fail("Upload failed")
        return False
    
    def create_folder(self, name):
        """Create folder
        Args:
            name: full path of foler
        Returns:
            Is success
        """
        self._get_jwt_token()
        url = self.host + "/api/files/folder_fm"
        r = requests.post(url, headers=self.headers, json={"name": name})
        if r.status_code == 200 and r.json()['code'] == 0:
            return True
        return False
