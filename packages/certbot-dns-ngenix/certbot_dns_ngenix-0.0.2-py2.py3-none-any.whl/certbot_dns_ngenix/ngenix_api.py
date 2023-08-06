"""NGENIX API wrapper"""
import sys
import logging

from typing import Any, Callable, Dict, List

import json
import uuid
import requests
from requests import Response

logger = logging.getLogger(__name__)

class Error(Exception):
    pass

class ClientError(Error):
    pass

class ModelError(ClientError):
    pass

class Client(object):
    __instance = None
    def __new__(cls, headers=None, auth=None, verify=None, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(Client, cls).__new__(cls, *args, **kwargs)
            cls.__instance.__uuid = None
        return cls.__instance
    def __init__(self, headers=None, auth=None, verify=None) -> None:
        if self.__uuid is None:
            self.__uuid = uuid.uuid4()
            self._session = requests.Session()
            self._session.auth = auth
            self._session.headers = headers
            self._session.verify = verify
            logger.debug("Client {} initialized".format(self.__uuid))
    def __repr__(self):
        return "Client({}, {}, {})".format(self._session.headers, self._session.auth, self._session.verify)
    def __request(self, method: str, url=None, data=None) -> Response:
        logger.debug("Sending {} request to {}".format(method, url))
        res = None
        if not url:
            url = self._url
        try:            
            if method.upper() == "GET":
                res = self._session.get(url, data=data)
            elif method == "POST":
                res = self._session.post(url, data=data)
            elif method == "PUT":
                res = self._session.put(url, data=data)
            elif method == "PATCH":
                res = self._session.patch(url, data=data)
            elif method == "DELETE":
                res = self._session.delete(url, data=data)
            else:
                raise ClientError("Unknown HTTP method: {}".format(method))
        except Exception as e:
            raise ClientError("{}".format(e))
        if res is not None:
            if res.status_code == 200:
                logger.debug('{} {}\nReceived response:\n{}'.format(method, url, json.dumps(json.loads(res.content), indent=2, sort_keys=True)))
                return res.content
            elif res.content:
                body = json.loads(res.content)
                if body["detail"]:
                    raise ClientError("Got error: {}, {}".format(body["title"], body["detail"]))
                else:
                    raise ClientError("Got error: {}".format(body["message"]))
            elif res.reason:
                raise ClientError("Got error: {}".format(res.reason))
            else:
                raise ClientError("Unknown error")
    def get(self, url=None) -> Response:
        return self.__request("GET", url)
    def post(self, url=None, data=None) -> Response:
        return self.__request("POST", url, data)
    def put(self, url=None, data=None) -> Response:
        return self.__request("PUT", url, data)
    def patch(self, url=None, data=None) -> Response:
        return self.__request("PATCH", url, data)
    def delete(self, url=None) -> Response:
        return self.__request("DELETE", url)

class Object(object):
    def __iter__(self):
        for k, v in self.__dict__.items():
            yield (k, v)
    def __repr__(self):
        return json.dumps(self.__dict__)
    def __str__(self):
        return "{}({})".format(self.__class__.__name__.capitalize(), json.dumps(self.__dict__, indent=2, sort_keys=True))
    def to_dict(self):
        data: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if k is None:
                continue
            if v is None:
                continue
            if k.startswith("_"):
                continue
            if callable(v):
                continue
            if isinstance(v, list):
                data[k] = []
                for e in v:
                    if isinstance(e, Object):
                        data[k].append(e.to_dict())
                    else:
                        data[k].append(e)
            elif isinstance(v, Object):
                data[k] = v.to_dict()
            else:
                data[k] = v
        return data

class Reference(Object):
    _link: str = None
    id: int = None
    def __init__(self, id: int, link: str) -> None:
        super().__init__()
        self.id = id
        self._link = link
    def to_dict(self):
        return {
            "id": self.id
        }
    def link(self):
        return self._link

class Record(Object):
    targetGroupRef: Reference = None
    configRef: Reference = None
    name: str = None
    type: str = None
    data: str = None
    def __init__(self, name: str = None, type: str = None, data: Any = None, configRef: Reference = None, targetGroupRef: Reference = None) -> None:
        super().__init__()
        if not name:
            name = "@"
        if not type:
            type = "A"
        if type.upper() not in ["A", "CNAME", "MX", "AAAA", "SRV", "NS", "TXT", "CAA"]:
            raise ModelError("Wrong DNS resource record type {}, only A, CNAME, MX, AAAA, SRV, NS, TXT and CAA allowed\n{} {}".format(type, name, data))
        self.type = type.upper()
        self.name = name
        self.data = data
        if configRef is not None:
            self.configRef = Reference(**configRef)
        if targetGroupRef is not None:
            self.targetGroupRef = Reference(**targetGroupRef)

class Model(Object):
    _client = None
    _model: Dict[str, Any] = {}
    def __init__(self, client: Client = None, url: str = None) -> None:
        super().__init__()
        if client is None:
            self._client = Client()
        else:
            self._client = client
        self._model = json.loads(self._client.get(url))
    def __iter__(self):
        for k in self._model:
            yield (k, self._model[k])
    def __str__(self):
        return "{}({})".format(self.__class__.__name__, json.dumps(self._model, indent=2, sort_keys=True))

class WhoAmI(Model):
    __url = "https://api.ngenix.net/api/v3/whoami"
    _userRef: Reference = None
    def __init__(self, client: Client = None, url: str = None) -> None:
        if url is None:
            url = self.__url
        super().__init__(client, url)
        self._userRef = Reference(**self._model["userRef"])
    def user(self):
        return User(self._userRef.id)

class User(Model):
    __url = "https://api.ngenix.net/api/v3/user/{}"
    _id: int = None
    _customerRef: Reference = None
    email: str = None
    firstName: str = None
    lastName: str = None
    phone: str = None
    def __init__(self, user_id: int = None, client: Client = None, url: str = None) -> None:
        if url is None:
            url = self.__url.format(user_id)
        super().__init__(client, url)
        self._id = self._model["id"]
        self._customerRef = Reference(**self._model["customerRef"])
        self.email = self._model["email"]
        self.firstName = self._model["firstName"]
        self.lastName = self._model["lastName"]
        self.phone = self._model["phone"]
    def id(self):
        return self._id
    def customer(self):
        return Customer(self._customerRef.id)

class Customer(Model):
    __url = "https://api.ngenix.net/api/v3/customer/{}"
    _id: int = None
    _name: str = None
    _active: bool = None
    _status: str = None
    def __init__(self, customer_id: int = None, client: Client = None, url: str = None) -> None:
        if url is None:
            url = self.__url.format(customer_id)
        super().__init__(client, url)
        self._id = self._model["id"]
        self._name = self._model["name"]
        self._active = self._model["active"]
        self._status = self._model["status"]
    def id(self):
        return self._id
    def services(self):
        return Services(self._id)

class Services(Model):
    __url = "https://api.ngenix.net/api/v3/customer/{}/service"
    __customer_id = None
    def __init__(self, customer_id: int = None, client: Client = None, url: str = None) -> None:
        if url is None:
            url = self.__url.format(customer_id)
        super().__init__(client, url)
        self.__customer_id = customer_id
    def __iter__(self):
        for e in self._model["elements"]:
            yield e
    def dns(self):
        for e in self._model["elements"]:
            if e["serviceAbbreviation"].upper() == "DNS":
                return DNS(self.__customer_id)

class DNS(Model):
    __url = "https://api.ngenix.net/api/v3/dns-zone?customerId={}"
    def __init__(self, customer_id: int = None, client: Client = None, url: str = None) -> None:
        if url is None:
            url = self.__url.format(customer_id)
        super().__init__(client, url)
    def __iter__(self):
        for e in self._model["elements"]:
            yield e
    def zone(self, name):
        for e in self._model["elements"]:
            if e["name"].lower() == name.lower():
                return Zone(e["id"])

class Zone(Model):
    __url = "https://api.ngenix.net/api/v3/dns-zone/{}"
    id: int = None
    name: str = None
    soa: Dict[str, Any] = {}
    nameservers: List[str] = []
    records: List[Record] = []
    def __init__(self, id: int = None, client: Client = None, url: str = None) -> None:
        if url is None:
            url = self.__url.format(id)
        self.__url = url
        super().__init__(client, url)
        self.id = self._model["id"]
        self.name = self._model["name"]
        self.soa = self._model["soa"]
        self.nameservers = self._model["nameservers"]
        self.records = []
        for r in self._model["records"]:
            self.records.append(Record(**r))
    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "soa": self.soa,
            "nameservers": self.nameservers,
            "records": self.records
        }
    def _remove(self, name, type, data):
        for r in self.records:
            if r.name == name and r.type == type and r.data == data:
                self.records.remove(r)
            elif r.name == name and r.type == type:
                self.records.remove(r)
        return self.records
    def add(self, name: str, type: str, data = None):
        if data is not None:
            self._remove(name, type, data)
            self.records.append(Record(name, type, data))
            records = []
            for r in self.records:
                records.append(r.to_dict())
            self._client.patch(self.__url, json.dumps({"records": records}))
        return records
    def delete(self, name: str, type: str, data = None):
        if data is not None:
            self._remove(name, type, data)
            records = []
            for r in self.records:
                records.append(r.to_dict())
            self._client.patch(self.__url, json.dumps({"records": records}))
        return records

class Ngenix(object):
    _url = "https://api.ngenix.net/api/v3"
    services: Services = None
    def __init__(self, email: str, token: str, headers=None, verify=True) -> None:
        api = Client(headers, (str(email + "/token"), str(token)), verify)
        whoami = WhoAmI(api)
        self.services = whoami.user().customer().services()