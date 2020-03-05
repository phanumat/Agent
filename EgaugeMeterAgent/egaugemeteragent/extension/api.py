# -*- coding: utf-8 -*-
import time
import json
import requests
import socket
from struct import pack
from bs4 import BeautifulSoup

import urllib, datetime
from xml.etree import ElementTree as ET


class API:
    def __init__(self, **kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True
        self.set_variable('offline_count', 0)
        self.set_variable('connection_renew_interval', 6000)

    def renewConnection(self):
        pass

    def set_variable(self, k, v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self, k):
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
    # getDeviceStatus(), printDeviceStatus()
    def getDeviceStatus(self):

        getDeviceStatusResult = True
        import requests
        url = 'http://'+self.get_variable("ip") + "/cgi-bin/egauge?inst&tot"
        print(url)
        response = urllib.request.urlopen(url)
        data = response.read()  # a `bytes` object
        text = data.decode('utf-8')  # a `str`;
        soup = BeautifulSoup(text, 'xml')

        try:
            for h in soup.find_all(n="MDB PANEL"):
                mdb_text = h.find('i')

            mdb = (mdb_text.text)
        except:
            print ("error no mdb i data")

        try:
            for h in soup.find_all(n="1 Floor Plug"):
                floor1plug_text = h.find('i')
            floor1plug = (floor1plug_text.text)
        except:
            print("error no 1floorplug i data")

        try:
            for h in soup.find_all(n="1 Floor Light"):
                floor1light_text = h.find('i')
            floor1light = (floor1light_text.text)
        except:
            print("error no 1floorlight i data")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            for h in soup.find_all(n="1 Floor Air"):
                floor1air_text = h.find('i')
            floor1air = (floor1air_text.text)
        except:
            print("error no 1floorlight i data")

        try:
            for h in soup.find_all(n="2 Floor Plug"):
                floor2plug_text = h.find('i')
            floor2plug = (floor2plug_text.text)
        except:
            print("error no 2floorplug i data")

        try:
            for h in soup.find_all(n="2 Floor Light"):
                floor2light_text = h.find('i')
            floor2light = (floor2light_text.text)
        except:
            print("error no 2floorlight i data")

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            for h in soup.find_all(n="2 Floor Air"):
                floor2air_text = h.find('i')
            floor2air = (floor2air_text.text)
        except:
            print("error no 2floorlight i data")


        try:
            for h in soup.find_all(n="EBD"):
                edb_text = h.find('i')
            edb = (edb_text.text)
        except:
            print("error no 2floorlight i data")


        self.set_variable('mdb', str(mdb))
        self.set_variable('floor1plug', str(floor1plug))
        self.set_variable('floor1light', str(floor1light))
        self.set_variable('floor1air', str(floor1air))
        self.set_variable('floor2plug', str(floor2plug))
        self.set_variable('floor2light', str(floor2light))
        self.set_variable('floor2air', str(floor2air))
        self.set_variable('edb', str(edb))
        self.printDeviceStatus()

    def printDeviceStatus(self):
        # now we can access the contents of the JSON like any other Python object
        print(" the current status is as follows:")
        print(" mdb = {}".format(self.get_variable('mdb')))
        print(" floor1plug = {}".format(self.get_variable('floor1plug')))
        print(" floor1light = {}".format(self.get_variable('floor1light')))
        print(" floor1air = {}".format(self.get_variable('floor1air')))
        print(" floor2plug = {}".format(self.get_variable('floor2plug')))
        print(" floor2light = {}".format(self.get_variable('floor2light')))
        print(" floor2air = {}".format(self.get_variable('floor2air')))
        print(" edb = {}".format(self.get_variable('edb')))


    # ----------------------------------------------------------------------


# This main method will not be executed when this class is used as a module
def main():
    # -------------Kittchen----------------
    meter = API(model='eGauge', api='API3', agent_id='05EGA010101', types='imeter', device='egauge50040',
                ip='192.168.10.21', port=82)

    meter.getDeviceStatus()
    # time.sleep(3)


if __name__ == "__main__": main()
