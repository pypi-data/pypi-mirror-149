from win32com.client import GetObject
from subprocess import Popen
from wmi import WMI

class SAP:
    
    # constructor
    def __init__(self):
        self.connection = None
        self.session = None

    # methods
    def app(self):
        wmi_object = WMI()
        
        # checking if SAP is already open
        sap_open = len(wmi_object.Win32_Process(name='saplgpad.exe')) > 0

        if not sap_open:
            # opening SAP
            Popen(['C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplgpad.exe'])

        # connecting scripts to SAP
        return GetObject("SAPGUI").GetScriptingEngine

    def connect_sap(self, connection_name):
        # opening given SAP environment
        self.connection = SAP.app().OpenConnection(connection_name)
        self.session = self.connection.Children(0)

        # trying to close SAP GUI if it is already open
        try:
            self.session.findById("wnd[1]/usr/radMULTI_LOGON_OPT1").select()
            self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
        except:
            pass

        self.session.findById("wnd[0]").sendVKey(0)

        return self.session
