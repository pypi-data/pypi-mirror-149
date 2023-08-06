import logging
from threading import Lock
from .HardwareHandlerFactory import HardwareHandlerFactory
from .ExecThread import *
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp
from .kerror import KERR

handler = None
mutex = Lock()

try:
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S')
    import coloredlogs
    coloredlogs.install()
except:
    pass

def handle(websocket, extensions, userPath):
    global handler
    ws = websocket
    import random, string
    letters = string.ascii_lowercase
    instanceTag = ''.join(random.choice(letters) for i in range(6))
    if handler:
        logging.error("new sock without close %s" %handler.dbgTag)
        handler.closed = True
    mutex.acquire()
    logging.warn("\033[1;32m New socket %s %s" %(ws, instanceTag))

    hardwareHandlerFactory = HardwareHandlerFactory()
    handler = hardwareHandlerFactory.handle('meowbit', websocket, extensions, userPath, instanceTag)
    handler.ws = ws
    while not ws.closed and not handler.closed:
        # blocking receive
        if not ws._link_messages.empty():
            message = ws._link_messages.get()
        # if not message:
        #     continue
            try:
                handler.handle(message)
            except Exception as err:
                import traceback
                traceback.print_exc()
                handler.sendReq('ws-error', {'code': KERR.WEBSOCKET_ERR, 'msg': str(err)})
                continue
        else:
            time.sleep(0.05)
    logging.warn("WS connection closed %s" %instanceTag)
    if handler:
        handler.disconnect()
    mutex.release()
    handler = None
    
  