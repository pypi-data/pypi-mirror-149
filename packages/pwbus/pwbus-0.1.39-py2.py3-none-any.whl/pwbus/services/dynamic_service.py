# PWBus - DynamicService Class
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Mon Nov 18 09:30:57 -03 2019

import importlib
import os.path
import traceback

from pwbus.commons.logging import *

# DynamicService
#
#


class DynamicService():

    def __init__(self, service_id, payload, isDebugEnabled=False):
        try:
            service_name = service_id.split('.')
            module_name = f'pwbus_services.{service_name[0]}.{service_name[1]}'
            class_name = service_name[1].capitalize()
        except:
            log_debug(
                f'🟥 DynamicService - Invalid service_id [{service_id}] specify "module.class" (lowercase)')
            return

        try:
            if not os.path.isfile(module_name.replace('.', '/') + '.py'):
                log_debug(
                    f'🟥 DynamicService - module not found [{service_id}] specify "module.class" (lowercase)')
                return

            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
            self.instance = class_(payload)

            if isDebugEnabled:
                log_debug(
                    f'DynamicService - Module [{module_name}] Class [{class_name}] instance created')

        except:
            log_debug(
                f'⚠️ DynamicService - WARNING!!! Class not found or with errors for service_id [{service_id}]')
            traceback.print_exc()
            raise

    # DynamicService.getInstance
    #
    def getInstance(self):
        return self.instance

    # DynamicService.isLoaded
    #
    def isLoaded(self):
        return True if self.instance else False
