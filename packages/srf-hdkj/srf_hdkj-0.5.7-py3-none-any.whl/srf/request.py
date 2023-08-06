# -*- coding: utf-8 -*-
from srf.utils import ObjectDict
from sanic.exceptions import InvalidUsage
from sanic.request import Request as SanicRequest


class SRFRequest(SanicRequest):
    def __init__(self, *args, **kwargs):
        super(SRFRequest, self).__init__(*args, **kwargs)
        self.user = None

    @property
    def data(self):
        try:
            data = self.json
        except InvalidUsage as exc:
            data = self.form
        data = {} if data is None else data
        return data