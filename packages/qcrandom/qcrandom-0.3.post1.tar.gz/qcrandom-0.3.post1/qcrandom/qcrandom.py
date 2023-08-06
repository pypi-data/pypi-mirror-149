import sys
from qiskit import *
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
import logging
import time
import json
import os
import threading
import io

# Define default values
DEFAULT_LOG_FILES = ["qcrandom.log"]
DEFAULT_DEVICE_EXCLUSIONS = []
DEFAULT_DEVICE_EXPIRATION_TIME = 600

# Define default buffer values
DEFAULT_QCBUFFER_SIZE = 100
DEFAULT_QCBUFFER_ACCURACY = 64
DEFAULT_QCBUFFER_REFILL_THRESHOLD = 0.5


def ConfigCheck():
    try:
        # try loading an account
        # works only if account was previously saved
        _qclogger.logger.info("Loading account...")
        IBMQ.load_account()
        _qclogger.logger.info("Account loaded succesfully!")
    except Exception:
        try:
            # try loading an account using token in token.txt
            _qclogger.logger.error("Loading failed! Loading from token.txt")
            with open("token.txt","r") as tokenFile:
                token = tokenFile.readline()
                IBMQ.save_account(token)
                IBMQ.load_account()
                _qclogger.logger.info("Successfully loaded account from token.txt!")
        except Exception:
            # loading account failed - working without ibmq provider
            _qclogger.logger.error("Loading from token.txt failed!")

# Selects backend device
def ChooseBackend(NotASimulator=False):
    try:
        _qclogger.logger.info("Selecting backend...")
        provider = IBMQ.get_provider(hub='ibm-q')
        # lambda filters backends without reset gate and exclusions from configuration file
        servers = provider.backends(filters=lambda b: "reset" in b.configuration().basis_gates and not b.configuration().backend_name in _qcconfig.BackendExclusions, simulator=False, operational=True)
        # select least busy server
        leastbusy = least_busy(servers)
        _qclogger.logger.info(f"Selected {leastbusy}!")
        return leastbusy
    except Exception:
        _qclogger.logger.error("Selecting backend failed!")
        if NotASimulator:
            raise RuntimeError("No quantum computer is available")
        else:
            _qclogger.logger.warning("Using local simulator! Numbers won't be truly random!")
            return BasicAer.get_backend("qasm_simulator")

class _QCLogging:
    def __init__(self):
        self.logger = logging.getLogger('QCLogger')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s: %(levelname)s> %(message)s')
        self.handlers = []
        self.UpdateHandler()
    def UpdateHandler(self):
        # remove all logging handlers
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

        # select new handler
        self.FillHandlers()
        
        # add handlers to logger
        for handler in self.handlers:
            self.logger.addHandler(handler)
    def FillHandlers(self):
        self.handlers.clear()

        for file in _qcconfig.LogFiles:
            if file == 'stdout':
                self.handlers.append(logging.StreamHandler(sys.stdout))
            elif file == 'stderr':
                self.handlers.append(logging.StreamHandler(sys.stderr))
            else:
                self.handlers.append(logging.FileHandler(file))
                
        for handler in self.handlers:
            handler.setFormatter(self.formatter)
        
class _QCBackend:
    def __init__(self):
        ConfigCheck()
        self.lastChange = time.time()
        self.backend = ChooseBackend()
    def GetBackend(self):
        # choosing backends is time-expensive, so we limit it by reusing same backend until it expired
        # expiration time is specified as seconds
        # backend has expiration time because selected device may go into
        # if backend has expired choose a new backend
        if (time.time() - self.lastChange > _qcconfig.BackendExpireTime):
            self.backend = ChooseBackend()
            self.lastChange = time.time()
        return self.backend

class _QCConfig:
    def __init__(self):
        self.LoadDefaultValues()
        # Only load config from file if file exsisted before
        if self.CreateFile():
            self.LoadConfig()
    
    # Set default values
    def LoadDefaultValues(self):
        self.LogFiles = DEFAULT_LOG_FILES
        self.BackendExclusions = DEFAULT_DEVICE_EXCLUSIONS
        self.BackendExpireTime = DEFAULT_DEVICE_EXPIRATION_TIME

        self.BufferSize = DEFAULT_QCBUFFER_SIZE
        self.BufferAccuracy = DEFAULT_QCBUFFER_ACCURACY
        self.BufferRefill = DEFAULT_QCBUFFER_REFILL_THRESHOLD

    # Creates configuration file (if it doesn't exist)
    # Returns True/False. If the value is True that means that config.json exists and it should be loaded during initialization
    def CreateFile(self):
        # If config.json exists return true
        if os.path.exists("config.json"):
            return True

        # Using print, because _QCConfig is initialized before _QCLogger
        print("Couldn't find config.json! Creating new config.json!", file=sys.stderr)
        with open("config.json", "w") as file:
            # self.dict creates a dictionary with all attributes, have to be careful when adding new ones
            file.write(json.dumps(self.__dict__))
        return False

        

    # Loads values from config.json
    def LoadConfig(self):
        with open("config.json", "r") as file:
            config = json.load(file)
            # Copy same keys to _QCConfig from config file
            for key in config.keys():
                if key in self.__dict__.keys():
                    self.__dict__[key] = config[key]
        self.CheckConfig()

    def CheckConfig(self):
        # Change to list of files // for backwards compatibility
        if isinstance(self.LogFiles, str):
            self.LogFiles = [self.LogFiles]

_qcconfig = _QCConfig()
_qclogger = _QCLogging()
_qcbackend = _QCBackend()
_qcbuffer = []

# Returns sum of main buffer's size and secondary buffer's size
def GetNumberCount():
    return len(_qcbuffer) + len(_qcthreading.buffer)

# Returns main buffer's size
def GetMainBufferSize():
    return len(_qcbuffer)
    
# User interface for updating configuration file, updates logging file
def LoadConfig():
    _qcconfig.LoadConfig()
    _qclogger.UpdateHandler()
    
# Returns number of digits the random number will be rounded to
def GetRoundFactor(accuracy):
    return len(str(2**accuracy))

# Calculates number between 0 and 1 based on string returned by qiskit job
def CalculateFraction(strValue, accuracy):
    return round(int(strValue, 2) / (2**accuracy - 1), GetRoundFactor(accuracy))

# Fills secondary buffer
def GenerateBuffer(accuracy, buffersize):
    assert accuracy > 1, "Accuracy must be higher than 1!"
    assert buffersize > 0, "Buffer size must be higher than 0!"

    # creating a quantum circuit
    qr = QuantumRegister(1)
    cr = ClassicalRegister(accuracy)
    circuit = QuantumCircuit(qr, cr)

    for j in range(accuracy):
        circuit.h(0)
        circuit.measure(0, j)
        # skipping last reset (it doesn't change anything)
        if j < accuracy - 1:
            circuit.reset(0)

    job = execute(circuit, _qcbackend.GetBackend(), shots=buffersize, memory=True)
   
    # Save the results of job_monitor to temporary string stream
    stream = io.StringIO("")
    job_monitor(job, interval=5, output=stream)
    _qclogger.logger.info(stream.getvalue())

    data = job.result().get_memory()

    # clear the buffer and fill it with new data
    _qcthreading.buffer.clear()
    for number in data:
        _qcthreading.buffer.append(CalculateFraction(number, accuracy))
    
    _qclogger.logger.info(f"Second thread finished working, main buffer size {GetMainBufferSize()}, secondary buffer size {len(_qcthreading.buffer)}")

# wrapper around GenerateBuffer with accuracy and size specified in _qcconfig
def _QCGenerateBuffer():
    GenerateBuffer(_qcconfig.BufferAccuracy, _qcconfig.BufferSize)

class _QCThreading:
    def __init__(self):
        self.buffer = []
        self.startGenerating()
    # Main function that starts fetching numbers in the background
    def startGenerating(self):
        _qclogger.logger.info(f"Second thread started working, main buffer size {GetMainBufferSize()}")
        self.thread = threading.Thread(target=_QCGenerateBuffer)
        self.thread.start()
    # The thread is ready if it isn't working and secondary buffer is empty
    def isReady(self):
        return not self.thread.is_alive() and len(self.buffer) == 0
    # Copies values from secondary buffer to the main buffer
    def copyBuffer(self):
        self.thread.join()
        _qcbuffer.extend(_qcthreading.buffer)
        self.buffer.clear()


_qcthreading = _QCThreading()

# Calculates refill threshold as number of items
def GetRefillThreshold():
    return int(_qcconfig.BufferRefill * _qcconfig.BufferSize)

# Returns first number from the buffer and removes it off the list
def GetNumber():
    number = _qcbuffer[0]
    _qcbuffer.pop(0)
    return number

# Starts second thread / copies values from secondary bufer to the main buffer
def CheckBufferState():
    assert _qcconfig.BufferRefill <= 1.0, "Buffer refill threshold must be lower or equal to 1!"
    assert _qcconfig.BufferRefill >= 0, "Buffer refill threshold must be higher or equal to 0!"
    
    if GetMainBufferSize() <= GetRefillThreshold():
        # start the second thread only if it isn't working and secondary buffer is empty
        if _qcthreading.isReady():
            _qcthreading.startGenerating()
    # refill main buffer when it's empty
    if GetMainBufferSize() == 0:
        _qcthreading.copyBuffer()

# Main interface - generates random numbers between left and right
def QCRandom(left, right, accuracy=16):
    assert accuracy > 1, "Accuracy must be higher than 1!"
    assert left < right, "Left must be lower than right!"
    CheckBufferState()

    ret = GetNumber() * abs(right - left) + left
    return round(ret, GetRoundFactor(accuracy))
