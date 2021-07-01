import serial
import time
# message
class RoboteqHandler:
    """
    Create a roboteq device object for communication
    """

    def __init__(self):
        self.port = ""
        self.baudrate = 115200
        self.ser = None
    
    def connect(self, port, baudrate = 115200):
        """
        Attempt to establish connection with the controller
        If the attempt fails, the method will return False otherwise, True.
        """
        self.port = port
        self.baudrate = baudrate
        
        try: # attempt to create a serial object and check its status
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baudrate,
                parity = serial.PARITY_NONE,
                stopbits = serial.STOPBITS_ONE,
                bytesize = serial.EIGHTBITS,
                timeout = 0.04
            )
            # if self.ser.isOpen():
            #     self.ser.close()
            # self.ser.open()

        except Exception as e:
            # TODO
            pass
            

    def request_handler(self, request= ""):
        """
        Sends a command and a parameter, 
        """
        try:
            raw_command = "%s+\r"%(request)
            self.ser.write(raw_command.encode())

            char_echo = self.ser.readline() # This is the char echo
            result = self.ser.readline() # Actual response
            # result = result.split("\r")
            return result
        except Exception as e:
            #TODO
            print("Exception at request_handler function")
            
    
    def send_command(self, command, first_parameter = "", second_parameter = ""):
        if first_parameter != "" and second_parameter != "":
            message = "%s %s %s "%(command,first_parameter,second_parameter)
        if first_parameter != "" and second_parameter == "":
            message = "%s %s "%(command,first_parameter)
        if first_parameter == "" and second_parameter == "":
            message = "%s "%(command)
        
        response = self.request_handler(message)
        return response

    def read_value(self, command= "", parameter = ""):
        """
        Constructs a message and sends it to the controller.
        param: command (str)
        param: parameter (str/int)
        returns: answer from the controller, data from request commands, or echo from action commands.
        """
        request = "%s [%s]"%(command,parameter)
        response = self.request_handler(request)
        return response
