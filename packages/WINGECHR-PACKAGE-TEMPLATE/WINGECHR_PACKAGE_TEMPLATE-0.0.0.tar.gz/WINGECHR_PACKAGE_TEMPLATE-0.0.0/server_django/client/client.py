# coding: utf-8
import logging  # noqa

import requests


class Client:
    def __init__(self, url, token=None, username=None, password=None):
        self.url = url
        self.token = token if token else self.get_token(username, password)
        self.headers = {"Authorization": "Token %s" % self.token}

    @staticmethod
    def _check_response(r):
        try:
            r.raise_for_status()
        except Exception:
            c = r.text
            raise Exception(c)

    def get_token(self, username, password):
        url = self.url + "get_token/?format=json"
        data = {"username": username, "password": password}
        r = requests.post(url, data=data)
        self._check_response(r)
        token = r.json()["token"]
        return token

    def get_objects(self, object):
        url = self.url + object + "/"

        r = requests.get(url, headers=self.headers)
        self._check_response(r)
        data = r.json()
        return data

    def get_object(self, object, id):
        url = self.url + object + "/%d/" % id
        r = requests.get(url, headers=self.headers)
        self._check_response(r)
        data = r.json()
        return data

    def create_object(self, object, data):
        url = self.url + object + "/"
        r = requests.post(url, headers=self.headers, data=data)
        self._check_response(r)
        data = r.json()
        return data

    def update_object(self, object, id, data):
        url = self.url + object + "/%d/" % id
        r = requests.patch(url, headers=self.headers, data=data)
        self._check_response(r)
        data = r.json()
        return data

    def delete_object(self, object, id):
        url = self.url + object + "/%d/" % id
        r = requests.delete(url, headers=self.headers)
        self._check_response(r)

    def options(self, object):
        url = self.url + object + "/"
        r = requests.options(url, headers=self.headers)
        self._check_response(r)
        data = r.json()
        return data

    def get_writable_attributes(self, object, method="POST"):
        opts = self.options(object)["actions"][method]
        res = []
        for name, inf in opts.items():
            if not inf["read_only"]:
                res.append(name)
        return res
