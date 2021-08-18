from tkinter import *
from threading import *
import xmlrpc.client
import os

class MessageBox:
    def __init__(self, container):
        self.widget = Text(container, font="Raleway", height=20, width=50, state=DISABLED, wrap='word', borderwidth=2)

    def display_message(self, text, newline=False):
        self.widget.config(state=NORMAL)
        message = text
        if newline == True:
            message = "\n" + text
        self.widget.insert(END, message)
        self.widget.config(state=DISABLED)

def check_connection():
    global server_ip
    msg_window.display_message("Checking connection to server...")
    for _ in range(5):
        status = os.system(f"timeout 1.5 ping -c 1 {server_ip} ")
        if status == 0:
            msg_window.display_message(" OK!")
            reboot_button.config(state=NORMAL)
            return status
        else:
            msg_window.display_message(".", False)
    msg_window.display_message(f"Server at {server_ip} is unreachable", True)

def reboot_router():
    reboot_button.config(state='disabled')
    try:
        msg_window.display_message("Rebooting...", True)
        result = client.reboot_router(10)
        if result == "OK":
            msg_window.display_message("Router rebooted successfully!", True)
        else:
            msg_window.display_message("Error rebooting router. Please try again", True)
        reboot_button.config(state='normal')
    except xmlrpc.client.Fault as error:
        msg_window.display_message(f"Call to server failed with xml-rpc fault: {error}", True)
    except ConnectionError as error:
        msg_window.display_message(f"Connection error (Is the server running?): {error}", True)
    reboot_button.config(state='normal')

def use_thread(method):
    #Create a thread
    t1 = Thread(target=method)
    t1.start()

#Ip/Port may be configureable via GUI in the future
server_ip = "192.168.1.163" 
server_port = '6870'

root = Tk()
root.title("LAN Router Reboot")
root.resizable(False, False)
root.geometry("520x460")

msg_window = MessageBox(root)
msg_window.widget.pack(pady=10)

button_frame = Frame(root)
button_frame.pack()

reboot_button = Button(button_frame, text="Reboot Router", font="Raleway", state=DISABLED, command=lambda: use_thread(reboot_router))
reboot_button.grid(column=0, row=0)

exit_button = Button(button_frame, text="Exit", font="Raleway", command=root.quit)
exit_button.grid(column=1, row=0)

client = xmlrpc.client.ServerProxy(f'http://{server_ip}:{server_port}')

use_thread(check_connection)

root.mainloop()