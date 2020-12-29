import os
from unittest import TestCase

import requests


class TestAdminLogin(TestCase):
    def test_retrieve(self):
        print(os.getcwd())
        env_file = open('../.env', 'r')
        username = ""
        password = ""
        for line in env_file.readlines():
            if line.startswith("ADMIN_USER="):
                username = line.split("ADMIN_USER=")[1].strip()
            elif line.startswith("ADMIN_PASS="):
                password = line.split("ADMIN_PASS=")[1].strip()
        env_file.close()
        print(username)
        print(password)
        url = "http://localhost:9090/login"

        payload = "{\n  \"username\":\"" + username + "\", \n  \"password\":\"" + password + "\"\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        import json
        result = json.loads(response.text)
        refresh = result["refresh"]["token"]
        access = result["access"]["token"]
        admin_file = open("../.admin_file", 'w')
        admin_file.write("access:{}".format(access))
        admin_file.write("\n")
        admin_file.write("refresh:{}".format(refresh))
        admin_file.close()
        # print(response.text)
