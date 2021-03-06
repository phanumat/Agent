# -*- coding: utf-8 -*-

from pyHS100 import Discover
from pyHS100 import SmartPlug
import time

class API:
    def __init__(self,**kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count',0)
        self.set_variable('connection_renew_interval', 6000)
        self.only_white_bulb = None

    def renewConnection(self):
        pass

    def set_variable(self,k,v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self,k):
        return self.variables.get(k, None)  # default of get_variable is none

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label            GET          label in string
    status           GET          status
    unitTime         GET          time
    type             GET          type      
     ------------------------------------------------------------------------------------------
    '''

    '''
    API3 available methods:
    1. getDeviceStatus() GET
    2. setDeviceStatus() SET
    '''

    # ----------------------------------------------------------------------
    # getDeviceStatus(), getDeviceStatusJson(data), printDeviceStatus()
    def getDeviceStatus(self):

        ip = self.get_variable("ip")
        port = self.get_variable("port")
        p = SmartPlug(ip)
        emeter_info = p.get_emeter_realtime()
        self.set_variable('status', str(p.state))
        self.set_variable('current', str(emeter_info['current']))
        self.set_variable('voltage', str(emeter_info['voltage']))
        self.set_variable('power', str(emeter_info['power']))
        self.printDeviceStatus()

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" status = {}".format(self.get_variable('status')))
        print(" current = {}".format(self.get_variable('current')))
        print(" voltage = {}".format(self.get_variable('voltage')))
        print(" power = {}".format(self.get_variable('power')))
        print("---------------------------------------------")

    # setDeviceStatus(postmsg), isPostmsgValid(postmsg), convertPostMsg(postmsg)
    def setDeviceStatus(self, postmsg):
        setDeviceStatusResult = True
        ip = self.get_variable("ip")
        port = self.get_variable("port")
        p = SmartPlug(ip)

        if postmsg['status'] == 'ON':
            p.turn_on()
        if postmsg['status'] == 'OFF':
            p.turn_off()

    # ----------------------------------------------------------------------

# This main method will not be executed when this class is used as a moduled
def main():

    # -------------Kittchen----------------
    TPLINK = API(model='TPlinkPlug', api='API3', agent_id='TPlinkPlugAgent',types='plug', ip='192.168.10.123',
                  port=9999)

    TPLINK.getDeviceStatus()
    # TPLINK.setDeviceStatus({"status": "ON"})
    # time.sleep(3)
    # TPLINK.getDeviceStatus()
    # TPLINK.setDeviceStatus({"status": "OFF"})
    # time.sleep(3)
    # TPLINK.getDeviceStatus()
    # TPLINK.setDeviceStatus({"status": "ON"})
    # time.sleep(3)
    # TPLINK.getDeviceStatus()

if __name__ == "__main__": main()
