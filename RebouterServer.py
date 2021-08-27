from xmlrpc.server import SimpleXMLRPCServer
import RPi.GPIO as GPIO
import time, os

#Initialized the pi's GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

#Define server and create it
server = SimpleXMLRPCServer(('192.168.1.163', 6870), logRequests=True)
gateway_address = "192.168.100.1"

def get_router_status():
    global gateway_address
    for _ in range(25):
        status = os.system(f"timeout 1 ping -c 1 {gateway_address}")
        if status == 0:
            return "OK"
    return "Unreachable"

    

#Define any functions we want available
def reboot_router(wait_time):
    print("Rebooting...")
    GPIO.output(17, True)
    time.sleep(wait_time)
    GPIO.output(17, False)
    router_status = get_router_status()
    if router_status == "OK":
        return "Router rebooted successfully!"
    else:
        return "Router rebooted but gateway is not currently reachable"

#Register these functions with the server instance
server.register_function(reboot_router)

#If 
if __name__ == '__main__':
    try:
        print('NetRouter service active')
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nExiting')