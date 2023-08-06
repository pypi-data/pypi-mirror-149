# PWBus - Service Class
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Mon Nov 18 10:58:09 -03 2019

import importlib
from time import sleep
from datetime import datetime
import traceback

from pwbus.commons.logging import *
from pwbus.services.service_unique_id import ServiceUniqueId

# Service
#
#


class Service():

    def __init__(self, payload):
        self.payload = payload
        self.setField('__pwbus-service-unique-id__', ServiceUniqueId().get())

    # Service.execute
    #
    def execute(self):
        self.main()
        return self.payload

    # Service.main - override this in your service
    #
    def main(self):
        return None

    # Service.setField
    #
    def setField(self, name, value):
        self.payload[name] = value

    # Service.getField
    #
    def getField(self, name):
        return self.payload[name]

    # Service.deleteField
    #
    def deleteField(self, name):
        del self.payload[name]

    # Service.getDateTime
    #
    def getDateTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    # Service.getDateTimeFormat
    #
    def getDateTimeFormat(self, my_format):
        return datetime.now().strftime(my_format)

    # Service.sleep
    #
    def sleep(self, ms):
        sleep(ms)
