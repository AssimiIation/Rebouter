from xmlrpc.server import SimpleXMLRPCServer
import RPi.GPIO as GPIO
import atexit
import time

#Initialized the pi's GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

#Define server and create it
server = SimpleXMLRPCServer(('192.168.1.163', 6870), logRequests=True)

#Define any functions we want available
def reboot_router(wait_time):
    print("Rebooting...")
    GPIO.output(17, True)
    time.sleep(wait_time)
    GPIO.output(17, False)
    print("router rebooted")
    return("OK")

#Register these functions with the server instance
server.register_function(reboot_router)

#If 
if __name__ == '__main__':
    try:
        print('NetRouter service active')
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nExiting')