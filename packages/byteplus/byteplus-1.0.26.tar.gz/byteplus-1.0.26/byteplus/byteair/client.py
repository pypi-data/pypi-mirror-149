from datetime import datetime
from datetime import timedelta
import logging
from optparse import Option
from typing import Optional

from byteplus.common.client import CommonClient
from byteplus.common.protocol import *
from byteplus.core import BizException
from byteplus.core import MAX_WRITE_ITEM_COUNT, MAX_IMPORT_ITEM_COUNT
from byteplus.core import Region
from byteplus.core.context import Param
from byteplus.byteair.url import _GeneralURL
from byteplus.byteair.protocol import *
from byteplus.core.option import Option as CoreOption
from byteplus.core.options import Options

log = logging.getLogger(__name__)

_ERR_MSG_TOO_MANY_ITEMS = "Only can receive max to {} items in one request".format(MAX_IMPORT_ITEM_COUNT)

_DEFAULT_PREDICT_SCENE = "default"
_DEFAULT_CALLBACK_SCENE = "default"


class Client(CommonClient):

    def __init__(self, param: Param):
        super().__init__(param)
        self._general_url: _GeneralURL = _GeneralURL(self._context)

    def do_refresh(self, host: str):
        self._general_url.refresh(host)

    def write_data(self, data_list: list, topic: str, *opts: Option) -> WriteResponse:
        if len(data_list) > MAX_IMPORT_ITEM_COUNT:
            raise BizException(_ERR_MSG_TOO_MANY_ITEMS)

        url_format: str = self._general_url.write_data_url_format
        url: str = url_format.replace("#", topic)
        response: WriteResponse = WriteResponse()
        self._http_caller.do_json_request(url, data_list, response, *opts)
        log.debug("[ByteplusSDK][WriteData] rsp:\n %s", response)
        return response

    def predict(self, request: PredictRequest, *opts: CoreOption) -> PredictResponse:
        url_format: str = self._general_url.predict_url_format
        options: Options = CoreOption.conv_to_options(opts)
        scene: str = _DEFAULT_PREDICT_SCENE
        if options.scene:
            scene = options.scene
        url: str = url_format.replace("#", scene)
        response: PredictResponse = PredictResponse()
        self._http_caller.do_pb_request_with_opts_object(url, request, response, options)
        log.debug("[ByteplusSDK][Predict] rsp:\n%s", response)
        return response

    def callback(self, request: CallbackRequest, *opts: CoreOption) -> CallbackResponse:
        url: str = self._general_url.callback_url
        options: Options = CoreOption.conv_to_options(opts)
        if not options.scene:
            options.scene = _DEFAULT_CALLBACK_SCENE
        request.scene = options.scene
        response: CallbackResponse = CallbackResponse()
        self._http_caller.do_pb_request_with_opts_object(url, request, response, options)
        log.debug("[ByteplusSDK][Callback] rsp:\n%s", response)
        return response


class ClientBuilder(object):
    def __init__(self):
        self._param = Param()

    def tenant_id(self, tenant_id: str):
        self._param.tenant_id = tenant_id
        return self

    def project_id(self, project_id: str):
        self._param.tenant = project_id
        return self

    def token(self, token: str):
        self._param.token = token
        return self

    def schema(self, schema: str):
        self._param.schema = schema
        return self

    def hosts(self, hosts: list):
        self._param.hosts = hosts
        return self

    def headers(self, headers: dict):
        self._param.headers = headers
        return self

    def region(self, region: Region):
        self._param.region = region
        return self

    def ak(self, ak: str):
        self._param.ak = ak
        return self

    def sk(self, sk: str):
        self._param.sk = sk
        return self

    def use_air_auth(self):
        self._param.use_air_auth = True
        return self

    def build(self) -> Client:
        return Client(self._param)
