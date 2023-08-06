from .MeowbitHandler import MeowbitHandler

class HardwareHandlerFactory:
  def handle(self, hwVersion, websocket, extensions, userPath, tag=""):
    if hwVersion == 'meowbit':
      return MeowbitHandler(websocket, extensions, userPath, tag)
