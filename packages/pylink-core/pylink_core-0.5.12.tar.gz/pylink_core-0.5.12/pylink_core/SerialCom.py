import os
import glob
import logging
import sys
import serial
import serial.tools.list_ports as list_ports
import time
import platform
import threading

from collections import deque

import array
import usb.core
import usb.util
import usb.control

# meowbit vendor and pid
cdclist = [
    (0xf055, 0x9800, 'meowbit'),
    (10473, 394, 'meow32'),
    # (0x28E9, 0x0380, 'joyfrog'),
]
CDC_COMM_INTF = 1

DEBUG = False

# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
def serialList():
    """Lists serial ports
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    serialPortList = []
    for port in list_ports.comports():
        print("usb dev", port)
        if (port.pid and port.vid):
            serialPortList.append({'name': port.description, 'type':'serial', 'peripheralId': port.device, 'pid': port.pid, 'vid': port.vid})
        elif 'usbmodem' in port.device:
            if "ARM64" in str(os.uname()):
                # mac m1 return without pid/vid
                # 394 === e.pid && 10473 === e.vid
                serialPortList.append({'name': port.device, 'type':'serial', 'peripheralId': port.device, 'pid': 394, 'vid': 10473})


    if platform.system() == "Windows":
        try:
            for (vid,pid,pname) in cdclist:
                usbCdc = usb.core.find(idVendor=vid, idProduct=pid)
                if usbCdc:
                    serialPortList.append({
                        'name': "CDC %s" %pname,
                        'type':'serial',
                        'peripheralId': "USB_CDC_%s" %pname,
                        'pid': pid,
                        'vid': vid
                    })
        except Exception as err:
            if "No backend available" in str(err):
                pass
            else:
                logging.warn("usb cdc error: %s" %err)

    return serialPortList

class serialRead(threading.Thread):
    def __init__(self,ser,fifo,cb,tag):
        self.ser = ser
        self.cb = cb
        self.tag = tag
        self.fifo = fifo
        self.running = True
        self.rawMode = False
        self.t = time.clock()
        threading.Thread.__init__(self)
    
    def run(self):
        if DEBUG: logging.info("thread {} start ------------------------------".format(self.tag))
        while self.running:
            try:
                c = self.ser.read(64)
                if c:
                    dt = (time.clock() - self.t)*1000000
                    if self.ser.pybMutex:
                        self.fifo.extend(c)
                        if DEBUG: logging.info("[{}] rd: {}".format(self.tag, c))
                    else:
                        self.cb(c, dt)
                    self.t = time.clock()
            except Exception as err:
                logging.warn("Serial Read error %s" %err)
                self.running = False
                self.cb(None, -1)
        if DEBUG: logging.info("thread {} end -------------------------------".format(self.tag))

class cdcRead(threading.Thread):
    def __init__(self,ep,fifo,cb):
        self.ep = ep
        self.cb = cb
        self.fifo = fifo
        self.running = True
        self.timeout = 200
        self.t = time.clock()
        threading.Thread.__init__(self)
    
    def run(self):
        while self.running:
            try:
                c = self.ep.read(self.ep.wMaxPacketSize, self.timeout)
                if c:
                    dt = (time.clock() - self.t)*1000000
                    if self.ep.pybMutex:
                        self.fifo.extend(c)
                    else:
                        self.cb(c, dt)
                    self.t = time.clock()
            except Exception as err:
                errLog = str(err)
                if 'timeout error' in errLog:
                    pass
                else:
                    logging.warn("CDC Read error %s" %err)
                    self.running = False
                    self.cb(None, -1)

class serialCom():
    opened = False
    usbdev = None
    serdev = None
    readThread = None
    def __init__(self,rxCallback, dbgTag=""):
        if serialCom.readThread:
            serialCom.readThread.running = False
            serialCom.readThread.join()
            if DEBUG: logging.info("serial thread join")
        self.rxcb = rxCallback
        self.ser = serialCom.serdev
        self.dev = serialCom.usbdev
        self.rxth = None
        self.ep_out = None
        self.ep_in = None

        self.dbgTag = dbgTag
        
        # bit1: rts,    bit0: dtr
        # bit1: en,     bit0: boot0
        self.dtr = 0x1
        self.rts = 0x1
        self.cacheBaud = 115200
        self.cacheTimeout = 200
        return

    @property
    def baudrate(self):
        if self.ser:
            return self.ser.baudrate
        elif self.dev:
            return self.cacheBaud
    
    @baudrate.setter
    def baudrate(self, baud):
        if self.ser:
            self.ser.baudrate = baud
        elif self.dev:
            # print("set baud", baud)
            ary = [0, 0, 0, 0, 0x00, 0x00, 0x08]
            ary[0] = baud & 0xff
            ary[1] = (baud>>8) & 0xff
            ary[2] = (baud>>16) & 0xff
            ary[3] = (baud>>24) & 0xff
            self.dev.ctrl_transfer(0x21, 0x20, 0, CDC_COMM_INTF, array.array('B', ary))
            self.cacheBaud = baud

    @property
    def timeout(self):
        if self.ser:
            return self.ser.timeout
        elif self.dev:
            # print("get timeout", self.cacheTimeout)
            return self.cacheTimeout/1000

    @timeout.setter
    def timeout(self,timeout):
        if self.ser:
            self.ser.timeout = timeout
        elif self.dev:
            self.cacheTimeout = int(timeout*1000)
            self.rxth.timeout = self.cacheTimeout
            # print("set timeout", self.cacheTimeout)

    def setDTR(self, state):
        if self.ser:
            self.ser.dtr = state
        elif self.dev:
            self.dtr = state
            # print("set dtr", state)
            self.dev.ctrl_transfer(0x21, 0x22, ((self.rts&0x1)<<1) | (self.dtr&0x1), CDC_COMM_INTF, None)

    def setRTS(self, state):
        if self.ser:
            self.ser.rts = state
        elif self.dev:
            self.rts = state
            # print("set rts", state)
            self.dev.ctrl_transfer(0x21, 0x22, ((self.rts&0x1)<<1) | (self.dtr&0x1), CDC_COMM_INTF, None)

    def hardwareReset(self):
        self.setDTR(0)
        self.setRTS(0)
        time.sleep(0.1)
        self.setDTR(1)
        self.setRTS(1)

    def flushInput(self):
        if self.ser:
            self.ser.flushInput()
        elif self.dev:
            self.fifo.clear()

    def flushOutput(self):
        if self.ser:
            self.ser.flushOutput()
        elif self.dev:
            "todo: flush output for cdc"

    def setPybMutex(self, v):
        if DEBUG: print("\033[1;34m mutex %s \033[0m" %(v))
        if self.ser:
            self.ser.pybMutex = v
        if self.ep_in:
            self.ep_in.pybMutex = v

    def cdcCallbackHook(self, msg, dt):
        if msg == None and dt == -1:
            if DEBUG: print("\033[0;31m cdc closed \033[0m")
            self.opened = False
            usb.util.release_interface (self.dev, 2)
            usb.util.release_interface (self.dev, CDC_COMM_INTF)
            usb.util.dispose_resources(self.dev)
            self.dev = serialCom.usbdev = None
        self.rxcb(msg, dt)

    def serCallbackHook(self, msg, dt):
        if msg == None and dt == -1:
            try:
                if DEBUG: print("\033[0;31m ser closed \033[0m")
                self.opened = False
                self.ser.close()
            except:
                pass
            self.ser = serialCom.serdev = None
        self.rxcb(msg, dt)
    
    def connect(self,port,baud=115200,timeout=0.05):
        self.fifo = deque()
        if port.startswith('USB_CDC'):
            # zadig mewobit stm32
            # only config once for cdc runtime
            if self.dev:
                try:
                    # quick test if cdc dev is still available
                    self.dev.ctrl_transfer(0x21, 0x22, ((self.rts&0x1)<<1) | (self.dtr&0x1), CDC_COMM_INTF, None)
                except:
                    self.dev = None
            if self.dev == None:
                for (vid,pid,pname) in cdclist:
                    usbCdc = usb.core.find(idVendor=vid, idProduct=pid)
                    if usbCdc:
                        serialCom.usbdev = usbCdc
                        break
                self.dev = serialCom.usbdev
                self.dev.set_configuration(1)
                usb.util.claim_interface(self.dev, CDC_COMM_INTF)

            self.cfg = self.dev.get_active_configuration()
            self.intf = self.cfg[(1, 0)]
            # stick endpoint in and out setup
            self.ep_out = self.intf[0]
            self.ep_in = self.intf[1]
            # baudrate at 115200
            self.dev.ctrl_transfer(0x21, 0x22, ((self.rts&0x1)<<1) | (self.dtr&0x1), CDC_COMM_INTF, None)
            # print("cdc conn baud", baud)
            self.dev.ctrl_transfer(0x21, 0x20, 0, CDC_COMM_INTF, array.array('B', [(baud & 0xff), ((baud>>8) & 0xff), ((baud>>16) & 0xff), 0x00, 0x00, 0x00, 0x08]))
            # self.dev.ctrl_transfer(0x21, 0x20, 0, CDC_COMM_INTF, array.array('B', [0x40, 0x42, 0x0f, 0x00, 0x00, 0x00, 0x08]))

            setattr(self.ep_in, 'pybMutex', False)
            self.rxth = cdcRead(self.ep_in,self.fifo,self.cdcCallbackHook)
            self.rxth.setDaemon(True)
            self.rxth.start()

        else:
            if not self.ser:
                self.ser = serial.Serial(port, baud, timeout=timeout, write_timeout=0)
                serialCom.serdev = self.ser
            setattr(self.ser, 'pybMutex', False)
            self.rxth = serialRead(self.ser,self.fifo,self.serCallbackHook,self.dbgTag)
            self.rxth.setDaemon(True)
            self.rxth.start()
        serialCom.readThread = self.rxth
        self.opened = True
    
    def close(self):
        print("comm close {}".format(self.dbgTag))
        if self.rxth:
            self.rxth.running = False
        if self.ser:
            'riven, 保持后台实例，下一次页面打开更快且不冲突'
            # self.hardwareReset()
            # time.sleep(0.2)
            # self.ser.close()
        if self.dev:
            ''
            # usb.util.release_interface (self.dev, 2)
            # usb.util.release_interface (self.dev, CDC_COMM_INTF)
            # self.dev.reset() # only reset, no replug event
            # usb.util.dispose_resources(self.dev)
        # todo: find correct api to toggle usb device on disconnect
        # self.dev = None
        self.rxth = None
        
    def write(self,msg):
        if DEBUG: logging.info("[{}] wr: {}".format(self.dbgTag, msg))
        if self.ser:
            self.ser.write(msg)
        if self.dev:
            self.ep_out.write(msg)

    def read(self, size=1):
        # if self.ser:
        #     return self.ser.read(size)
        # elif self.dev:
        timeout_count = 0
        while len(self.fifo) < size:
            time.sleep(0.01)
            if timeout_count > 100:
                break
            timeout_count += 1
        data = b''
        while len(data) < size and len(self.fifo) > 0:
            data += bytes([self.fifo.popleft()])
        return data

    def inWaiting(self):
        # if self.ser:
        #     return self.ser.inWaiting()
        # elif self.dev:
        n_waiting = len(self.fifo)
        if not n_waiting:
            try:
                dt = self.cacheTimeout/1000/100
                for t in range(100):
                    time.sleep(dt)
                    if len(self.fifo):
                        return len(self.fifo)
                return len(self.fifo)
            except Exception:
                return 0
        else:
            return n_waiting

