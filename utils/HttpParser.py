#!usr/bin/env python
# -*- coding:utf-8 -*-

from requests.auth import HTTPBasicAuth
import json
import time
import requests
import RrdLogger

DEFAULT_POST_HEADER = {'content-type': "application/x-www-form-urlencoded;charset=UTF-8"}
DEFAULT_JSON_HEADER = {'content-type': "application/json;charset=UTF-8"}
DEFAULT_FILE_HEADER = {}
GLOBAL_API_REQUEST_TIMEOUT = 60
logger =  RrdLogger.RrdLogger().getLogger('HTTPSERVER')

def response_dump(rsp):
    content = json.dumps(rsp, sort_keys=True, indent=4, ensure_ascii=False)
    logger.info(content)
    return content

def echo_req_and_resp(function):
    def wrapper(*args, **kwargs):
        logger.info("request method: {}()".format(function.__name__))
        if "url" in kwargs.keys():
            logger.info("Requesting Url:{}".format(kwargs["url"]))
        if "timeout" in kwargs.keys():
            logger.info("Timeout Limited To {} seconds".format(kwargs["timeout"]))
        start_time = time.time()
        logger.info("Input Params: ")
        if "params" in kwargs.keys():
            response_dump(kwargs["params"])
        if "data" in kwargs.keys():
            response_dump(kwargs["data"])
        if "json" in kwargs.keys():
            response_dump(kwargs["json"])
        rsp = function(*args, **kwargs)
        end_time = time.time()
        logger.info("Response in {} seconds:".format(float('%.6f' % (end_time - start_time))))
        try:
            response_dump(rsp.json())
        except ValueError:
            logger.info(rsp.text)
        except TypeError:
            logger.info(rsp.text)
        except RuntimeError:
            logger.info(rsp.text)
        if "responseTime" in kwargs.keys() and kwargs["responseTime"] == True:
            return rsp, float('%.6f' % (end_time - start_time))
        else:
            return rsp
    return wrapper


class Client():
    def __init__(self):
        self.session = requests.Session()

    @echo_req_and_resp
    def get(self, url, params=None, timeout=GLOBAL_API_REQUEST_TIMEOUT, auth=None, responseTime=False):
        return self.session.get(url=url, params=params, timeout=timeout, auth=auth, verify=False)

    @echo_req_and_resp
    def post(self, url, data, headers=DEFAULT_POST_HEADER,
             timeout=GLOBAL_API_REQUEST_TIMEOUT, auth=None, responseTime=False):
        return self.session.post(url=url, data=data, headers=headers, timeout=timeout, auth=auth, verify=False)

    @echo_req_and_resp
    def postJson(self, url, json, headers=DEFAULT_JSON_HEADER,
                 timeout=GLOBAL_API_REQUEST_TIMEOUT, auth=None, responseTime=False):
        return self.session.post(url=url, json=json, headers=headers, timeout=timeout, auth=auth, verify=False)

    @echo_req_and_resp
    def postFile(self, url, json, headers=DEFAULT_FILE_HEADER,
                 timeout=GLOBAL_API_REQUEST_TIMEOUT, auth=None, responseTime=False):
        return self.session.post(url=url, json=json, headers=headers, timeout=timeout, auth=auth, verify=False)

    def proc_request(self, req, responseTime=False):
        auth = None
        if "method" in req.keys():
            if "auth" in req.keys() and req["auth"] is not None:
                if req["auth"]["type"] == "basic":
                    auth = HTTPBasicAuth(req["auth"]["user"], req["auth"]["password"])
            else:
                pass
            if "headers" in req.keys() and req["headers"] is not None:
                headers = req["headers"]
            else:
                if req["method"] == "POST":
                    headers = DEFAULT_POST_HEADER
                elif req["method"] == "JSON":
                    headers = DEFAULT_JSON_HEADER
                elif req["method"] == "FILE":
                    headers = DEFAULT_FILE_HEADER
                else:
                    headers = None
            if req["method"] == "GET":
                return self.get(url=req["request_url"], params=req["parameter"],
                                auth=auth,
                                responseTime=responseTime)
            elif req["method"] == "JSON":
                return self.postJson(url=req["request_url"], json=req["parameter"],
                                     auth=auth,
                                     headers=headers,
                                     responseTime=responseTime)
            elif req["method"] == "POST":
                # print("****---*****"+ req["request_url"] +"?" + req["parameter"])
                return self.post(url=req["request_url"], data=req["parameter"],
                                 auth=auth,
                                 headers=headers,
                                 responseTime=responseTime)
            else:
                # req["method"] == "FILE"
                return self.postFile(url=req["request_url"], json=req["parameter"],
                                     auth=auth,
                                     headers=headers,
                                     responseTime=responseTime)
        else:
            logger.info("{}:request data miss 'method'".format(req['request_url']))
            #sys.exit()


def set_request(method, url, req = None, auth = None, **kwargs):
    if req == None or req == '':
        parameter = {}
        for key in kwargs.keys():
            parameter[key] = kwargs[key]
        if auth == None:
            request_instance = {'method': method, 'request_url': url, 'parameter': parameter}
        else:
            request_instance = {"auth": auth, 'method': method, 'request_url': url, 'parameter': parameter}
    else:
        if auth == None:
            request_instance = {'method': method, 'request_url': url, 'parameter': json.loads(req)}
        else:
            request_instance = {"auth": auth, 'method': method, 'request_url': url, 'parameter': json.loads(req)}
    return request_instance