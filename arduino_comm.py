import struct, sys, time
import serial

class ArduinoComm(object):
#    """A class to define a Minolta LS100 (or LS110?) photometer
#    """

    longName = "Arduino joystick logger"

    def __init__(self, port, maxAttempts=2):
        if type(port) in [int, float]:
            self.portNumber = port #add one so that port 1=COM1
            self.portString = 'COM%i' %self.portNumber #add one so that port 1=COM1
        else:
            self.portString = port
            self.portNumber=None
        self.isOpen=0
        self.lastQual=0
        self.lastLum=None
        self.type='UNO'
        self.com=False
        self.OK=True#until we fail
        self.maxAttempts=maxAttempts

        self.codes={
            'ER00\r\n':'Unknown command',
            'ER01\r\n':'Setting error',
            'ER11\r\n':'Memory value error',
            'ER10\r\n':'Measuring range over',
            'ER19\r\n':'Display range over',
            'ER20\r\n':'EEPROM error (the photometer needs repair)',
            'ER30\r\n':'Photometer battery exhausted',}

        #try to open the port
        if sys.platform in ['darwin', 'win32']:
            try:self.com = serial.Serial(self.portString)
            except:
                self._error("Couldn't connect to port %s. Is it being used by another program?" %self.portString)
        else:
            self._error("I don't know how to handle serial ports on %s" %sys.platform)

        self.com.setByteSize(8)
        self.com.setBaudrate(9600)
        try:
            if not self.com.isOpen():
                self.com.open()
        except:
            self._error("Opened serial port %s, but couldn't connect to ArduinoComm" %self.portString)
        else:
            self.isOpen=1
            
    def measure(self):
        #flush the read buffer first
        #self.com.read(self.com.inWaiting())#read as many chars as are in the buffer
        for attemptN in range(self.maxAttempts):
            #send the message
            time.sleep(0.001)
            self.com.write("M")
            #self.com.flush()
            time.sleep(0.001)
            #get reply (within timeout limit)
            #self.com.setTimeout(timeout)
            #logging.debug('Sent command:'+message[:-2])#send complete message
            retVal= self.com.readline()
            try:
                _x, _y = retVal[:-1].split(",")
                return int(_x), int(_y)
            except Exception, e:
                print e
        return -1, -1
        
    def trial_begin(self):
        self.com.write("h")
        
    def trial_end(self):
        self.com.write("l")
        
    def trial_trajectory_away(self):
        self.com.write("A")
        
    def escape_exp(self):
        self.com.write("l")
        
    def trial_trajectory_center(self):
        self.com.write("C")


    def _error(self, msg):
        self.OK=False
        #logging.error(msg)
        print msg
