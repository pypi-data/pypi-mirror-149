import platform
from .ExecThread import *
from .Uf2Manager import *
from .SerialCom import serialList, serialCom
from .uflash import getDisk
from .ImageManager import saveToBmp
from .kerror import KERR
import shutil,os,time


class HardwareHandler:
  def __init__(self, ws, extensions, userPath, dbgTag=""):
    self.closed = False
    self.ws = ws
    self.extensions = extensions
    self.ext = self.extensions['meow32']
    self.comm = None
    self.commType = None
    self.commList = []
    self.uploadTh = None
    self.pid = 0
    self.params = []
    self.userPath = userPath
    self.usbStatus = []
    self.meow32_ID = "USB\VID_F055&PID_9800&MI_01"
    self.mewbit_ID = "USB\VID_28E9&PID_018A"
    self.dbgTag = dbgTag

  def sendResp(self, pid, result, error=None):
      """发送response"""
      res = {
          "jsonrpc":"2.0",
          "id": pid,
          "result": result
      }
      if error:
          res['error'] = error
      try:
        if not self.closed:
          logging.info("[{}]<<< {}".format(self.dbgTag, json.dumps(res)))
          self.ws.send(json.dumps(res))
      except Exception as err:
        print(err)

  def sendReq(self,method, params={}):
      """发送request"""
      req = {
          "jsonrpc":"2.0",
          "method":method,
          "params": params
      }
      try:
        if not self.closed:
          logging.info("[{}]<<< {}".format(self.dbgTag, json.dumps(req)))
          self.ws.send(json.dumps(req))
      except Exception as err:
        print(err)

  def commRx(self,msg, dt):
      """发送串口读到的数据"""
      if msg == None and dt == -1:
          self.sendReq('connclose')
      else:
          b64 = str(base64.b64encode(msg), 'utf8')
          self.sendReq("data", {"data": b64})

  def handle(self,message):
      """
      供外部使用的方法
      处理收到消息的method/params/id
      根据收到消息的method执行名称对应的方法
      """
      obj = json.loads(message)
      logging.info("[{}]>>> {}".format(self.dbgTag, message))
      if 'id' in obj:
          self.pid = obj['id']
      if 'params' in obj:
          self.params = obj['params']
      method = obj['method']
      method = method.replace("-", "_")
      func = getattr(self, method, None)
      func()

  def sync(self):
    """与前端连接建立收到第一条消息"""
    extId = self.params['extensionId']
    self.ext = self.extensions[extId]
    self.sendResp(self.pid, self.ext)
  
  def link_version(self):
    import pkg_resources
    version = pkg_resources.get_distribution("pylink_core").version
    self.sendResp(self.pid, {'version': version})
  
  def install_driver(self):
    if os.name == 'nt':
      try:
        # 1. download filter driver installer
        import tempfile,requests
        tmp = tempfile.mkdtemp()
        url = "http://kittenbot.gitee.io/xes_deploy/kittenbot_filterdrv_1.0.2.0.exe"
        if 'url' in self.params:
          url = self.params['url']
        r = requests.get(url, verify=False)
        if r.ok:
          totalSize = int(r.headers.get('content-length', 0))
          tmpPath = os.path.join(tmp, os.path.basename(url))
          with open(tmpPath, 'wb') as f:
            dataWritten = 0
            for data in r.iter_content(16384):
              f.write(data)
              dataWritten += len(data)
              self.sendReq("upload-status", {"text": "downloading installer".format(dataWritten, totalSize), "progress": int(dataWritten/totalSize*100)})
          n = os.system(tmpPath + " /S")
          self.sendResp(self.pid, {"status": 'ok', 'code': n})
        else:
          self.sendResp(self.pid, None, {"error": "installer download fail", "code": KERR.DRIVER_INSTALL_DOWNLOADFAIL})
        # 2. exec installer
      except Exception as err:
        self.sendResp(self.pid, None, {"error": str(err), "code": KERR.DRIVER_INSTALL_FAIL})
    else:
      self.sendResp(self.pid, None, error={"msg":"No Driver install need for osx", "code":KERR.DRIVER_INSTALL_OSX})

  def listdevice(self):
    """查看可用串口列表"""
      # 1. 检测盘符
    disk = getDisk("PYBFLASH", "2M")
    diskboot = getDisk("ARCADE-F4")
    if diskboot:
      self.sendResp(self.pid, None, error={"msg":"in bootloader mode", "code":KERR.DISK_IN_BOOTLOADER_MODE})
      return
    if platform.system() == "Windows":
      try:
        import win32com.client
        # 添加设备信息到列表
        # win7不引用下面会报错
        import pythoncom
        pythoncom.CoInitialize ()
        win32 = win32com.client.GetObject("winmgmts:")
        self.usbStatus = []
        for usb in win32.InstancesOf("win32_pnpentity"):
          if usb.PNPDeviceID.find(self.meow32_ID) > -1 or usb.PNPDeviceID.find(self.mewbit_ID) > -1:
              self.usbStatus.append({
                "name":usb.Name,
                "errCode":usb.ConfigManagerErrorCode,
                "usbsta":usb.Status
              })

        print(self.usbStatus)
        if len(self.usbStatus):
          for item in self.usbStatus:
            if item["usbsta"] == 'OK':
              # 串口正常，准备连接
              break
            else:
              self.sendResp(self.pid, None, error = {"msg": self.usbStatus, "code": KERR.CANNOT_FIND_COMMPORT_BUTDISK})
        else:
          # 没有设备
          self.sendResp(self.pid, None, error = {"msg": "no device", "code": KERR.CANNOT_FIND_COMMPORT})  
      except Exception as ex:
        # 调用windows中的接口报错
        serPorts = serialList()
        if not serPorts and disk:
          # 如果没有串口但是有盘符
          self.sendResp(self.pid, None, error={
              "msg":"find disk but no comm port", 
              "code":KERR.CANNOT_FIND_COMMPORT_BUTDISK,
              "platform": platform.system(), 
              "release": platform.release(),
              "windowsAPIErr": str(ex)
            })
          return
        elif serPorts:
          # 正常流程，有通信端口
          self.commList = serPorts
          self.sendResp(self.pid, self.commList)
          # print('>>>',ex)
          return
        else:
          # 没有串口,也没盘符,提示用户插入硬件 (esp32同样有效)
          self.sendResp(self.pid, None, error={"msg":"No comm port", "code":KERR.CANNOT_FIND_COMMPORT,"windowsAPIErr": str(ex)})
          return



      serPorts = serialList()
      self.commList = serPorts
      self.sendResp(self.pid, self.commList)
    else:
      serPorts = serialList()
      self.commList = serPorts
      self.sendResp(self.pid, self.commList)

  def connect(self):
    """连接串口"""
    peripheralId = self.params['peripheralId']
    port = None
    if '@' in peripheralId:
      peripheralId = peripheralId.split('@')[0]
    for p in self.commList:
        if p['peripheralId'] == peripheralId:
            port = p
            break
    try:
      if not port:
        raise Exception("无法找到串口 {}".format(peripheralId))
      if port['pid'] == 38912: # meowbit stm32
        if self.ext['id'] != 'meowbit':
          self.ext = self.extensions['meowbit']
      else:
        if self.ext['id'] != 'meow32':
          self.ext = self.extensions['meow32']
      
      if port['type'] == 'serial':
          self.comm = serialCom(self.commRx, self.dbgTag)
          self.comm.connect(p['peripheralId'], baud=1000000)
          self.commType = 'serial'
      self.sendResp(self.pid, p)
    except Exception as e:
      msg = str(e)
      if 'PermissionError' in msg:
        msg = '通信端口被占用，请检查是否有其他页面已经打开了掌机'
      err = {
          "msg": msg,
          "code": KERR.SERIAL_COMM_ERROR
      }
      self.sendResp(self.pid, None, error=err)
    finally:
      print("connected", self.comm)

  def disconnect(self):
    if self.comm :
      self.comm.close()
      
  def write(self):
    """通过串口写数据"""
    msg = self.params['data']
    msg = base64.b64decode(msg)
    # print(msg)
    if self.comm:
        self.comm.write(msg)